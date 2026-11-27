# Quality Assurance Markdown checklist templates

Reusable checklists in Markdown format compatible with the Smart Checklist app for Jira Cloud.

[All teams](../README.md) · [Catalog](../catalog.json)

| ID | Template | Use it for |
| --- | --- | --- |
| T067 | [API testing](t067-api-testing.md) | Verify API contracts, requests, error handling, authorization, reliability, and reporting. |
| T070 | [Bug reporting, investigation, and fix validation](t070-bug-report-completeness.md) | Create a complete bug report, investigate and prioritize it, then validate the fix and regression coverage. |
| T071 | [QA testing](t071-feature-qa-and-testing.md) | Complete functional and regression testing, applicable specialist checks, defect triage, evidence, and QA sign-off. |
| T072 | [Performance testing](t072-performance-testing.md) | Plan load scenarios, establish thresholds, run performance tests, and report findings. |
| T073 | [General regression testing](t073-regression-testing-general-checklist.md) | Run general regression coverage across UI, functionality, integrations, performance, and security. |
| T074 | [Security testing](t074-security-testing.md) | Check application security across authentication, sessions, access control, inputs, and data. |
| T075 | [Smart Checklist regression testing](t075-smart-checklist-regression-testing.md) | Illustrate Smart Checklist product regression scenarios, template behavior, and JQL patterns. |
| T076 | [Test execution](t076-test-execution.md) | Prepare a test run, execute cases, record defects, and hand over the results. |
| T077 | [Test plan entry and exit criteria](t077-test-plan-entry-and-exit-criteria.md) | Define the environment, evidence, and quality conditions for starting and finishing testing. |
| T078 | [Usability and accessibility testing](t078-usability-and-accessibility-testing.md) | Check accessible interactions, content, navigation, contrast, and form usability. |

## Adaptation notes

- **T070:** Consolidates T068, T069; use the relevant sections of this checklist instead of the retired standalone templates.
- **T071:** Role mentions are illustrative labels. Use confirmed Jira user IDs for real user mentions or dedicated assignees. The 1000-concurrent-user load target and named browsers are supplied test-scope choices; confirm them for the product before use.
- **T075:** Specific to testing Smart Checklist. For a general regression checklist, prefer T073. JQL fragments include alternatives and legacy properties: verify against current documentation and replace placeholders before execution.
