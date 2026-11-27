# Live import smoke tests — 27 November 2026

All 78 templates were saved in the Smart Checklist Markdown editor on Jira Cloud in eight batches. The rendered item totals matched the expected 1,890 items. The catalog's `result: passed` records this **save/render smoke test**, not comprehensive verification of every template feature or business process.

The installed app's version was not exposed in the tested UI, so the catalog records `not exposed by app UI`. Testing used the repository owner's authorized test issue in Chrome. Its original 25-item checklist was backed up, restored after testing, and its restored count and section headings were observed.

## Changes since the test

T021 subsequently had one duplicated “Filters” item removed. Its current body has no live-test claim in the catalog. The counts below describe the tested versions and remain unchanged as evidence of that test.

## Inputs and scope

Templates were concatenated with blank lines; their checklist wording and status markers were preserved. In test copies, bare URL placeholders were replaced with HTTPS example URLs, date placeholders with 28 March 2029 in the required ISO or day/month/year format, and dedicated assignee ID placeholders with an account available on the test site. Other text placeholders remained draft labels. These substitutions were not written into the reusable templates.

Each catalog record refers to the hash of its original source template. The test used the substitutions described above; it was not an assertion that unresolved attributes work as production values. Private account identifiers, issue content, raw UI captures, and screenshots are retained outside the public repository.

## Observed batch results

| Batch | Template IDs | Expected items | Rendered items |
| --- | --- | ---: | ---: |
| batch-01 | T001, T002, T003, T004, T005, T006, T007, T008, T009, T011, T012, T013 | 249 | 249 |
| batch-02 | T014, T015, T016, T017, T018, T019, T020, T021, T023, T024, T025, T082 | 222 | 222 |
| batch-03 | T026, T027, T028, T029, T030, T031, T032, T033, T034 | 247 | 247 |
| batch-04 | T035, T036, T037, T038, T039, T040, T041 | 243 | 243 |
| batch-05 | T042, T043, T044, T045, T046, T047, T048 | 246 | 246 |
| batch-06 | T049, T050, T051, T052, T053, T054, T055, T056, T057, T058, T059, T060 | 234 | 234 |
| batch-07 | T061, T062, T063, T064, T065, T066, T067, T070, T071, T072, T073, T074 | 246 | 246 |
| batch-08 | T075, T076, T077, T078, T079, T080, T081 | 203 | 203 |

## Representative individual checks

- **T001:** saved separately and rendered 15 items with section headings.
- **T017:** rendered 10 items. Bold, italic, inline code, role labels, links, and the date display were observed. Expanding the feature-flag item's details showed its note and documentation link.
- **T082:** rendered 17 items. The tutorial displayed headings, links, bold, italic, inline code, a custom mention, an inline date, and dedicated due-date, assignee, and High-priority attributes.

## Limits

Batch counts establish that the app accepted and counted the checklist items. They do not establish that every heading, detail block, mandatory marker, image, or link destination was individually checked. The representative visual checks cover only the features listed above. No checklist process steps, external links, workflow validators, automation rules, notifications, permissions, or completion transitions were exercised. No byte-for-byte round-trip assertion is made.

For stronger assurance before deployment, repeat the detailed per-template procedure in [import validation](import-validation.md) on the target app configuration. Retest changed template bodies; the repository validator rejects evidence tied to an obsolete content hash.
