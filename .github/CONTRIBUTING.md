# Contributing Markdown checklist templates

Contribute checklists in Markdown format compatible with the Smart Checklist app for Jira. Keep each checklist template focused on one reusable process, a coherent set of stages, or a distinct specialist use case. Improve an existing template when the proposed addition differs mostly in wording. Keep separate templates when they have different outcomes or useful domain-specific coverage.

1. Read the [formatting guide](../skills/write-jira-checklist/references/formatting-guide.md) and [design practices](../skills/write-jira-checklist/references/checklist-design.md).
2. Add or edit a raw `.md` file under the appropriate team directory in `templates/`. Do not include YAML, an attribution block, or code fences in that file.
3. Add or update its entry in `templates/catalog.json`: stable ID, title, team, summary, tags, kind, path, source URLs, and notes. Assign a new unused ID for a new template; do not renumber existing IDs.
4. Include a source record with its title and URL for an adapted template. Identify original contributions in `contribution` metadata; reserve notes for guidance needed to adapt the checklist. Do not insert real customer details, credentials, private URLs, or personal data into public examples.
   When consolidating templates, retain retired IDs in the successor's `superseded_ids`, merge their source URLs, and remove redundant payload files. Do not reuse retired IDs for new templates. Record user-supplied replacements in `contribution` metadata so historical blog sources are not mistaken for the current wording.
5. Regenerate the indexes and run validation:

```sh
python3 -m pip install -r tools/requirements-dev.txt
python3 tools/rebuild_indexes.py
python3 tools/build_skill.py
python3 tools/validate_repository.py
python3 -m unittest discover -s tools/tests
```

`rebuild_indexes.py` refreshes placeholder lists, content hashes, counts, the team directories, `docs/sources.md`, and `llms.txt`. Review generated diffs before committing. Edit the maintained sources below; manual edits to generated files are overwritten and fail validation until regenerated.

| Content to change | Maintained source | Generated output |
| --- | --- | --- |
| Checklist steps | Raw template `.md` files | Catalog item counts, placeholders, and hashes |
| Template metadata and attribution | Editorial fields in `templates/catalog.json` | Team directories and `docs/sources.md` |
| LLM introduction and instructions | `tools/index_sources/llms-intro.txt` | `llms.txt` introduction |
| LLM team directory | Team metadata in `templates/catalog.json` | `llms.txt` team links |

If a template contains real `snake_case` code identifiers or JQL field names, list those exact names in its optional `literal_identifiers` catalog field, for example `["custom_field", "request_id"]`. Generation excludes these names from the placeholder inventory, and validation uses the same allow-list. Do not list values that still need replacing. For a standalone file, use the linter's repeatable `--allow-identifier` option.

If you can test the Markdown in the Smart Checklist app for Jira Cloud, describe the app version and the behavior observed. A successful static check is not a claim that a live Jira import was tested. Avoid expanding compatibility claims to other apps or Data Center without evidence.

Contributions are made under the repository's MIT license. Retain attribution to adapted source material.

The catalog declares its JSON Schema for editor support. CI checks the schema, links, unexpected invisible controls, and generated outputs. Actual checklist link destinations must use HTTPS; draft URL names remain allowed. Raw rendered HTML is not checklist syntax. Legitimate emoji sequences are supported.

For new content, use one verifiable action or outcome per item, sentence case, and restrained emphasis. Reserve inline code for identifiers, commands, or literal syntax. Emoji and custom role labels are optional; distinguish labels from verified assignees. Preserve the author's valid syntax when updating existing contributions.

To enable the optional local hook, run `git config core.hooksPath tools/hooks`. It rebuilds indexes and the latest skill ZIP, validates, and runs tests. It never stages changes automatically; stage regenerated files and retry. CI remains authoritative.
