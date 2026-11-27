# Optional tools

Run these commands from the repository root. No tools or installation are needed to browse and copy templates.

Search and the portable skill need only Python. Repository checks are tested on Python 3.10–3.13 and require `python -m pip install -r tools/requirements-dev.txt` for JSON Schema validation.

```sh
python3 tools/search_templates.py "release approval"
python3 tools/search_templates.py onboarding --team "HR and Recruiting" --json
python3 skills/write-jira-checklist/scripts/lint_checklist.py path/to/draft.md
python3 skills/write-jira-checklist/scripts/lint_checklist.py path/to/final.md --ready
python3 tools/validate_repository.py
python3 tools/build_skill.py --check
python3 -m unittest discover -s tools/tests
```

Search matches whole words and common English plural forms; it does not perform full linguistic stemming or synonym expansion. The `--team` filter requires the full team name, ignoring case and repeated whitespace. Exact template IDs and retired IDs still resolve directly.

The linter checks common syntax mistakes and unresolved placeholders. For real code identifiers, use `--allow-identifier request_id` (repeat as needed); unresolved values in code spans are still checked. See [contribution instructions](../.github/CONTRIBUTING.md) for catalog exceptions and the source files to edit when updating generated documentation. It is not the app parser and cannot verify Jira user IDs, custom statuses, live URLs, or workflow settings. Templates have been reviewed against the published formatting documentation; actual Jira imports are not part of the repository's automated checks.

## Maintainers

Build scripts, tests, the catalog schema, dependency requirements, and the optional commit hook live together here. The portable checklist linter stays inside the skill so it also works without this repository.

See the [contribution guide](../.github/CONTRIBUTING.md) for the edit and rebuild workflow and the [publication policy](../docs/publication.md) for publishing the latest snapshot.
