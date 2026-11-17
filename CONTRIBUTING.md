# Contributing Markdown checklist templates

Contribute checklists in Markdown format compatible with the Smart Checklist app for Jira. Keep each checklist template focused on one reusable process, a coherent set of stages, or a distinct specialist use case. Improve an existing template when the proposed addition differs mostly in wording. Keep separate templates when they have different outcomes or useful domain-specific coverage.

1. Read the [formatting guide](skills/write-jira-checklist/references/formatting-guide.md) and [design practices](skills/write-jira-checklist/references/checklist-design.md).
2. Add or edit a raw `.md` file under the appropriate team directory in `templates/`. Do not include YAML, an attribution block, or code fences in that file.
3. Add or update its entry in `catalog.json`: stable ID, title, team, summary, tags, kind, path, source URLs, and notes. Assign a new unused ID for a new template; do not renumber existing IDs.
4. Include a source record with its title and URL for an adapted template. Identify original contributions in the entry notes. Do not insert real customer details, credentials, private URLs, or personal data into public examples.
   When consolidating templates, retain retired IDs in the successor's `superseded_ids`, merge their source URLs, and remove redundant payload files. Do not reuse retired IDs for new templates. Record user-supplied replacements in `contribution` metadata so historical blog sources are not mistaken for the current wording.
5. Regenerate the indexes and run validation:

```sh
python3 scripts/rebuild_indexes.py
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests
```

`rebuild_indexes.py` refreshes placeholder lists, content hashes, counts, the team directories, `SOURCES.md`, and `llms.txt`. Template bodies and editorial catalog fields remain the maintained source. Review generated diffs before committing.

If you can test the Markdown in the Smart Checklist app for Jira Cloud, describe the app version and the behavior observed. A successful static check is not a claim that a live Jira import was tested. Avoid expanding compatibility claims to other apps or Data Center without evidence.

Contributions are made under the repository's MIT license. Retain attribution to adapted source material.
