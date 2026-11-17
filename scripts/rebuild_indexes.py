#!/usr/bin/env python3
"""Regenerate discovery files from catalog metadata and canonical raw templates."""
import collections
import hashlib
import importlib.util
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('checklist_placeholders', ROOT/'skills/write-jira-checklist/scripts/lint_checklist.py')
placeholder_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(placeholder_module)


def generated_files(catalog):
    groups = collections.defaultdict(list)
    files = {}
    for entry in catalog['templates']:
        content = (ROOT / entry['path']).read_text(encoding='utf-8')
        entry['placeholders'] = sorted(set(placeholder_module.find_placeholders(content)))
        entry['item_count'] = len(re.findall(r'^[-+~x]!? ', content, re.M))
        entry['sha256'] = hashlib.sha256(content.encode()).hexdigest()
        groups[entry['team']].append(entry)
    catalog['template_count'] = len(catalog['templates'])
    catalog['team_count'] = len(groups)
    files['catalog.json'] = json.dumps(catalog, ensure_ascii=False, indent=2) + '\n'
    directory = ['# Markdown checklist template directory', '', f"{len(catalog['templates'])} reusable Markdown checklist templates organized by {len(groups)} teams, compatible with the Smart Checklist app for Jira Cloud. Read catalog notes before adapting historical or product-specific examples. Open each file as raw text for copying.", '', '| Team | Templates |', '| --- | --- |']
    for team, entries in groups.items():
        folder = Path(entries[0]['path']).parent.name
        directory.append(f'| [{team}]({folder}/README.md) | {len(entries)} |')
    directory += ['', 'For automated selection, use [catalog.json](../catalog.json). For syntax, use the [formatting guide](../skills/write-jira-checklist/references/formatting-guide.md).', '']
    llms = ['# Markdown checklist templates for Smart Checklist', '', '> Create checklists in Markdown format compatible with the Smart Checklist app for Jira. This repository provides reusable Markdown checklist templates, a formatting guide, and an LLM writing skill. The guide targets Jira Cloud.', '', '## Start', '', '- [Writing skill](skills/write-jira-checklist/SKILL.md): create or adapt checklist Markdown; ask for missing context when needed.', '- [Formatting guide](skills/write-jira-checklist/references/formatting-guide.md): authoritative repository syntax reference.', '- [Design practices](skills/write-jira-checklist/references/checklist-design.md): practical guidance with TitanApps sources.', '- [JSON catalog](catalog.json): IDs, summaries, tags, paths, placeholders, sources, and caveats.', '- [Human directory](templates/README.md): browse by team.', '', '## Retrieval', '', 'Search catalog metadata first, then read a few matching template paths. Template files contain only checklist Markdown. Paste the checklist content into the Smart Checklist editor; keep catalog metadata and README prose outside it. Keep stable template IDs in attribution notes outside the payload. Resolve retired IDs through the successor entry’s superseded_ids; the search script also supports these aliases. Read contribution metadata to distinguish user-supplied replacements from historical blog sources.', '', 'All placeholders use descriptive lowercase snake_case names with at least two words and no curly brackets, such as document_url, due_date, and employee_name. They are draft markers, not app variables. Preserve the type-specific syntax around them: assignee attributes, @ mentions, links, images, and due-date attributes. Follow the formatting guide when replacing values. Use - for To Do, not - [ ]. Distinguish mentions from assignee attributes and mandatory markers from workflow validators. The skill can be used standalone; the catalog requires this repository.', '', 'T075 is a product regression example with illustrative JQL patterns; use T073 for general regression. T021 is historical migration guidance. Read each entry’s notes. Static checks are not a live Jira import test.', '', '## Teams', '']
    for team, entries in groups.items():
        folder = Path(entries[0]['path']).parent.name
        llms.append(f'- [{team}](templates/{folder}/README.md): {len(entries)} checklist template{"s" if len(entries) != 1 else ""}.')
        page = [f'# {team} Markdown checklist templates', '', 'Reusable checklists in Markdown format compatible with the Smart Checklist app for Jira Cloud.', '', '[All teams](../README.md) · [Catalog](../../catalog.json)', '', '| ID | Template | Use it for |', '| --- | --- | --- |']
        for entry in entries:
            name = Path(entry['path']).name
            page.append(f"| {entry['id']} | [{entry['title']}]({name}) | {entry['summary']} |")
        with_notes = [e for e in entries if e['notes']]
        if with_notes:
            page += ['', '## Adaptation notes', '']
            for entry in with_notes:
                page.append(f"- **{entry['id']}:** {' '.join(entry['notes'])}")
        files[f'templates/{folder}/README.md'] = '\n'.join(page) + '\n'
    files['templates/README.md'] = '\n'.join(directory)
    files['llms.txt'] = '\n'.join(llms) + '\n'
    source_page = ['# Markdown checklist template sources', '', 'The collection includes adaptations from the following TitanApps articles plus original contributions and user-supplied replacements. Historical article provenance remains attached to each current template ID in `catalog.json`; contribution metadata and notes identify replaced bodies. Original contributions may have no article source. Initial blog snapshots were collected in November 2026; source pages may change. Repository formatting and editorial conventions may differ from the originals.', '', '| Article | Templates |', '| --- | --- |']
    by_url = {s['url']:s for s in catalog['sources']}
    for source in sorted(by_url.values(), key=lambda s:s['title'].lower()):
        entries = [e for e in catalog['templates'] if source['url'] in e['source_urls']]
        refs = ', '.join(f"[{e['id']}]({e['path']})" for e in entries)
        title = source['title'].replace('|', '\\|')
        source_page.append(f"| [{title}]({source['url']}) | {refs} |")
    files['SOURCES.md'] = '\n'.join(source_page) + '\n'
    return files


def main():
    catalog = json.loads((ROOT / 'catalog.json').read_text())
    files = generated_files(catalog)
    for relative, content in files.items():
        path = ROOT / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')
    print(f"Generated {len(files)} files for {catalog['template_count']} templates in {catalog['team_count']} teams.")


if __name__ == '__main__': main()
