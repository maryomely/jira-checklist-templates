#!/usr/bin/env python3
"""Build a deterministic latest-only skill ZIP without creating tags or releases."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = 'skills/write-jira-checklist.zip'


def build(root=ROOT):
    skill = root/'skills/write-jira-checklist'
    files = {}
    for path in sorted(skill.rglob('*')):
        if path.is_file() and path.suffix in {'.md', '.py', '.yaml', '.json', '.txt'} and '__pycache__' not in path.parts:
            if path.is_symlink(): raise ValueError(f'Do not package symlinks: {path}')
            files[path.relative_to(skill).as_posix()] = path.read_text(encoding='utf-8').replace('\r\n', '\n').encode('utf-8')
    for name in ['LICENSE', 'NOTICE']:
        files[name] = (root/name).read_text(encoding='utf-8').replace('\r\n', '\n').encode('utf-8')
    manifest = {name: hashlib.sha256(value).hexdigest() for name, value in sorted(files.items())}
    files['manifest.json'] = (json.dumps(manifest, indent=2)+'\n').encode()
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w', compression=zipfile.ZIP_STORED) as archive:
        for name, value in sorted(files.items()):
            info = zipfile.ZipInfo('write-jira-checklist/'+name, date_time=(2020,1,1,0,0,0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, value)
    return buffer.getvalue()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    expected = build()
    path = ROOT/OUTPUT
    if args.check:
        if not path.is_file() or path.read_bytes() != expected:
            parser.exit(1, 'Skill ZIP is stale; run python tools/build_skill.py\n')
        print('Skill ZIP matches the current source.')
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(expected)
        print(f'Built {OUTPUT} ({len(expected)} bytes).')


if __name__ == '__main__': main()
