# Markdown checklist templates for Smart Checklist

**Create checklists in Markdown format compatible with the Smart Checklist app for Jira.** This repository gives people and LLMs 78 reusable Markdown checklist templates organized by 12 teams, a formatting guide, and a skill for creating or adapting checklists. The formatting guide targets the app's **Jira Cloud** edition.

Each checklist template is a reusable `.md` file containing checklist items and supporting details. The skill uses these files as starting points and produces checklist Markdown tailored to your process. You can paste the result into Smart Checklist and optionally save it as a reusable template in the app.

The collection covers Definition of Done, code review, onboarding, releases, QA, marketing, finance, procurement, and support.

## Start here

| You want to… | Open |
| --- | --- |
| Find a checklist template by team or purpose | [Template directory](templates/README.md) |
| Explore Smart Checklist with a guided checklist | [Get Started with Smart Checklist](templates/it-and-engineering/t082-get-started-with-smart-checklist.md) |
| Let an LLM find only the relevant templates | [LLM entry point](llms.txt) and [JSON catalog](catalog.json) |
| Learn the exact Markdown syntax | [Formatting guide](skills/write-jira-checklist/references/formatting-guide.md) |
| Ask an LLM to write checklist Markdown | [Write Markdown Checklists skill](skills/write-jira-checklist/SKILL.md) |
| Write clear, testable steps | [Checklist design practices](skills/write-jira-checklist/references/checklist-design.md) |
| Add or improve a template | [Contribution guide](CONTRIBUTING.md) |

### For users

1. Find a template in the directory and open its `.md` file. Template files contain only checklist content, with no frontmatter to remove.
2. Replace placeholders with the appropriate values, keeping the surrounding Markdown syntax. All placeholders use descriptive names without curly brackets, such as `document_url`, `due_date`, and `employee_name`. See the examples below.
3. Copy the file's raw text into the Smart Checklist full-screen editor on a Jira issue. GitHub's rendered Markdown is a preview, not the Smart Checklist renderer.
4. Review the result and save it as a template in the app if you want to reuse it.

Placeholders mark missing values in reusable drafts. Their names use `snake_case`; the surrounding syntax determines whether a value is an assignee, mention, link, image, or date. For a link such as `[Document](document_url)`, replace only `document_url` with the real URL. Likewise, replace only `due_date` in `[dueDate="due_date"]` with a real date, such as `2029-03-28`. Smart Checklist does not automatically substitute these placeholders.

| Value | Draft syntax | Replace the placeholder with |
| --- | --- | --- |
| Assignee | `[assignee="assignee_user_id"]` | The responsible person's Jira user ID, keeping the quotes and brackets. |
| User mention | `@reviewer_user_id` | A Jira user ID, keeping `@`. A mention is separate from a dedicated assignee. |
| Link | `[Document](document_url)` | The document URL, keeping the link label and parentheses. |
| Image | `![Diagram](image_url)` | The image URL, keeping `!`, the alt text, and parentheses. |
| Item due date | `[dueDate="due_date"]` | A valid date in `YYYY-MM-DD` format, keeping the quotes and brackets. |

Put assignee and due-date attributes immediately after the item status marker. A name or role such as `@DesignLead` is a custom mention label, not a confirmed Jira user ID. Dates in headings or ordinary text provide context; the dedicated due-date column uses the `dueDate` attribute. See the [formatting guide](skills/write-jira-checklist/references/formatting-guide.md) for full examples.

A minimal checklist looks like this:

```text
## Release checks
- Confirm acceptance criteria are met
> Attach the test evidence and record any exceptions
-! Approve the release decision
```

The `-` creates a To Do item; it is not a GitHub `- [ ]` checkbox. Marking a step mandatory with `-!` and configuring a Jira workflow validator are separate actions. [Mandatory items documentation](https://railsware.atlassian.net/wiki/spaces/CHK/pages/3839393793).

### For LLMs and coding agents

Read `llms.txt`, then the skill and formatting guide. Search the catalog by `team`, `tags`, or `summary`; read a few matching template files rather than loading the whole collection. Stable IDs such as `T017` survive filename or title changes. Each catalog entry lists its placeholders, source URLs, and any compatibility notes.

Consolidated templates retain retired IDs in `superseded_ids`, and the search script resolves those IDs to the current template. T010 and T022 are now sections of T008 (employee onboarding); T068 and T069 are now sections of T070 (bug reporting, investigation, and fix validation). Role labels and supplied process choices, such as coverage thresholds or load targets, need review before reuse; see each template's catalog notes.

Example request:

> Use this repository's write-jira-checklist skill to create a release checklist in Markdown format compatible with the Smart Checklist app for Jira. Start from T024 and adapt it to our web app. Include QA evidence, rollback readiness, and approval. Ask for the responsible people, links, and due dates only where needed. Return a reusable draft if those details are missing.

The skill folder is portable: copy `skills/write-jira-checklist/` into the skill directory supported by your agent, including its `references/` and `scripts/` folders. It can write Markdown checklists without the catalog; keep this repository available when you want it to reuse these examples. Agents without skill support can read `SKILL.md` as task instructions. Discovery and installation conventions depend on the agent.

## How this fits Jira work

**Smart Checklist for Jira** is a checklist app by TitanApps on the [Atlassian Marketplace](https://marketplace.atlassian.com/apps/1216451/smart-checklists-for-jira?hosting=cloud&tab=overview). It keeps checklist items inside Jira work items, so a team can follow a shared process alongside the work it describes.

Use a checklist template for related action items, repeatable to-do lists, acceptance criteria, or a shared Definition of Done. For example, adapt the [Definition of Done template](templates/it-and-engineering/t017-definition-of-done.md) for your team's quality standards, or the [release readiness template](templates/it-and-engineering/t024-release-readiness-and-approval.md) for QA and deployment approvals. Use subtasks when a piece of work needs its own issue lifecycle, discussion, or time tracking. [Checklist versus subtask guidance](https://titanapps.io/blog/jira-subtasks-vs-checklists).

### Give each step an owner and context

A checkbox records completion. An assignee and priority make ownership and urgency clear, while due dates help teams plan handoffs. Checklist items can have their own responsible users, independently of the parent Jira issue's assignee. Add details, links, and images to explain the expected result and where to find evidence. The Markdown examples above show how to include these values when adapting a template. [Item attributes](https://railsware.atlassian.net/wiki/spaces/CHK/pages/5861736450) and [formatting options](https://railsware.atlassian.net/wiki/spaces/CHK/pages/90636343/Formatting+Guide).

For longer processes, organize related checks under headers. If you need multiple checklists for Jira release work, for example, separate QA, deployment, and communication into their own sections. In Tab view, each level-one Markdown header (`# `) becomes a tab with its own progress indicator. [Checklist tabs](https://railsware.atlassian.net/wiki/spaces/CHK/pages/5379194882/Checklist+Tabs).

### Reuse checklists as work moves forward

Save an adapted checklist as a template in the app, then apply it automatically at issue creation, when a field changes, or when a work item transitions. Conditions can use the issue type or a label: for example, apply a release checklist to work items labeled `release`, or a Definition of Done checklist to stories. Advanced conditions require a plan that includes them. [Default template conditions](https://railsware.atlassian.net/wiki/spaces/CHK/pages/1294532651/Set+a+Template+as+Default).

For recurring tasks such as monthly reviews, reuse the same template to keep recurring checklists consistent. Jira Automation can import saved checklist templates as part of a configured rule; use a [scheduled trigger](https://support.atlassian.com/cloud-automation/docs/jira-automation-triggers/) to create the recurring work items when needed. In Jira Cloud, the `Checklists` custom field stores the raw Markdown. This checklist text field is also useful when an automation rule needs to add or update checklist content. [Template automation](https://railsware.atlassian.net/wiki/spaces/CHK/pages/3921543201/Use+Templates+in+Automations) and [custom fields](https://railsware.atlassian.net/wiki/spaces/CHK/pages/1372422219/Custom+Fields+Setup).

For required approvals, mark the relevant items mandatory with `-!`. In company-managed projects, a Jira workflow validator can block a transition until those items are complete. This requires a plan that includes validators and configuration in Jira separately from the Markdown. [Mandatory-item completion validator](https://railsware.atlassian.net/wiki/spaces/CHK/pages/3807641616).

### Follow progress across the team

Use JQL search to find work items by checklist content and supported checklist properties. You can also display the `Smart Checklist Progress` custom field on an agile board to see completion progress without opening every work item. [JQL search](https://railsware.atlassian.net/wiki/spaces/CHK/pages/152961090/JQL+Search) and [progress field](https://railsware.atlassian.net/wiki/spaces/CHK/pages/1372422219/Custom+Fields+Setup).

For service requests, Smart Checklist can show customers a read-only checklist on the Jira Service Management customer portal. Enable portal visibility in both global and project settings to let customers follow progress while your team maintains the checklist. [Customer portal setup](https://railsware.atlassian.net/wiki/spaces/CHK/pages/3687874561).

## Compatibility and naming

The checklists use the Markdown syntax supported by the Smart Checklist app for Jira Cloud, including its status markers, details, and item attributes. A heading, mention, or label in checklist text does not automatically set a Jira field. For example, `#must` is descriptive text, whereas `-!` marks a mandatory checklist item. User mentions and dedicated assignee attributes also have different meanings; the formatting guide explains both.

T075 is a product-specific regression example with illustrative JQL patterns, not a general-purpose regression checklist or a set of guaranteed executable queries. T021 is a historical Server-to-Cloud migration example. These distinctions are included in the catalog so LLMs can choose appropriate starting points. Security, legal, and financial templates are process examples to adapt to your requirements, not certifications of compliance.

## Search and validate locally

Python 3.10 or newer is sufficient; no third-party packages are required.

```sh
python3 scripts/search_templates.py "release approval"
python3 scripts/search_templates.py onboarding --team "HR and Recruiting" --json
python3 skills/write-jira-checklist/scripts/lint_checklist.py path/to/draft.md
python3 skills/write-jira-checklist/scripts/lint_checklist.py path/to/final.md --ready
python3 scripts/validate_repository.py
python3 -m unittest discover -s tests
```

The linter checks common syntax mistakes and unresolved placeholders. It is not the app parser and cannot verify Jira user IDs, custom statuses, live URLs, or workflow settings. Templates have been reviewed against the published formatting documentation; actual Jira imports are not part of the repository's automated checks.

## Reuse and attribution

Copy, adapt, and reuse the repository under the [MIT license](LICENSE), retaining its notice. See [NOTICE](NOTICE) and [SOURCES.md](SOURCES.md) for source attribution. Product names and trademarks remain with their respective owners. This repository contains templates and guidance; the Smart Checklist app has its own license.
