import importlib.util
import hashlib
import io
import contextlib
import json
import tempfile
import unittest
from unittest import mock
import zipfile
from pathlib import Path

MODULE = Path(__file__).resolve().parents[1] / 'library.py'
spec = importlib.util.spec_from_file_location('unified_library', MODULE)
library = importlib.util.module_from_spec(spec)
spec.loader.exec_module(library)

def archive_bytes(entries):
    data = io.BytesIO()
    with zipfile.ZipFile(data, 'w') as archive:
        for name, content in entries:
            archive.writestr(name, content)
    return data.getvalue()

class LibraryTests(unittest.TestCase):
    def fixture(self, root):
        raw = archive_bytes([('repo/SKILL.md', b'complete original'), ('repo/references/ref.md', b'full ref')])
        (root / 'payload.zip').write_bytes(raw)
        refs = root / 'references'
        (refs / 'upstream').mkdir(parents=True)
        entry = {'id': 'repo:fixture:SKILL.md', 'kind': 'repository_skill', 'title': 'Fixture',
                 'source': 'fixture', 'status': 'full',
                 'document': {'payload': 'payload.zip', 'member': 'repo/SKILL.md'},
                 'materialize': {'payload': 'payload.zip'}}
        (refs / 'library-index.json').write_text(json.dumps({'entries': [entry]}))
        record = {'payload': 'payload.zip', 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest(),
                  'original_files': [{'member': 'repo/SKILL.md', 'sha256': hashlib.sha256(b'complete original').hexdigest()}]}
        (refs / 'upstream/payload-manifest.json').write_text(json.dumps({'payloads': [record]}))
        return entry

    def test_traversal_is_rejected_before_any_file_is_written(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / 'new'
            data = archive_bytes([('safe.txt', b'yes'), ('../escape.txt', b'no')])
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                with self.assertRaises(ValueError):
                    library.safe_extract(archive, destination)
            self.assertFalse(destination.exists())

    def test_absolute_windows_paths_are_rejected(self):
        for name in ('/abs.txt', 'C:/abs.txt', '..\\escape.txt'):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp:
                with zipfile.ZipFile(io.BytesIO(archive_bytes([(name, b'x')]))) as archive:
                    with self.assertRaises(ValueError):
                        library.safe_extract(archive, Path(temp) / 'new')

    def test_relative_reference_layout_and_original_bytes_survive(self):
        entries = [('repo/skills/a/SKILL.md', b'../refs/test.md\r\n'), ('repo/skills/refs/test.md', b'full\x00data')]
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / 'new'
            with zipfile.ZipFile(io.BytesIO(archive_bytes(entries))) as archive:
                report = library.safe_extract(archive, destination)
            self.assertEqual(report['files'], 2)
            for path, raw in entries:
                self.assertEqual((destination / path).read_bytes(), raw)

    def test_existing_destination_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp)
            with zipfile.ZipFile(io.BytesIO(archive_bytes([('x', b'x')]))) as archive:
                with self.assertRaises(ValueError):
                    library.safe_extract(archive, destination)

    def test_symlink_payload_is_reported_without_following_it(self):
        data = io.BytesIO()
        with zipfile.ZipFile(data, 'w') as archive:
            link = zipfile.ZipInfo('repo/node_modules')
            link.create_system = 3
            link.external_attr = (0o120777 << 16)
            archive.writestr(link, '/private/author/machine')
            archive.writestr('repo/file.txt', b'ok')
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / 'new'
            with zipfile.ZipFile(io.BytesIO(data.getvalue())) as archive:
                report = library.safe_extract(archive, destination)
            self.assertEqual(report['skipped_links'][0]['target'], '/private/author/machine')
            self.assertFalse((destination / 'repo/node_modules').exists())
            self.assertEqual((destination / 'repo/file.txt').read_bytes(), b'ok')

    def test_nested_source_is_read_without_altering_document(self):
        raw = b'---\r\nname: original\r\n---\r\ncomplete text\r\n'
        nested = archive_bytes([('repo/SKILL.md', raw)])
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'payload.zip').write_bytes(archive_bytes([('sources/repo.zip', nested)]))
            location = {'payload': 'payload.zip', 'container': 'sources/repo.zip', 'member': 'repo/SKILL.md'}
            self.assertEqual(library.read_document(root, location), raw)

    def test_materialization_into_skill_discovery_roots_is_rejected(self):
        for suffix in ('.codex/skills/new', '.agents/skills/new', '.claude/skills/new'):
            with self.assertRaises(ValueError):
                library.check_destination(Path(tempfile.gettempdir()) / suffix)

    def test_duplicate_normalized_paths_are_rejected(self):
        data = archive_bytes([('A.txt', b'a'), ('a.txt', b'b')])
        with tempfile.TemporaryDirectory() as temp:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                with self.assertRaises(ValueError):
                    library.safe_extract(archive, Path(temp) / 'new')

    def test_lfs_restores_exact_asset_and_preserves_archived_pointer(self):
        raw = b'original binary media\x00\x01'
        oid = hashlib.sha256(raw).hexdigest()
        pointer = ('version https://git-lfs.github.com/spec/v1\noid sha256:' + oid + '\nsize ' + str(len(raw)) + '\n').encode()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'skill'
            up = root / 'references/upstream'
            up.mkdir(parents=True)
            target = Path(temp) / 'work/repo'
            target.mkdir(parents=True)
            (target / 'asset.mp4').write_bytes(pointer)
            manifest = {'paths': [{'path': 'asset.mp4', 'oid': oid}],
                        'objects': [{'oid': oid, 'status': 'downloaded', 'size': len(raw)}]}
            archive_raw = archive_bytes([('manifest.json', json.dumps(manifest)), ('objects/' + oid, raw)])
            (up / 'lfs.snapshot.zip').write_bytes(archive_raw)
            result = library.apply_lfs(root, {'source': 'heygen-com/hyperframes'}, target.parent)
            self.assertEqual(result['restored'], 1)
            self.assertEqual((target / 'asset.mp4').read_bytes(), raw)
            self.assertEqual((up / 'lfs.snapshot.zip').read_bytes(), archive_raw)

    def test_lfs_path_cannot_escape_materialized_tree(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'skill'
            up = root / 'references/upstream'
            up.mkdir(parents=True)
            target = Path(temp) / 'work'
            target.mkdir()
            manifest = {'paths': [{'path': '../secret', 'oid': 'fake'}],
                        'objects': [{'oid': 'fake', 'status': 'downloaded'}]}
            (up / 'lfs.snapshot.zip').write_bytes(archive_bytes([('manifest.json', json.dumps(manifest))]))
            with self.assertRaises(ValueError):
                library.apply_lfs(root, {'source': 'heygen-com/hyperframes'}, target)

    def test_cli_search_and_list_locate_source_identity(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            for args in (['search', 'Fixture'], ['list', '--kind', 'repository_skill']):
                with mock.patch.object(library, 'ROOT', root), mock.patch.object(library.sys, 'argv', ['library.py'] + args):
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
                        self.assertEqual(library.main(), 0)
                    self.assertIn('repo:fixture:SKILL.md', output.getvalue())

    def test_cli_show_exports_complete_original_document(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            output = root / 'copy.md'
            with mock.patch.object(library, 'ROOT', root), mock.patch.object(library.sys, 'argv', ['library.py', 'show', 'repo:fixture:SKILL.md', '--output', str(output)]):
                self.assertEqual(library.main(), 0)
            self.assertEqual(output.read_bytes(), b'complete original')

    def test_cli_materializes_references_without_running_source(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            destination = root / 'project/vendor'
            with mock.patch.object(library, 'ROOT', root), mock.patch.object(library.sys, 'argv', ['library.py', 'materialize', 'repo:fixture:SKILL.md', '--destination', str(destination)]):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(library.main(), 0)
            self.assertEqual((destination / 'repo/references/ref.md').read_bytes(), b'full ref')

    def test_integrity_verification_reports_changed_and_missing_payload(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            self.assertTrue(library.verify_payload(root)['verified'])
            data = (root / 'payload.zip').read_bytes()
            (root / 'payload.zip').write_bytes(data[:-1] + b'Z')
            self.assertFalse(library.verify_payload(root)['verified'])
            (root / 'payload.zip').unlink()
            self.assertFalse(library.verify_payload(root)['verified'])

    def test_cli_verify_and_unknown_id_have_truthful_exit_codes(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.fixture(root)
            with mock.patch.object(library, 'ROOT', root), mock.patch.object(library.sys, 'argv', ['library.py', 'verify']):
                with contextlib.redirect_stdout(io.StringIO()):
                    self.assertEqual(library.main(), 0)
            with mock.patch.object(library, 'ROOT', root), mock.patch.object(library.sys, 'argv', ['library.py', 'show', 'missing']):
                with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as raised:
                    library.main()
                self.assertEqual(raised.exception.code, 1)

    def test_materialization_prefix_preserves_only_available_source_documents(self):
        entries = [('database/skill/a/PREVIEW.md', b'original preview'),
                   ('database/skill/a/page.json', b'original metadata'),
                   ('database/skill/b/SKILL.md', b'unrelated')]
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / 'new'
            with zipfile.ZipFile(io.BytesIO(archive_bytes(entries))) as archive:
                report = library.safe_extract(archive, destination, prefix='database/skill/a/')
            self.assertEqual(report['files'], 2)
            self.assertEqual((destination / entries[0][0]).read_bytes(), entries[0][1])
            self.assertFalse((destination / entries[2][0]).exists())

    def test_unknown_or_unsafe_prefix_is_rejected_before_writes(self):
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / 'new'
            for prefix in ('../escape/', 'missing/'):
                with zipfile.ZipFile(io.BytesIO(archive_bytes([('a.txt', b'a')]))) as archive:
                    with self.assertRaises(ValueError):
                        library.safe_extract(archive, destination, prefix=prefix)
            self.assertFalse(destination.exists())

    def test_locked_document_export_keeps_raw_bytes_and_discloses_access_status(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            entry = {**self.fixture(root), 'kind': 'skillry_skill', 'status': 'locked_excerpt',
                     'bundle_available': False, 'source': 'https://example.test/locked'}
            (root / 'references/library-index.json').write_text(json.dumps({'entries': [entry]}))
            output = root / 'copy.md'
            error = io.StringIO()
            with mock.patch.object(library, 'ROOT', root), mock.patch.object(library.sys, 'argv', ['library.py', 'show', entry['id'], '--output', str(output)]):
                with contextlib.redirect_stderr(error):
                    self.assertEqual(library.main(), 0)
            self.assertEqual(output.read_bytes(), b'complete original')
            self.assertIn('locked_excerpt', error.getvalue())
            self.assertIn('false', error.getvalue())
            self.assertIn(entry['source'], error.getvalue())

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(LibraryTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
