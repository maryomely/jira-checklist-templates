#!/usr/bin/env python3
"""Check catalog integrity, raw template syntax, discovery links, and generated files."""
import collections
import importlib.util
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

from rebuild_indexes import generated_files

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('checklist_linter', ROOT/'skills/write-jira-checklist/scripts/lint_checklist.py')
linter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(linter)


def validate():
    errors = []
    warnings = collections.Counter()
    catalog = json.loads((ROOT/'catalog.json').read_text())
    entries = catalog['templates']
    ids = [e['id'] for e in entries]
    paths = [e['path'] for e in entries]
    if len(ids) != len(set(ids)): errors.append('Duplicate template IDs.')
    if len(paths) != len(set(paths)): errors.append('Duplicate template paths.')
    superseded = [old_id for entry in entries for old_id in entry.get('superseded_ids', [])]
    if len(superseded) != len(set(superseded)): errors.append('Superseded IDs must have one successor.')
    if set(superseded) & set(ids): errors.append('Superseded IDs must not also be active templates.')
    if any(not re.fullmatch(r'T\d{3,}', old_id) for old_id in superseded):
        errors.append('Invalid superseded template ID.')
    source_urls = {s['url'] for s in catalog['sources']}
    for entry in entries:
        required = {'id','title','team','summary','tags','kind','path','source_urls','notes','placeholders','item_count','sha256'}
        if required - entry.keys(): errors.append(f"{entry['id']}: missing metadata fields {required-entry.keys()}")
        if not re.fullmatch(r'T\d{3,}', entry['id']): errors.append(f"Invalid ID: {entry['id']}")
        path = (ROOT/entry['path']).resolve()
        if not path.is_relative_to(ROOT/'templates') or not path.is_file():
            errors.append(f"Invalid template path: {entry['path']}")
            continue
        if not entry['summary'] or not entry['tags']: errors.append(f"{entry['id']}: missing discovery metadata")
        if not set(entry['source_urls']).issubset(source_urls): errors.append(f"{entry['id']}: unregistered source")
        body = path.read_text(encoding='utf-8')
        for finding in linter.lint(body):
            if finding['severity'] == 'error':
                errors.append(f"{entry['id']}:{finding['line']} [{finding['code']}] {finding['message']}")
            elif finding['severity'] == 'warning':
                warnings[finding['code']] += 1
    actual = {str(p.relative_to(ROOT)) for p in (ROOT/'templates').rglob('*.md') if p.name != 'README.md'}
    if actual != set(paths): errors.append(f'Catalog/file mismatch: {actual.symmetric_difference(paths)}')
    for relative, expected in generated_files(catalog).items():
        file = ROOT/relative
        if not file.is_file() or file.read_text() != expected:
            errors.append(f'{relative}: stale; run scripts/rebuild_indexes.py')
    # Only prose links are navigation. Examples inside fences/inline code are payload syntax.
    for path in [*ROOT.rglob('*.md'), ROOT/'llms.txt']:
        if str(path.relative_to(ROOT)) in actual: continue
        prose = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        prose = re.sub(r'`[^`]*`', '', prose)
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', prose):
            parts = urlsplit(target)
            if parts.scheme or target.startswith('#'): continue
            destination = (path.parent/unquote(parts.path)).resolve()
            if not destination.is_relative_to(ROOT) or not destination.exists():
                errors.append(f'{path.relative_to(ROOT)}: broken local link {target}')
    return errors, warnings, len(entries)


def main():
    errors, warnings, count = validate()
    for error in errors: print('ERROR:', error)
    print(f'{count} templates checked; {len(errors)} errors.')
    if warnings: print('Review notes:', json.dumps(dict(warnings), sort_keys=True))
    return bool(errors)


if __name__ == '__main__': sys.exit(main())
