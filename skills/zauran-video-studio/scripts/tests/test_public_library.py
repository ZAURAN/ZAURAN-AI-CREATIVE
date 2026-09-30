import contextlib
import hashlib
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from test_library import library, archive_bytes


class PublicLibraryTests(unittest.TestCase):
    def fixture(self, root):
        raw = archive_bytes([('repo-pin/SKILL.md', b'full original'), ('repo-pin/ref.md', b'full ref')])
        source = {'repository': 'owner/repo', 'commit': 'a' * 40,
                  'archive_url': 'https://codeload.github.com/owner/repo/zip/' + 'a' * 40,
                  'archive_file': 'repo-pin.zip', 'bytes': len(raw),
                  'sha256': hashlib.sha256(raw).hexdigest()}
        entry = {'id': 'repo:owner/repo:SKILL.md', 'title': 'Fixture', 'kind': 'repository_skill',
                 'source': 'owner/repo', 'status': 'upstream_pinned',
                 'sha256': hashlib.sha256(b'full original').hexdigest(),
                 'document': {'source_archive': 'owner/repo', 'member': 'repo-pin/SKILL.md'},
                 'materialize': {'source_archive': 'owner/repo'}}
        refs = root / 'references'
        (refs / 'upstream').mkdir(parents=True)
        (refs / 'source-registry.json').write_text(json.dumps({'sources': [source]}))
        (refs / 'library-index.json').write_text(json.dumps({'entries': [entry]}))
        payload = {'payload': 'references/upstream/local.snapshot.zip', 'bytes': len(raw), 'sha256': source['sha256']}
        (refs / 'upstream/payload-manifest.json').write_text(json.dumps({'payloads': [payload]}))
        return raw, source, entry

    def response(self, raw, url):
        response = io.BytesIO(raw)
        response.geturl = lambda: url
        return response

    def test_source_fetch_verifies_and_reuses_cache_without_network(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            raw, source, entry = self.fixture(root)
            with mock.patch.object(library, 'urlopen', return_value=self.response(raw, source['archive_url'])) as opener:
                result = library.fetch_source(root, 'owner/repo')
            self.assertFalse(result['cached'])
            self.assertEqual(opener.call_count, 1)
            with mock.patch.object(library, 'urlopen', side_effect=AssertionError('network called')):
                self.assertTrue(library.fetch_source(root, 'owner/repo')['cached'])
            self.assertEqual(library.read_document(root, entry['document']), b'full original')

    def test_source_fetch_rejects_hash_size_crc_and_preserves_existing_file(self):
        for variation in ('hash', 'short', 'long', 'crc'):
            with self.subTest(variation=variation), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                raw, source, _ = self.fixture(root)
                cache = root / 'references/.cache/repository_archives/repo-pin.zip'
                cache.parent.mkdir(parents=True)
                cache.write_bytes(b'previous invalid bytes')
                bad = raw[:-1] if variation == 'short' else raw + b'x' if variation == 'long' else b'x' * len(raw)
                if variation == 'crc':
                    bad = raw.replace(b'full original', b'fail original')
                    source = {**source, 'sha256': hashlib.sha256(bad).hexdigest()}
                    (root / 'references/source-registry.json').write_text(json.dumps({'sources': [source]}))
                with mock.patch.object(library, 'urlopen', return_value=self.response(bad, source['archive_url'])):
                    with self.assertRaises(ValueError):
                        library.fetch_source(root, 'owner/repo')
                self.assertEqual(cache.read_bytes(), b'previous invalid bytes')
                self.assertEqual(list(cache.parent.glob('*.part')), [])

    def test_source_fetch_rejects_unsafe_metadata_before_network(self):
        for changes in ({'archive_url': 'http://codeload.github.com/owner/repo/zip/' + 'a' * 40},
                        {'archive_url': 'https://evil.test/zip'}, {'archive_file': '../escape.zip'},
                        {'bytes': 134 * 1024 ** 2}, {'repository': '../owner/repo'}, {'commit': 'main'}):
            with self.subTest(changes=changes), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                _, source, _ = self.fixture(root)
                (root / 'references/source-registry.json').write_text(json.dumps({'sources': [{**source, **changes}]}))
                with mock.patch.object(library, 'urlopen') as opener:
                    with self.assertRaises(ValueError):
                        library.fetch_source(root, 'owner/repo')
                    opener.assert_not_called()

    def test_atomic_replace_failure_preserves_destination_and_cleans_partial(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            raw, source, _ = self.fixture(root)
            cache = root / 'references/.cache/repository_archives/repo-pin.zip'
            cache.parent.mkdir(parents=True)
            cache.write_bytes(b'previous')
            with mock.patch.object(library, 'urlopen', return_value=self.response(raw, source['archive_url'])), mock.patch.object(library.os, 'replace', side_effect=OSError('denied')):
                with self.assertRaises(OSError):
                    library.fetch_source(root, 'owner/repo')
            self.assertEqual(cache.read_bytes(), b'previous')
            self.assertEqual(list(cache.parent.glob('*.part')), [])

    def test_attach_exact_payload_and_refuse_wrong_or_unknown_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            raw, _, _ = self.fixture(root)
            incoming = root / 'incoming.zip'
            incoming.write_bytes(raw)
            report = library.attach_payload(root, 'local.snapshot.zip', incoming)
            self.assertEqual(Path(report['path']).read_bytes(), raw)
            incoming.write_bytes(b'wrong')
            with self.assertRaises(ValueError):
                library.attach_payload(root, 'local.snapshot.zip', incoming)
            self.assertEqual(Path(report['path']).read_bytes(), raw)
            with self.assertRaises(ValueError):
                library.attach_payload(root, 'unknown.zip', incoming)

    def test_show_missing_document_mentions_payload_and_preserves_bundle_status(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, _, entry = self.fixture(root)
            entry = {**entry, 'kind': 'skillry_skill', 'source': 'https://example.test/locked',
                     'status': 'requires_local_payload', 'observed_status': 'locked_excerpt', 'bundle_available': False,
                     'document': {'payload': 'references/upstream/local.snapshot.zip', 'member': 'repo-pin/SKILL.md'}}
            (root / 'references/library-index.json').write_text(json.dumps({'entries': [entry]}))
            stderr = io.StringIO()
            with mock.patch.object(library, 'ROOT', root), mock.patch.object(library.sys, 'argv', ['library.py', 'show', entry['id']]):
                with contextlib.redirect_stderr(stderr), self.assertRaises(SystemExit):
                    library.main()
            self.assertIn('local.snapshot.zip', stderr.getvalue())
            self.assertIn('false', stderr.getvalue())
            self.assertIn('locked_excerpt', stderr.getvalue())

    def test_document_hash_mismatch_is_rejected_and_own_folder_keeps_complete_tree(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, _, entry = self.fixture(root)
            own = root / 'references/own-guide'
            own.mkdir()
            (own / 'SKILL.md').write_bytes(b'full original')
            (own / 'ref.md').write_bytes(b'exact ref')
            entry = {**entry, 'document': {'file': 'references/own-guide/SKILL.md'}, 'materialize': {'folder': 'references/own-guide'}}
            (root / 'references/library-index.json').write_text(json.dumps({'entries': [entry]}))
            target = root / 'export'
            report = library.materialize_entry(root, entry, target)
            self.assertEqual((target / 'ref.md').read_bytes(), b'exact ref')
            self.assertEqual(report['files'], 2)
            with self.assertRaises(ValueError):
                library.read_entry_document(root, {**entry, 'sha256': 'b' * 64})

    def test_public_verify_reports_valid_metadata_but_missing_availability(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            report = library.verify_payload(root)
            self.assertTrue(report['verified'])
            self.assertFalse(report['ready'])
            self.assertEqual(report['payloads'][0]['status'], 'missing')
            self.assertEqual(report['sources'][0]['status'], 'missing')

    def test_lfs_fetch_and_materialize_report_restored_and_missing_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            raw = b'original media'
            oid = hashlib.sha256(raw).hexdigest()
            lfs = {'repository': 'heygen-com/hyperframes', 'commit': 'b' * 40,
                   'objects': [{'oid': oid, 'size': len(raw), 'status': 'upstream_pinned'}],
                   'paths': [{'path': 'asset one.mp4', 'oid': oid}]}
            (root / 'references/source-registry.json').write_text(json.dumps({'sources': [], 'lfs': lfs}))
            target = root / 'export/repo'
            target.mkdir(parents=True)
            pointer = ('version https://git-lfs.github.com/spec/v1\noid sha256:' + oid + '\nsize ' + str(len(raw)) + '\n').encode()
            (target / 'asset one.mp4').write_bytes(pointer)
            result = library.apply_lfs(root, {'source': lfs['repository']}, target.parent)
            self.assertEqual(result['missing'], 1)
            url = 'https://media.githubusercontent.com/media/heygen-com/hyperframes/' + 'b' * 40 + '/asset%20one.mp4'
            with mock.patch.object(library, 'urlopen', return_value=self.response(raw, url)):
                self.assertEqual(library.fetch_lfs(root)['downloaded'], 1)
            with mock.patch.object(library, 'urlopen', side_effect=AssertionError('network called')):
                self.assertEqual(library.fetch_lfs(root)['cached'], 1)
                result = library.apply_lfs(root, {'source': lfs['repository']}, target.parent)
            self.assertEqual(result['restored'], 1)
            self.assertEqual(result['missing'], 0)
            self.assertEqual((target / 'asset one.mp4').read_bytes(), raw)

    def test_published_cli_fetch_attach_show_and_materialize_end_to_end(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            raw, source, entry = self.fixture(root)
            incoming = root / 'incoming.zip'
            incoming.write_bytes(raw)
            commands = [(['fetch-source', 'owner/repo'], None),
                        (['attach-payload', 'local.snapshot.zip', '--file', str(incoming)], None),
                        (['show', entry['id'], '--output', str(root / 'export.md')], None),
                        (['materialize', entry['id'], '--destination', str(root / 'export')], None),
                        (['verify'], None)]
            for arguments, _ in commands:
                with mock.patch.object(library, 'ROOT', root), mock.patch.object(library.sys, 'argv', ['library.py'] + arguments), mock.patch.object(library, 'urlopen', return_value=self.response(raw, source['archive_url'])):
                    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                        self.assertEqual(library.main(), 0)
            self.assertEqual((root / 'export.md').read_bytes(), b'full original')
            self.assertEqual((root / 'export/repo-pin/ref.md').read_bytes(), b'full ref')
            self.assertTrue(library.verify_payload(root)['ready'])

    def test_verify_reports_corrupt_present_cache_and_rejects_raw_public_text(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            raw, _, entry = self.fixture(root)
            cache = root / 'references/.cache/repository_archives/repo-pin.zip'
            cache.parent.mkdir(parents=True)
            cache.write_bytes(raw[:-1])
            report = library.verify_payload(root)
            self.assertFalse(report['verified'])
            self.assertEqual(report['sources'][0]['status'], 'invalid')
            self.assertEqual(report['documents'][0]['status'], 'invalid')
            (root / 'references/library-index.json').write_text(json.dumps({'entries': [{**entry, 'search_text': 'raw third party content'}]}))
            with self.assertRaises(ValueError):
                library.verify_payload(root)

    def test_redirect_unknown_source_invalid_digest_and_size_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            raw, source, _ = self.fixture(root)
            with self.assertRaises(ValueError):
                library.fetch_source(root, 'unknown/repo')
            with mock.patch.object(library, 'urlopen', return_value=self.response(raw, 'https://evil.test/redirect')):
                with self.assertRaises(ValueError):
                    library.fetch_source(root, 'owner/repo')
            for size, digest in ((len(raw), 'bad'), (-1, 'a' * 64), (True, 'a' * 64)):
                with self.assertRaises(ValueError):
                    library.check_artifact(root / 'absent', size, digest)

    def test_payload_tampering_and_symlink_path_escape_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            raw, _, entry = self.fixture(root)
            attached = root / 'references/upstream/local.snapshot.zip'
            attached.write_bytes(raw)
            payload_entry = {**entry, 'document': {'payload': 'references/upstream/local.snapshot.zip', 'member': 'repo-pin/SKILL.md'}}
            self.assertEqual(library.read_entry_document(root, payload_entry), b'full original')
            attached.write_bytes(archive_bytes([('repo-pin/SKILL.md', b'altered')]))
            with self.assertRaises(ValueError):
                library.read_entry_document(root, payload_entry)
            with self.assertRaises(ValueError):
                library.rooted_path(root, '../outside')
            for value in ('NUL/file', 'dir/COM1.txt', 'file\x00.md'):
                with self.assertRaises(ValueError):
                    library.safe_name(value)

    def test_lfs_failures_keep_pointer_intact_and_metadata_is_validated(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            raw = b'media'
            oid = hashlib.sha256(raw).hexdigest()
            lfs = {'repository': 'heygen-com/hyperframes', 'commit': 'b' * 40,
                   'objects': [{'oid': oid, 'size': len(raw)}], 'paths': [{'path': 'asset.mp4', 'oid': oid}]}
            registry = root / 'references/source-registry.json'
            registry.write_text(json.dumps({'sources': [], 'lfs': lfs}))
            with mock.patch.object(library, 'urlopen', return_value=self.response(b'wrong', 'https://media.githubusercontent.com/media/heygen-com/hyperframes/' + 'b' * 40 + '/asset.mp4')):
                with self.assertRaises(ValueError):
                    library.fetch_lfs(root)
            target = root / 'export/repo'
            target.mkdir(parents=True)
            pointer = ('version https://git-lfs.github.com/spec/v1\noid sha256:' + 'a' * 64).encode()
            (target / 'asset.mp4').write_bytes(pointer)
            with self.assertRaises(ValueError):
                library.apply_lfs(root, {'source': lfs['repository']}, target.parent)
            self.assertEqual((target / 'asset.mp4').read_bytes(), pointer)
            registry.write_text(json.dumps({'sources': [], 'lfs': {**lfs, 'paths': [{'path': '../outside', 'oid': oid}]}}))
            with self.assertRaises(ValueError):
                library.fetch_lfs(root)
            with self.assertRaises(ValueError):
                library.attach_payload(root, '../local.snapshot.zip', root / 'missing.zip')

    def test_verify_counts_objects_in_valid_attached_lfs_snapshot_as_ready(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            raw = b'full media'
            oid = hashlib.sha256(raw).hexdigest()
            lfs = {'repository': 'heygen-com/hyperframes', 'commit': 'b' * 40,
                   'objects': [{'oid': oid, 'size': len(raw), 'status': 'upstream_pinned'}],
                   'paths': [{'path': 'asset.mp4', 'oid': oid}]}
            (root / 'references/source-registry.json').write_text(json.dumps({'sources': [], 'lfs': lfs}))
            snapshot_manifest = {**lfs, 'objects': [{**lfs['objects'][0], 'status': 'downloaded'}]}
            snapshot = archive_bytes([('manifest.json', json.dumps(snapshot_manifest)), ('objects/' + oid, raw)])
            (root / 'references/upstream/lfs.snapshot.zip').write_bytes(snapshot)
            manifest_path = root / 'references/upstream/payload-manifest.json'
            manifest = json.loads(manifest_path.read_text())
            manifest_path.write_text(json.dumps({'payloads': manifest['payloads'] + [
                {'payload': 'references/upstream/lfs.snapshot.zip', 'bytes': len(snapshot), 'sha256': hashlib.sha256(snapshot).hexdigest()}]}))
            (root / 'references/library-index.json').write_text(json.dumps({'entries': []}))
            report = library.verify_payload(root)
            self.assertEqual(report['lfs_objects'][0]['status'], 'ready')
            self.assertEqual(report['lfs_objects'][0]['available_from'], 'attached_lfs_snapshot')

    def test_attached_database_supplies_pinned_sources_without_extraction_or_network(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            raw, source, entry = self.fixture(root)
            member = 'original/repository_archives/' + source['archive_file']
            outer = archive_bytes([(member, raw)])
            payload = root / 'references/upstream/database.snapshot.zip'
            payload.write_bytes(outer)
            manifest = {'payloads': [{'payload': 'references/upstream/database.snapshot.zip',
                       'bytes': len(outer), 'sha256': hashlib.sha256(outer).hexdigest(),
                       'original_files': [{'member': member, 'bytes': len(raw), 'sha256': source['sha256']}]}]}
            (root / 'references/upstream/payload-manifest.json').write_text(json.dumps(manifest))
            with mock.patch.object(library, 'urlopen', side_effect=AssertionError('network called')):
                result = library.fetch_source(root, 'owner/repo')
                self.assertTrue(result['cached'])
                self.assertEqual(result['available_from'], 'attached_snapshot')
                self.assertEqual(library.read_entry_document(root, entry), b'full original')
                library.materialize_entry(root, entry, root / 'export')
                report = library.verify_payload(root)
            self.assertTrue(report['ready'])
            self.assertEqual(report['sources'][0]['available_from'], 'attached_snapshot')
            self.assertFalse((root / 'references/.cache/repository_archives').exists())
            self.assertEqual((root / 'export/repo-pin/ref.md').read_bytes(), b'full ref')
            payload.write_bytes(outer[:-1])
            with self.assertRaises(ValueError):
                library.read_entry_document(root, entry)


if __name__ == '__main__':
    unittest.main()
