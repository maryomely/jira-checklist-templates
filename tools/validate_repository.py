#!/usr/bin/env python3
"""Check catalog integrity, raw template syntax, discovery links, and generated files."""
import collections
import importlib.util
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit
from jsonschema import Draft202012Validator, FormatChecker

from rebuild_indexes import generated_files

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('checklist_linter', ROOT/'skills/write-jira-checklist/scripts/lint_checklist.py')
linter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(linter)


def catalog_path(path, root):
    """Catalog paths use forward slashes on every operating system."""
    return path.relative_to(root).as_posix()


def validate(root=ROOT):
    root = root.resolve()
    errors = []
    warnings = collections.Counter()
    try:
        catalog = json.loads((root/'templates/catalog.json').read_text(encoding='utf-8'))
    except (OSError, UnicodeError, ValueError) as error:
        return [f'templates/catalog.json: {error}'], warnings, 0
    schema = json.loads((ROOT/'tools/catalog.schema.json').read_text(encoding='utf-8'))
    Draft202012Validator.check_schema(schema)
    for error in Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(catalog):
        location = '/'.join(str(part) for part in error.absolute_path)
        errors.append(f'templates/catalog.json/{location}: schema: {error.message}')
    if errors:
        return errors, warnings, 0
    entries = catalog['templates']
    def scan_metadata(value, location='templates/catalog.json'):
        if isinstance(value, dict):
            for key, child in value.items():
                scan_metadata(key, location + '/key')
                scan_metadata(child, location + '/' + key)
        elif isinstance(value, list):
            for index, child in enumerate(value): scan_metadata(child, location + f'/{index}')
        elif isinstance(value, str):
            for finding in linter.content_findings(value, allow_local=True):
                errors.append(f"{location}: [{finding['code']}] {finding['message']}")
    scan_metadata(catalog)
    required = {'id','title','team','summary','tags','kind','path','source_urls','notes','placeholders','item_count','sha256'}
    for index, entry in enumerate(entries):
        if required - entry.keys():
            errors.append(f"Entry {index + 1}: missing metadata fields {sorted(required-entry.keys())}")
        identifiers = entry.get('literal_identifiers', [])
        if not isinstance(identifiers, list) or any(
            not isinstance(name, str) or not linter.PLACEHOLDER.fullmatch(name) for name in identifiers
        ):
            errors.append(f"Entry {index + 1}: literal_identifiers must be a list of snake_case names.")
    if errors:
        return errors, warnings, len(entries)
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
        if not re.fullmatch(r'T\d{3,}', entry['id']): errors.append(f"Invalid ID: {entry['id']}")
        path = (root/entry['path']).resolve()
        if not path.is_relative_to(root/'templates') or not path.is_file():
            errors.append(f"Invalid template path: {entry['path']}")
            continue
        if not entry['summary'] or not entry['tags']: errors.append(f"{entry['id']}: missing discovery metadata")
        if not set(entry['source_urls']).issubset(source_urls): errors.append(f"{entry['id']}: unregistered source")
        body = path.read_text(encoding='utf-8')
        evidence = entry.get('import_validation')
        if evidence:
            import hashlib
            if evidence['template_sha256'] != hashlib.sha256(body.encode('utf-8')).hexdigest():
                errors.append(f"{entry['id']}: import-validation evidence is stale; retest or remove it.")
            report = (root/evidence['evidence']).resolve()
            if not report.is_relative_to(root/'docs') or not report.is_file():
                errors.append(f"{entry['id']}: import-validation evidence must reference an existing report in docs/.")
        for finding in linter.lint(body, allowed_identifiers=entry.get('literal_identifiers', [])):
            if finding['severity'] == 'error':
                errors.append(f"{entry['id']}:{finding['line']} [{finding['code']}] {finding['message']}")
            elif finding['severity'] == 'warning':
                warnings[finding['code']] += 1
    actual = {catalog_path(p, root) for p in (root/'templates').rglob('*.md') if p.name != 'README.md'}
    if actual != set(paths): errors.append(f'Catalog/file mismatch: {actual.symmetric_difference(paths)}')
    # Do not regenerate from missing or unsafe source paths; report the catalog errors first.
    if errors:
        return errors, warnings, len(entries)
    try:
        generated = generated_files(catalog, root=root)
    except (OSError, UnicodeError, ValueError) as error:
        return errors + [f'Cannot regenerate indexes: {error}'], warnings, len(entries)
    for relative, expected in generated.items():
        file = root/relative
        if not file.is_file() or file.read_text(encoding='utf-8') != expected:
            errors.append(f'{relative}: stale; run tools/rebuild_indexes.py')
    ignored = {'.git', '.venv', '__pycache__', 'dist'}
    text_files = [path for path in root.rglob('*') if path.is_file()
                  and path.suffix in {'.md', '.txt', '.yml', '.yaml', '.py'}
                  and not (set(path.relative_to(root).parts) & ignored)]
    # Only prose links are navigation. Examples inside fences/inline code are payload syntax.
    for path in text_files:
        if catalog_path(path, root) in actual: continue
        if not path.is_file(): continue  # Missing generated files are already reported above.
        for finding in linter.unicode_findings(path.read_text(encoding='utf-8')):
            errors.append(f"{catalog_path(path, root)}:{finding['line']} [{finding['code']}] {finding['message']}")
        if path.suffix != '.md' and path.name != 'llms.txt': continue
        prose = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
        prose = re.sub(r'`[^`]*`', '', prose)
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', prose):
            parts = urlsplit(target)
            if parts.scheme or target.startswith('#'): continue
            destination = (path.parent/unquote(parts.path)).resolve()
            if not destination.is_relative_to(root) or not destination.exists():
                errors.append(f'{path.relative_to(root)}: broken local link {target}')
    return errors, warnings, len(entries)


def main():
    errors, warnings, count = validate()
    for error in errors: print('ERROR:', error)
    print(f'{count} templates checked; {len(errors)} errors.')
    if warnings: print('Review notes:', json.dumps(dict(warnings), sort_keys=True))
    return bool(errors)


if __name__ == '__main__': sys.exit(main())
