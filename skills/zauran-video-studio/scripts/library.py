"""Inspect pinned sources, attach owned payloads, and materialize without execution."""
import argparse
import hashlib
import io
import json
import os
import re
import shutil
import stat
import sys
import zipfile
import tempfile
from contextlib import contextmanager
from pathlib import Path, PurePosixPath
from urllib.parse import quote
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
MAX_SOURCE_BYTES = 133 * 1024 ** 2


def rooted_path(root, name):
    path = root / safe_name(name)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('Path is outside skill root: ' + name)
    return path


def validate_identity(repository, commit):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository) or any(part in ('.', '..') for part in repository.split('/')):
        raise ValueError('Invalid source repository identity.')
    if not re.fullmatch(r'[0-9a-f]{40}', commit):
        raise ValueError('Source must use an exact lowercase 40-character commit.')


def validate_digest(digest):
    if not isinstance(digest, str) or not re.fullmatch(r'[0-9a-f]{64}', digest):
        raise ValueError('Invalid SHA-256 identity.')


def check_artifact(path, size, digest, zip_crc=False):
    validate_digest(digest)
    if type(size) is not int or size < 0:
        raise ValueError('Invalid declared artifact size.')
    if not path.is_file() or path.stat().st_size != size:
        raise ValueError(str(path) + ': missing or size mismatch')
    hasher = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(1024 * 1024):
            hasher.update(chunk)
    if hasher.hexdigest() != digest:
        raise ValueError(str(path) + ': SHA-256 mismatch')
    if zip_crc:
        try:
            with zipfile.ZipFile(path) as archive:
                if archive.testzip():
                    raise ValueError(str(path) + ': ZIP CRC failure')
        except zipfile.BadZipFile as error:
            raise ValueError(str(path) + ': invalid ZIP or CRC failure') from error


def source_record(root, repository):
    sources = read_json(root / 'references/source-registry.json')['sources']
    matches = [item for item in sources if item['repository'] == repository]
    if len(matches) != 1:
        raise ValueError('Unknown or duplicate source repository: ' + repository)
    item = matches[0]
    validate_identity(item['repository'], item['commit'])
    expected = 'https://codeload.github.com/' + repository + '/zip/' + item['commit']
    if item['archive_url'] != expected:
        raise ValueError('Source URL must be the exact pinned GitHub codeload URL.')
    name = safe_name(item['archive_file'])
    if len(name.parts) != 1 or not item['archive_file'].endswith('.zip'):
        raise ValueError('Archive filename must be a ZIP basename.')
    if type(item['bytes']) is not int or not 0 < item['bytes'] <= MAX_SOURCE_BYTES:
        raise ValueError('Source archive exceeds its allowed size bound.')
    validate_digest(item['sha256'])
    return item


def source_path(root, item):
    return rooted_path(root, 'references/.cache/repository_archives/' + item['archive_file'])


def attached_source(root, item):
    manifest = read_json(root / 'references/upstream/payload-manifest.json')
    suffix = '/repository_archives/' + item['archive_file']
    matches = [(payload, record) for payload in manifest['payloads']
               for record in payload.get('original_files', [])
               if record['member'].endswith(suffix) and rooted_path(root, payload['payload']).is_file()]
    if len(matches) > 1:
        raise ValueError('Duplicate attached repository archive.')
    if not matches:
        return None
    payload, record = matches[0]
    safe_name(record['member'])
    if record['sha256'] != item['sha256'] or record['bytes'] != item['bytes']:
        raise ValueError('Attached repository differs from pinned source identity.')
    return payload, record


@contextmanager
def repository_archive(root, item, verified=False):
    path = source_path(root, item)
    if path.is_file():
        if not verified:
            check_artifact(path, item['bytes'], item['sha256'], True)
        with zipfile.ZipFile(path) as archive:
            yield archive
        return
    attached = attached_source(root, item)
    if not attached:
        raise ValueError('Missing source archive: ' + str(path) + '. Run fetch-source ' + item['repository'] + ' or attach the owned database snapshot.')
    payload, record = attached
    path = rooted_path(root, payload['payload'])
    if not verified:
        check_artifact(path, payload['bytes'], payload['sha256'], True)
    with zipfile.ZipFile(path) as outer:
        if outer.getinfo(record['member']).file_size != item['bytes']:
            raise ValueError('Attached source archive size differs from pinned source.')
        raw = outer.read(record['member'])
    if not verified and hashlib.sha256(raw).hexdigest() != item['sha256']:
        raise ValueError('Attached source archive failed SHA-256 verification.')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        if not verified and archive.testzip():
            raise ValueError('Attached source archive failed ZIP CRC verification.')
        yield archive


def atomic_copy(stream, destination, size, digest, zip_crc=False):
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=destination.name + '.', suffix='.part', dir=destination.parent)
    temporary = Path(temporary)
    try:
        with os.fdopen(descriptor, 'wb') as output:
            total = 0
            while chunk := stream.read(min(1024 * 1024, size - total + 1)):
                total += len(chunk)
                if total > size:
                    raise ValueError('Download exceeds declared exact byte size.')
                output.write(chunk)
        check_artifact(temporary, size, digest, zip_crc)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def download_artifact(url, destination, size, digest, zip_crc=False):
    try:
        check_artifact(destination, size, digest, zip_crc)
        return True
    except ValueError:
        pass
    with urlopen(url, timeout=60) as response:
        if response.geturl() != url:
            raise ValueError('Unexpected download redirect; pinned URL required.')
        atomic_copy(response, destination, size, digest, zip_crc)
    return False


def fetch_source(root, repository):
    item = source_record(root, repository)
    path = source_path(root, item)
    if not path.is_file() and attached_source(root, item):
        with repository_archive(root, item):
            payload, record = attached_source(root, item)
            return {'source': repository, 'path': str(rooted_path(root, payload['payload'])),
                    'member': record['member'], 'cached': True, 'verified': True, 'available_from': 'attached_snapshot'}
    cached = download_artifact(item['archive_url'], path, item['bytes'], item['sha256'], True)
    return {'source': repository, 'path': str(path), 'cached': cached, 'verified': True}


def attach_payload(root, basename, incoming):
    if safe_name(basename).name != basename:
        raise ValueError('Payload must be a manifest basename.')
    manifest = read_json(root / 'references/upstream/payload-manifest.json')
    matches = [item for item in manifest['payloads'] if PurePosixPath(item['payload']).name == basename]
    if len(matches) != 1:
        raise ValueError('Unknown or duplicate payload basename: ' + basename)
    item = matches[0]
    destination = rooted_path(root, item['payload'])
    check_artifact(incoming, item['bytes'], item['sha256'], True)
    if incoming.resolve() != destination.resolve():
        with incoming.open('rb') as stream:
            atomic_copy(stream, destination, item['bytes'], item['sha256'], True)
    return {'payload': item['payload'], 'path': str(destination), 'verified': True}


def lfs_metadata(root):
    registry = read_json(root / 'references/source-registry.json')
    lfs = registry.get('lfs')
    if not lfs:
        return None
    validate_identity(lfs['repository'], lfs['commit'])
    oids = [item['oid'] for item in lfs['objects']]
    if len(oids) != len(set(oids)):
        raise ValueError('Duplicate LFS object identity.')
    for item in lfs['objects']:
        validate_digest(item['oid'])
        if type(item['size']) is not int or not 0 <= item['size'] <= 4 * 1024 ** 3:
            raise ValueError('Invalid LFS object size.')
    for item in lfs['paths']:
        safe_name(item['path'])
        if item['oid'] not in oids:
            raise ValueError('LFS path has no declared object.')
    return lfs


def fetch_lfs(root, source='heygen-com/hyperframes'):
    lfs = lfs_metadata(root)
    if not lfs or source != lfs['repository']:
        raise ValueError('Unknown LFS source: ' + source)
    cached = downloaded = 0
    for item in lfs['objects']:
        matching = next((path['path'] for path in lfs['paths'] if path['oid'] == item['oid']), None)
        if matching is None:
            raise ValueError('LFS object has no retrieval path.')
        url = 'https://media.githubusercontent.com/media/' + source + '/' + lfs['commit'] + '/' + quote(matching, safe='/')
        path = rooted_path(root, 'references/.cache/lfs/objects/' + item['oid'])
        reused = download_artifact(url, path, item['size'], item['oid'])
        cached += int(reused)
        downloaded += int(not reused)
    return {'source': source, 'cached': cached, 'downloaded': downloaded, 'verified': True}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))


def check_destination(destination):
    target = destination.resolve()
    pairs = [tuple(p.lower() for p in target.parts[i:i + 2]) for i in range(len(target.parts) - 1)]
    if any(pair in {('.codex', 'skills'), ('.agents', 'skills'), ('.claude', 'skills')} for pair in pairs):
        raise ValueError('Materialize outside automatically discovered skill directories.')
    if target.exists():
        raise ValueError('Destination must be a new directory; existing files are preserved.')
    return target


def safe_name(name):
    if not isinstance(name, str) or '\x00' in name:
        raise ValueError('Unsupported path name.')
    path = PurePosixPath(name)
    if path.is_absolute() or '\\' in name or ':' in name or '..' in path.parts:
        raise ValueError('Unsafe archive path: ' + name)
    if not path.parts or any(part.rstrip(' .') != part for part in path.parts):
        raise ValueError('Unsupported archive path: ' + name)
    if any(re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part, re.IGNORECASE)
           or any(character in part for character in '<>"|?*') for part in path.parts):
        raise ValueError('Unsupported Windows archive path: ' + name)
    return Path(*path.parts)


def safe_extract(archive, destination, prefix=None):
    target = check_destination(destination)
    if prefix:
        prefix = safe_name(prefix).as_posix().rstrip('/') + '/'
    selected = [item for item in archive.infolist() if not prefix or item.filename.startswith(prefix)]
    if not selected:
        raise ValueError('Requested source folder is absent from the snapshot.')
    planned = [(item, safe_name(item.filename)) for item in selected]
    names = [str(path).casefold() for _, path in planned]
    if len(names) != len(set(names)):
        raise ValueError('Archive paths collide on a case-insensitive filesystem.')
    if sum(item.file_size for item, _ in planned) > 4 * 1024 ** 3:
        raise ValueError('Source exceeds the 4 GiB extraction bound.')
    links = []
    target.mkdir(parents=True)
    files = 0
    for item, relative in planned:
        output = target / relative
        mode = item.external_attr >> 16
        if stat.S_ISLNK(mode):
            links.append({'path': item.filename, 'target': archive.read(item).decode('utf-8', errors='replace')})
        elif item.is_dir():
            output.mkdir(parents=True, exist_ok=True)
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(item) as source, output.open('xb') as file:
                while chunk := source.read(1024 * 1024):
                    file.write(chunk)
            if mode & stat.S_IXUSR and sys.platform != 'win32':
                output.chmod(output.stat().st_mode | stat.S_IXUSR)
            files += 1
    return {'destination': str(target), 'files': files, 'skipped_links': links,
            'note': 'Symlinks are preserved in the original archive, listed here and never followed. Dependencies are not installed.'}


@contextmanager
def open_archive(root, location, verified=False):
    if 'source_archive' in location:
        item = source_record(root, location['source_archive'])
        with repository_archive(root, item, verified) as archive:
            yield archive
        return
    payload = rooted_path(root, location['payload'])
    if not payload.is_file():
        raise ValueError('Missing local payload: ' + location['payload'] + '. Attach the already-owned archive with attach-payload ' + payload.name + ' --file <existingzip>.')
    if not verified and (root / 'references/source-registry.json').is_file():
        manifest = read_json(root / 'references/upstream/payload-manifest.json')
        matches = [item for item in manifest['payloads'] if item['payload'] == location['payload']]
        if len(matches) != 1:
            raise ValueError('Payload is absent from pinned manifest: ' + location['payload'])
        item = matches[0]
        check_artifact(payload, item['bytes'], item['sha256'], True)
    with zipfile.ZipFile(payload) as outer:
        if location.get('container'):
            with zipfile.ZipFile(io.BytesIO(outer.read(location['container']))) as nested:
                yield nested
        else:
            yield outer


def read_document(root, location, verified=False):
    if 'file' in location:
        return rooted_path(root, location['file']).read_bytes()
    safe_name(location['member'])
    with open_archive(root, location, verified) as archive:
        return archive.read(location['member'])


def read_entry_document(root, entry, verified=False):
    raw = read_document(root, entry['document'], verified)
    if 'sha256' in entry:
        validate_digest(entry['sha256'])
        if hashlib.sha256(raw).hexdigest() != entry['sha256']:
            raise ValueError('Document failed SHA-256 verification: ' + entry['id'])
    elif 'source_archive' in entry['document'] or 'file' in entry['document']:
        raise ValueError('Missing full document hash: ' + entry['id'])
    return raw


def copy_folder(root, folder, destination):
    source = rooted_path(root, folder)
    if not source.is_dir():
        raise ValueError('Missing own guide folder: ' + folder)
    planned = [(path, path.relative_to(source)) for path in source.rglob('*')]
    links = [{'path': relative.as_posix(), 'target': os.readlink(path)} for path, relative in planned if path.is_symlink()]
    for _, relative in planned:
        safe_name(relative.as_posix())
    destination.mkdir(parents=True)
    files = 0
    for path, relative in planned:
        if path.is_symlink():
            continue
        output = destination / relative
        if path.is_dir():
            output.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            output.parent.mkdir(parents=True, exist_ok=True)
            with path.open('rb') as incoming, output.open('xb') as outgoing:
                shutil.copyfileobj(incoming, outgoing)
            files += 1
    return {'destination': str(destination), 'files': files, 'skipped_links': links}


def materialize_entry(root, entry, destination):
    target = check_destination(destination)
    read_entry_document(root, entry)
    location = entry['materialize']
    if 'folder' in location:
        report = copy_folder(root, location['folder'], target)
    else:
        with open_archive(root, location) as archive:
            report = safe_extract(archive, target, prefix=location.get('prefix'))
    return {**report, 'lfs': apply_lfs(root, entry, target), 'source_status': entry['status'],
            'source': entry['source'], **({'bundle_available': entry['bundle_available'],
             'content_scope': 'available_document_snapshot'} if entry['kind'] == 'skillry_skill' else {})}


def find_entry(entries, identity):
    matches = [entry for entry in entries if entry['id'] == identity]
    if len(matches) != 1:
        raise ValueError('Unknown document ID; use search/list to find the exact qualified ID.')
    return matches[0]


def apply_lfs(root, entry, target):
    supplement = root / 'references/upstream/lfs.snapshot.zip'
    if entry.get('source') != 'heygen-com/hyperframes':
        return {'restored': 0, 'missing': 0}
    with contextmanager_lfs(root, supplement) as (manifest, archive):
        if not manifest:
            return {'restored': 0, 'missing': 0, 'note': 'No LFS metadata is available.'}
        restored = missing = present = 0
        for item in manifest.get('paths', []):
            relative = safe_name(item['path'])
            obj = next((obj for obj in manifest['objects'] if obj['oid'] == item['oid']), None)
            matches = [parent / relative for parent in target.iterdir() if parent.is_dir() and (parent / relative).is_file()]
            if len(matches) != 1:
                missing += 1
                continue
            output = matches[0]
            if not output.resolve().is_relative_to(target.resolve()):
                raise ValueError('LFS output escapes materialized tree.')
            pointer = output.read_bytes()
            if b'version https://git-lfs.github.com/spec/v1' not in pointer[:200]:
                if obj:
                    check_artifact(output, obj['size'], item['oid'])
                    present += 1
                continue
            if ('oid sha256:' + item['oid']).encode('ascii') not in pointer:
                raise ValueError('LFS pointer identity differs from supplement manifest.')
            cache = rooted_path(root, 'references/.cache/lfs/objects/' + item['oid'])
            if obj and cache.is_file():
                check_artifact(cache, obj['size'], item['oid'])
                with cache.open('rb') as stream:
                    atomic_copy(stream, output, obj['size'], item['oid'])
            elif archive and obj and obj.get('status') == 'downloaded':
                with archive.open('objects/' + item['oid']) as stream:
                    atomic_copy(stream, output, obj['size'], item['oid'])
            else:
                missing += 1
                continue
            restored += 1
    return {'restored': restored, 'missing': missing, 'already_present': present,
            'note': 'Original source archive pointers remain unchanged. Run fetch-lfs explicitly for missing objects.'}


@contextmanager
def contextmanager_lfs(root, supplement):
    if supplement.is_file():
        with zipfile.ZipFile(supplement) as archive:
            yield json.loads(archive.read('manifest.json')), archive
    elif (root / 'references/source-registry.json').is_file():
        yield lfs_metadata(root), None
    else:
        yield None, None


def verify_legacy_payload(root):
    manifest = read_json(root / 'references/upstream/payload-manifest.json')
    errors = []
    for item in manifest['payloads']:
        path = root / safe_name(item['payload'])
        if not path.is_file() or path.stat().st_size != item['bytes']:
            errors.append(item['payload'] + ': missing or size mismatch')
            continue
        if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
            errors.append(item['payload'] + ': SHA-256 mismatch')
            continue
        with zipfile.ZipFile(path) as archive:
            if archive.testzip():
                errors.append(item['payload'] + ': ZIP CRC failure')
            for record in item.get('original_files', []):
                if hashlib.sha256(archive.read(record['member'])).hexdigest() != record['sha256']:
                    errors.append(record['member'] + ': original bytes changed')
    return {'verified': not errors, 'payload_count': len(manifest['payloads']), 'errors': errors}


def artifact_state(path, size, digest, zip_crc=False):
    validate_digest(digest)
    if type(size) is not int or size < 0:
        raise ValueError('Invalid artifact size.')
    if not path.is_file():
        return {'path': str(path), 'status': 'missing'}
    try:
        check_artifact(path, size, digest, zip_crc)
        return {'path': str(path), 'status': 'ready'}
    except (ValueError, OSError, zipfile.BadZipFile) as error:
        return {'path': str(path), 'status': 'invalid', 'error': str(error)}


def lfs_object_states(root, lfs, payloads):
    objects = []
    supplement = root / 'references/upstream/lfs.snapshot.zip'
    attached = any(item['payload'] == 'references/upstream/lfs.snapshot.zip' and item['status'] == 'ready' for item in payloads)
    with contextmanager_lfs(root, supplement if attached else root / 'references/.cache/absent-lfs-supplement') as (manifest, archive):
        for item in lfs['objects']:
            path = rooted_path(root, 'references/.cache/lfs/objects/' + item['oid'])
            state = {'oid': item['oid'], **artifact_state(path, item['size'], item['oid'])}
            if state['status'] == 'missing' and archive:
                obj = next((obj for obj in manifest['objects'] if obj['oid'] == item['oid']), None)
                if obj and obj.get('status') == 'downloaded':
                    try:
                        raw = archive.read('objects/' + item['oid'])
                        if len(raw) != item['size'] or hashlib.sha256(raw).hexdigest() != item['oid']:
                            raise ValueError('Attached LFS object failed size/SHA-256 verification.')
                        state = {**state, 'status': 'ready', 'available_from': 'attached_lfs_snapshot'}
                    except (KeyError, ValueError, zipfile.BadZipFile) as error:
                        state = {**state, 'status': 'invalid', 'error': str(error)}
            objects.append(state)
    return objects


def document_states(root, entries, artifacts):
    documents = []
    for entry in entries:
        if 'search_text' in entry or 'description' in entry:
            raise ValueError('Public index contains raw description/search text: ' + entry['id'])
        if 'sha256' in entry:
            validate_digest(entry['sha256'])
        elif 'source_archive' in entry['document'] or 'file' in entry['document']:
            raise ValueError('Missing full document hash: ' + entry['id'])
        location = entry['document']
        if 'file' in location:
            path = rooted_path(root, location['file'])
        elif 'source_archive' in location:
            path = source_path(root, source_record(root, location['source_archive']))
            safe_name(location['member'])
        else:
            path = rooted_path(root, location['payload'])
            safe_name(location['member'])
            if 'container' in location:
                safe_name(location['container'])
        scope = entry['materialize']
        if 'folder' in scope:
            rooted_path(root, scope['folder'])
        elif 'source_archive' in scope:
            source_record(root, scope['source_archive'])
        else:
            rooted_path(root, scope['payload'])
            if scope.get('prefix'):
                safe_name(scope['prefix'])
        state = {'id': entry['id'], 'status': 'missing'}
        source_state = next((item for item in artifacts if item.get('repository') == location.get('source_archive')), None) if 'source_archive' in location else None
        if path.is_file() or (source_state and source_state['status'] != 'missing'):
            try:
                prior = source_state or next((item for item in artifacts if item['path'] == str(path)), None)
                if prior and prior['status'] == 'invalid':
                    raise ValueError(prior['error'])
                read_entry_document(root, entry, verified=bool(prior and prior['status'] == 'ready'))
                state = {**state, 'status': 'ready'}
            except (ValueError, OSError, KeyError, zipfile.BadZipFile) as error:
                state = {**state, 'status': 'invalid', 'error': str(error)}
        documents.append(state)
    return documents


def verify_payload(root):
    if not (root / 'references/source-registry.json').is_file():
        return verify_legacy_payload(root)
    manifest = read_json(root / 'references/upstream/payload-manifest.json')
    registry = read_json(root / 'references/source-registry.json')
    entries = read_json(root / 'references/library-index.json')['entries']
    identities = [entry['id'] for entry in entries]
    if len(identities) != len(set(identities)):
        raise ValueError('Duplicate document IDs.')
    payloads = []
    for item in manifest['payloads']:
        path = rooted_path(root, item['payload'])
        state = {'payload': item['payload'], **artifact_state(path, item['bytes'], item['sha256'], True)}
        if state['status'] == 'ready':
            with zipfile.ZipFile(path) as archive:
                for record in item.get('original_files', []):
                    safe_name(record['member'])
                    validate_digest(record['sha256'])
                    if hashlib.sha256(archive.read(record['member'])).hexdigest() != record['sha256']:
                        state = {**state, 'status': 'invalid', 'error': record['member'] + ': original bytes changed'}
        payloads.append(state)
    sources = []
    for record in registry['sources']:
        item = source_record(root, record['repository'])
        state = artifact_state(source_path(root, item), item['bytes'], item['sha256'], True)
        attached = attached_source(root, item) if state['status'] == 'missing' else None
        if attached:
            payload, _ = attached
            original = next(record for record in payloads if record['payload'] == payload['payload'])
            state = {**original, 'available_from': 'attached_snapshot'}
        sources.append({'repository': item['repository'], **state})
    lfs = lfs_metadata(root)
    objects = lfs_object_states(root, lfs, payloads) if lfs else []
    documents = document_states(root, entries, payloads + sources)
    states = payloads + sources + objects + documents
    errors = [item['error'] for item in states if item['status'] == 'invalid']
    missing = sum(item['status'] == 'missing' for item in states)
    return {'verified': not errors, 'ready': not errors and not missing, 'missing_count': missing,
            'payload_count': len(payloads), 'payloads': payloads, 'sources': sources,
            'lfs_objects': objects, 'documents': documents, 'errors': errors,
            'note': 'verified checks public metadata and present artifacts; ready additionally requires every listed artifact.'}


def build_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    listing = sub.add_parser('list')
    listing.add_argument('--kind')
    searching = sub.add_parser('search')
    searching.add_argument('query')
    showing = sub.add_parser('show')
    showing.add_argument('id')
    showing.add_argument('--output', type=Path)
    materializing = sub.add_parser('materialize')
    materializing.add_argument('id')
    materializing.add_argument('--destination', required=True, type=Path)
    sub.add_parser('verify')
    fetching = sub.add_parser('fetch-source')
    fetching.add_argument('repository')
    lfs_fetching = sub.add_parser('fetch-lfs')
    lfs_fetching.add_argument('--source', default='heygen-com/hyperframes')
    attaching = sub.add_parser('attach-payload')
    attaching.add_argument('payload')
    attaching.add_argument('--file', required=True, type=Path)
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        if args.command == 'verify':
            report = verify_payload(ROOT)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0 if report['verified'] else 1
        if args.command in ('fetch-source', 'fetch-lfs', 'attach-payload'):
            if args.command == 'fetch-source':
                report = fetch_source(ROOT, args.repository)
            elif args.command == 'fetch-lfs':
                report = fetch_lfs(ROOT, args.source)
            else:
                report = attach_payload(ROOT, args.payload, args.file)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            return 0
        entries = read_json(ROOT / 'references/library-index.json')['entries']
        if args.command in ('search', 'list'):
            selected = [entry for entry in entries if (
                args.command == 'search' and args.query.casefold() in json.dumps(entry, ensure_ascii=False).casefold()
            ) or (args.command == 'list' and (not args.kind or entry['kind'] == args.kind))]
            for entry in selected:
                print(json.dumps({k: entry.get(k) for k in ('id', 'title', 'kind', 'source', 'status')}, ensure_ascii=False))
            print(str(len(selected)) + ' records', file=sys.stderr)
        elif args.command == 'show':
            entry = find_entry(entries, args.id)
            info = {k: entry.get(k) for k in ('id', 'source', 'status', 'observed_status', 'bundle_available')}
            if entry['kind'] == 'skillry_skill':
                info['note'] = 'Saved document availability depends on its local payload. A missing upstream bundle is not included.'
            print(json.dumps(info, ensure_ascii=False), file=sys.stderr)
            raw = read_entry_document(ROOT, entry)
            if args.output:
                with args.output.open('xb') as output:
                    output.write(raw)
            else:
                sys.stdout.buffer.write(raw)
        else:
            entry = find_entry(entries, args.id)
            print(json.dumps({k: entry.get(k) for k in ('id', 'source', 'status', 'observed_status', 'bundle_available')}, ensure_ascii=False), file=sys.stderr)
            report = materialize_entry(ROOT, entry, args.destination)
            print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, KeyError, zipfile.BadZipFile) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())
