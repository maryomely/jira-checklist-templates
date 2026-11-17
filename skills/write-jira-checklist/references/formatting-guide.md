# Markdown formatting guide for the Smart Checklist app for Jira

Use this guide to write checklists in Markdown format compatible with the Smart Checklist app for Jira. It covers the app's Jira Cloud edition. Reviewed 16 November 2026. Examples containing placeholders such as `document_url`, `due_date`, or `employee_name` are drafts: replace them before use. Copy raw checklist Markdown into the app's full-screen editor; do not paste this guide or its surrounding code fences.

## Statuses and mandatory items

Start each checkable line with a status marker and a space:

| Syntax | Meaning |
| --- | --- |
| `- Check the result` | To Do |
| `~ Check the result` | In Progress |
| `+ Check the result` | Done |
| `x Check the result` | Skipped |
| `- [In Review] Check the result` | Configured custom status |

Use custom status names that exist in the target configuration. A GitHub task marker such as `- [ ]` is not the recommended syntax here. [Status syntax](https://railsware.atlassian.net/wiki/spaces/CHK/pages/90636343/Formatting+Guide).

Add `!` directly after the status marker to make an item mandatory: `-!`, `~!`, `+!`, or `x!`. A leading asterisk or a `#must` label does not do this. Mandatory marking does not itself install a transition validator; enforcement needs workflow configuration. [Mandatory items](https://railsware.atlassian.net/wiki/spaces/CHK/pages/3839393793).

## Headings and tabs

Use one to six `#` characters followed by a space. In Tab view, level-one headings become separate tabs. Choose levels to reflect the workflow rather than visual decoration. [Headers](https://railsware.atlassian.net/wiki/spaces/CHK/pages/4146659350) and [tabs](https://railsware.atlassian.net/wiki/spaces/CHK/pages/5379194882).

```text
# Release
## Preparation
- Confirm scope
## Verification
- Confirm acceptance criteria
```

## Details and nested lists

Details use `>` on each line and follow their owner. Headers and standalone text can also have details; they are not automatically errors. Details are explanatory content, not separately checkable child items. The nested form below follows the guide's example. [Markdown support](https://railsware.atlassian.net/wiki/spaces/CHK/pages/88866897/Markdown+support), [formatting examples](https://railsware.atlassian.net/wiki/spaces/CHK/pages/90636343/Formatting+Guide), and [header-detail release notes](https://railsware.atlassian.net/wiki/spaces/CHK/pages/3573284886).

```text
## Verification
> Applies to the release candidate
- Record the test evidence
> * Link the test run
> * Record the environment
> > * Include the build identifier
> 1. Describe the expected result
> 2. Record the observed result
```

## Assignee priority and due date

Place attributes immediately after the status marker, before the item text. Use straight double quotes. Priority values are `High`, `Medium`, or `Low`; due dates use valid `YYYY-MM-DD` dates. A dedicated assignee requires a Jira user ID, not a display name. [Attribute documentation](https://railsware.atlassian.net/wiki/spaces/CHK/pages/5861736450).

```text
- [assignee="qa_user_id"] Verify the release candidate
- [dueDate="review_due_date"] Review the evidence
-! [priority="High"][dueDate="approval_due_date"][assignee="approver_user_id"] Approve the release
```

An `@reviewer_user_id` mention references a user; a custom mention such as `@ReviewTeam` is a label. Neither is the dedicated assignee attribute. Dates written in text or headings provide context; use `dueDate` for the dedicated deadline. The main guide's date-order prose is inconsistent with its examples; this repository follows the explicit ISO format in the attribute documentation.

## Inline formatting links and literal syntax

Use `**bold**`, `_italic_`, and backticks for code. `_italic_` is this repository's preferred spelling; balanced `*italic*` in source templates is also retained. Protect literal code and JQL fragments with backticks. [Text formatting examples](https://railsware.atlassian.net/wiki/spaces/CHK/pages/88866897/Markdown+support).

Use complete links, with both closing delimiters. Escape literal bracket labels so they do not resemble custom statuses. Jira issue URLs can be written directly. Image and emoji syntax is optional. The official guide's external-link example omits a closing parenthesis; the example below includes it. [Link, image, emoji, and escaping syntax](https://railsware.atlassian.net/wiki/spaces/CHK/pages/90636343/Formatting+Guide).

```text
- Review [the release plan](release_plan_url)
- \[Production\] Verify the deployed version
- Check [the related issue](jira_issue_url)
- Inspect ![architecture diagram](diagram_url)
- Announce completion :white_check_mark:
```

## Placeholders and output modes

Use descriptive `lowercase_snake_case` names without curly brackets for all missing values. Use at least two words, such as `employee_name` or `calendar_year`, to distinguish placeholders from ordinary prose. Keep the syntax required for each value type, as shown below. These are editing conventions, not Smart Checklist substitution features. Replace only the placeholder name with the real value.

| Value | Draft syntax | Required replacement |
| --- | --- | --- |
| Dedicated assignee | `[assignee="qa_user_id"]` | A confirmed Jira user ID, not a name or role. |
| User mention | `@reviewer_user_id` | A confirmed Jira user ID; this does not set the dedicated assignee. |
| Custom mention label | `@team_mention` | A custom label such as `ReviewTeam`; it does not identify a verified Jira account. |
| Document link | `[Evidence](evidence_url)` | A full document URL. Preserve the label and parentheses. |
| Image | `![Diagram](diagram_url)` | An image URL. Preserve the leading `!`, alt text, and parentheses. |
| Item due date | `[dueDate="review_due_date"]` | A valid calendar date in `YYYY-MM-DD` format. |
| Contextual date | `Meeting on meeting_date` | A date in `YYYY-MM-DD` format for this repository's prose examples; it does not populate the dedicated due-date column. |
| Plain text | `Welcome employee_name` | The employee's name, with no user mention implied. |

For new placeholders, use `_user_id` for Jira accounts, `_mention` for custom mention labels, `_url` for URLs, and `_date` for dates. All placeholders must be replaced before use. Bare URL names are not working relative links; date names are not calendar dates, and user ID names are not verified accounts. Keep plain-text names distinct from account IDs. Historical query examples may specify their own value formats in catalog notes; do not treat a query date format as a due-date attribute format.

Example reusable draft:

```text
- [assignee="qa_user_id"][dueDate="review_due_date"] Review the release
> Read [the test report](test_report_url) and ask @reviewer_user_id for feedback.
> Compare the result with ![the approved design](design_image_url).
```

Fill in the two Jira user IDs, the review date, the test report URL, and the design image URL before pasting. Keep the `@`, attribute names, quotes, brackets, link labels, image alt text, and parentheses in place.

For a **draft**, retain missing values and list them outside the copyable checklist. For **paste-ready output**, substitute real values, check valid calendar dates, and remove optional attributes that the user does not need. Confirm user IDs and custom statuses in Jira when possible. Do not invent dates or treat every contextual date as a deadline.

## Final check

- Use Smart Checklist status prefixes, not generic Markdown checkboxes.
- Keep details with their intended owner; preserve supported header details.
- Balance links, code spans, and emphasis; escape literal bracket labels.
- Check assignee IDs, dates, custom statuses, and unresolved placeholders.
- Keep setup instructions and explanatory notes outside the checklist payload.

The bundled linter catches common structural mistakes and treats bare lowercase snake_case names as draft placeholders, including in query examples. Real URLs and emoji shortcodes are excluded. Review code identifiers manually if they also use snake_case. It does not replace checking the rendered result in your installed app.
