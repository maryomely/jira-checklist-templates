# Checklist design practices

Use these practices to decide what to include in a Markdown checklist for the Smart Checklist app for Jira. They combine the cited TitanApps guidance with this repository's editorial conventions. A source checklist template is a starting point, not an obligation to include every step.

## Match the structure to the work

Use checklist items for steps or checks belonging to one process. Prefer separate Jira work items or subtasks when a piece needs its own lifecycle, estimates, time tracking, attachments, or discussion. Different checklist owners alone do not require subtasks because Smart Checklist supports item assignees. [TitanApps on subtasks versus checklists](https://titanapps.io/blog/jira-subtasks-vs-checklists).

Group checks by meaningful stage, such as preparation, execution, verification, and handover. Keep a reusable core and adapt context-specific steps. If a template covers a broad workflow, select the relevant stage rather than copying unrelated work. [TitanApps on checklist templates](https://titanapps.io/blog/jira-checklist-template).

## Write observable completion conditions

An action should name the work and its result: “Attach the approved deployment plan” is clearer than “Deployment plan.” For verification, state what must be true and how it can be checked. Put examples, instructions, and links in details so the item stays readable.

Acceptance criteria describe the expected outcome of a particular story or work item. The Definition of Done is the team's shared quality standard. Do not substitute a generic DoD checklist for the actual acceptance criteria. Use Given–When–Then where behavior needs a scenario; use concise checkable statements where the result is directly observable. [TitanApps on acceptance criteria](https://titanapps.io/blog/acceptance-criteria-jira).

For testing, identify the build, environment, test data, expected outcome, and evidence when they matter. Include failure and exception handling instead of assuming every check passes. Keep defects trackable and make the test handover understandable. [TitanApps on QA checklists](https://titanapps.io/blog/qa-checklist).

## Add ownership and evidence deliberately

Ask for the responsible person when a handoff or approval would otherwise be ambiguous. Use Jira IDs for assignee attributes; use named role placeholders while drafting. Distinguish the person doing the work from a reviewer or someone merely mentioned.

Use real links to policies, evidence, briefs, dashboards, and forms supplied by the user. Ask for missing links that materially affect execution; otherwise keep descriptive placeholders. Include a due date when the process has an agreed deadline. Clarify relative dates, time zones, or business-day assumptions before calculating them. These are repository conventions for avoiding invented operational details.

## Reuse without overstating automation

Save checklists for repeatable processes as templates in the app. Applying saved checklist templates automatically and using Jira Automation can reduce repeated setup, but Markdown only defines checklist content. Recurring work needs a configured trigger or schedule. Reserve mandatory markers for agreed gates and explain that blocking transitions needs a configured validator. [TitanApps on template reuse and automation](https://titanapps.io/blog/jira-checklist-template).

## Review before delivery

Remove duplicate checks and split items whose independent outcomes could be completed separately. Preserve distinct specialist checks when consolidation would lose coverage. Keep necessary conditions such as “if applicable,” and explain how to record exceptions. Do not turn an illustrative threshold, legal deadline, or sample policy into an asserted requirement for the user's organization.

Ask whether the checklist is usable by someone who was not in the planning conversation: they should understand what to do, what counts as done, where to find supporting information, and who owns important decisions. Then validate the syntax using the [formatting guide](formatting-guide.md).
