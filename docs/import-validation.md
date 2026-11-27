# Smart Checklist import validation

Static tests do not establish that every checklist renders correctly in a live app. Import evidence is recorded only after an observed test, with the exact template content hash. An absent `import_validation` catalog field means the current template version has no recorded live import result.

Use a disposable Jira Cloud issue with Smart Checklist installed. Save the original raw checklist before testing and restore it afterward. Do not execute the process steps or notify role mentions merely because they appear in a test template.

The [27 November 2026 results](import-validation-2026-11-27.md) cover save/render smoke tests for the 78 versions tested that day and representative visual checks. Later edits do not inherit that evidence. They do not complete the detailed procedure below for every template.

For a detailed per-template test:

1. Open the full-screen Markdown editor and paste the raw template. Substitute test values for unresolved attributes when testing dedicated assignees and dates; record those substitutions separately.
2. Save, reopen the issue, and check the number and text of items, mandatory markers, headings, details, links, mentions, and available metadata columns. Test image rendering with an approved accessible image when that syntax is used.
3. Reopen the Markdown editor and compare the saved content. Record parser normalization or rendering differences. An accepted save alone is not proof that every feature rendered correctly.
4. Record the test date, Jira Cloud, app version if exposed (otherwise `not exposed by app UI`), exact source `sha256`, pass/fail result, and a relative path to a public evidence summary. Keep private issue URLs, user IDs, original issue content, and screenshots containing private data outside the public repository.

The optional `import_validation` field is defined by `tools/catalog.schema.json`. Validation rejects evidence whose `template_sha256` no longer matches the template. After an edit, retest or remove the obsolete claim. Distinguish a raw draft import from a test using substituted values; do not describe untested templates as passed.
