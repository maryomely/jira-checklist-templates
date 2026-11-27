# IT and Engineering Markdown checklist templates

Reusable checklists in Markdown format compatible with the Smart Checklist app for Jira Cloud.

[All teams](../README.md) · [Catalog](../catalog.json)

| ID | Template | Use it for |
| --- | --- | --- |
| T014 | [Code formatting and review](t014-code-formatting-and-review.md) | Review code structure, conventions, maintainability, security, and performance. |
| T015 | [Code review](t015-code-review.md) | Review implementation, readability, maintainability, security, tests, documentation, and deployment risks. |
| T016 | [Dark mode implementation example](t016-dark-mode-implementation-example.md) | Illustrate a feature delivery workflow using dark mode from design through monitoring. |
| T017 | [Definition of Done](t017-definition-of-done.md) | Verify implementation, test coverage, QA, review, feature flags, documentation, and final sign-off. |
| T018 | [Developer technical onboarding through the first month](t018-developer-technical-onboarding-through-the-first-month.md) | Guide a developer's technical setup, working agreements, first week, and first month. |
| T019 | [Feature deployment and monitoring](t019-feature-deployment-and-monitoring.md) | Check production readiness, deploy a feature, and monitor the live result. |
| T020 | [Feature technical implementation](t020-feature-technical-implementation.md) | Translate a feature specification into technical tasks, APIs, data changes, and owners. |
| T021 | [Jira Server to Cloud premigration](t021-jira-server-to-cloud-premigration.md) | Review legacy Jira Server-to-Cloud migration prerequisites and preparation steps. |
| T023 | [Release deployment workflow](t023-release-deployment-workflow.md) | Coordinate staging, regression testing, production deployment, and post-release actions. |
| T024 | [Release readiness and approval](t024-release-readiness-and-approval.md) | Check code quality, QA sign-off, deployment preparation, production approval, and post-deployment smoke tests. |
| T025 | [Software licensing management](t025-software-licensing-management.md) | Inventory software, assign owners, manage access, and review license renewals and usage. |
| T082 | [Get Started with Smart Checklist](t082-get-started-with-smart-checklist.md) | Learn Smart Checklist editing, formatting, templates, automation, configuration, and support. |

## Adaptation notes

- **T016:** Dark mode is an example feature; adapt the implementation details to the actual product.
- **T017:** Role mentions are illustrative labels. Use confirmed Jira user IDs for real user mentions or dedicated assignees. The >80% coverage threshold, LaunchDarkly requirement, A-Team review, and role labels are supplied process choices, not universal requirements. Confirm them and replace the final sign-off date and document URLs before use.
- **T021:** Historical Server-to-Cloud material. Verify current migration guidance before use; #must labels are plain text and do not mark mandatory items.
- **T023:** Replace _user_id placeholders with confirmed Jira user IDs; user mentions retain @ and are separate from dedicated assignees.
- **T024:** Role mentions are illustrative labels. Use confirmed Jira user IDs for real user mentions or dedicated assignees.
- **T082:** Role mentions are illustrative labels. Use confirmed Jira user IDs for real user mentions or dedicated assignees. Replace the due-date and assignee placeholders before use. Configuration features depend on the installed edition and permissions; the Markdown does not configure them automatically.
