#!/usr/bin/env python3
"""Verify real standalone ZIPs and the portable host bundle before publication."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    parts = PurePosixPath(name).parts
    require(not PurePosixPath(name).is_absolute() and '..' not in parts and '\\' not in name,
            f'Invalid archive path: {name}')
    require(not any(p in {'dist', 'node_modules', '__pycache__', '.git', '.DS_Store'} for p in parts)
            and not any(p == '.env' or p.startswith('.env.') for p in parts)
            and not name.endswith(('.pyc', '.pyo', '.tmp', '.bak', '.log')),
            f'Unexpected generated/private file: {name}')


def names_of(archive):
    names = archive.namelist()
    require(len(names) == len(set(names)), 'Duplicate ZIP entries')
    for name in names:
        safe_name(name)
    return set(names)


def check_skill(root, ident):
    source = root / ident
    package = source / 'dist' / f'{ident}.zip'
    manifest = json.loads((source / 'dist' / f'{ident}.manifest.json').read_text())
    version = json.loads((source / 'package.json').read_text())['version']
    require(manifest['name'] == ident and manifest['version'] == version, f'{ident}: manifest version/name mismatch')
    require(digest(package.read_bytes()) == manifest['sha256'], f'{ident}: ZIP checksum mismatch')
    with zipfile.ZipFile(package) as archive:
        names = names_of(archive)
        expected = {f'{ident}/{rel}' for rel in manifest['entries']}
        require(names == expected and len(names) == manifest['files'], f'{ident}: ZIP entries differ from manifest')
        required = {'SKILL.md', 'README.md', 'README.en.md', 'package.json', 'knowledge/index.json', 'scripts/knowledge.py'}
        for rel in required:
            require(f'{ident}/{rel}' in names, f'{ident}: missing required resource {rel}')
        catalog = json.loads(archive.read(f'{ident}/knowledge/index.json'))
        for card in catalog['entries']:
            require(f'{ident}/knowledge/{card["path"]}' in names, f'{ident}: missing knowledge card {card["id"]}')
        atlas = 'assets/examples/creative-atlas.html'
        if (source / atlas).exists():
            require(f'{ident}/{atlas}' in names, f'{ident}: missing visual atlas')
        for spec in (source / 'assets/title-specs').glob('*.json'):
            require(f'{ident}/assets/title-specs/{spec.name}' in names, f'{ident}: missing title specimen {spec.name}')
        for name in names:
            require(name.startswith(ident + '/'), f'{ident}: wrong ZIP root')
            original = root / name
            require(original.resolve().is_relative_to(source.resolve()), f'{ident}: source escapes skill')
            require(original.is_file() and archive.read(name) == original.read_bytes(), f'{ident}: payload differs from source: {name}')
    return len(names)


def check_host(root):
    version = json.loads((root / 'package.json').read_text())['version']
    filename = f'topmind-writing-skills-{version}.zip'
    archive_path = root / 'dist' / filename
    checksum_name = f'topmind-writing-skills-{version}.SHA256SUMS'
    checksum = (root / 'dist' / checksum_name).read_text().split()
    require(checksum == [digest(archive_path.read_bytes()), filename], 'Host checksum mismatch')
    with zipfile.ZipFile(archive_path) as archive:
        names = names_of(archive)
        manifest = json.loads(archive.read('topmind-pack.json'))
        require(manifest['version'] == version and manifest['schema_version'] == 1, 'Host manifest version mismatch')
        files = manifest['files']
        require(names == set(files) | {'topmind-pack.json', 'LICENSE'}, 'Host resources differ from manifest')
        base = {key: value for key, value in manifest.items() if key != 'digest'}
        encoded = json.dumps(base, ensure_ascii=False, separators=(',', ':')).encode()
        require(manifest['digest'] == digest(encoded), 'Host manifest digest mismatch')
        for name, sha in files.items():
            payload = archive.read(name)
            require(digest(payload) == sha and payload == (root / name).read_bytes(), f'Host payload mismatch: {name}')
        require(archive.read('LICENSE') == (root / 'LICENSE').read_bytes(), 'Host license mismatch')
    latest = json.loads((root / 'dist/latest.json').read_text())
    require(latest['version'] == version and latest['writing'] == version, 'latest.json version mismatch')
    assets = latest['assets']
    require({a['name'] for a in assets} == {filename, checksum_name}, 'latest.json assets mismatch')
    require(all(a['browser_download_url'].endswith(f'/v{version}/{a["name"]}') for a in assets), 'latest.json tag/path mismatch')
    return len(files)


def main():
    try:
        skills = sorted(p.parent.name for p in ROOT.glob('*/SKILL.md'))
        require(bool(skills), 'No skills discovered')
        for ident in skills:
            print(f'{ident}: {check_skill(ROOT, ident)} verified ZIP entries')
        print(f'Host: {check_host(ROOT)} verified resources, checksums and latest.json')
        return 0
    except (OSError, ValueError, KeyError, TypeError, zipfile.BadZipFile) as error:
        print(f'Release artifact check failed: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
