## Smart Checklist regression item operations
### Work with checklist
- Add checklist item using Quick View
- Add checklist item using Full-Screen Editor
- Add checklist item by applying “Getting started” template
- Change checklist item statuses (To Do > In Progress > Skipped > Done)
- Edit checklist in Full-Screen Editor (headers, bullet/number points, bold/italic/emphasized text, link)
- Edit checklist in Full-Screen Editor: add item with custom status
- Edit checklist in Quick View (headers, bullet/number points, bold/italic/emphasized text, date, link)
- Verify tooltips exist for checklist items (after add/edit/change status/replace)
### Details
- Add details to checklist item from Smart Checklist menu
- Edit details from Quick View
- Add details to checklist item in Full-Screen Editor
### Dates
- Add date to checklist item (past, today, future; different formats)
- Add calendar date by typing //
### Content operations
- Copy & paste checklist from text to add-on
- Convert checklist item to Jira issue
- Reorder checklist items
- Delete checklist item in Quick View
- Delete details from Quick View
- Clear checklist
### Links & references
- Add Jira ticket with Jira key
- Add external link (Facebook, Instagram, GitHub, HelpScout, etc.)
### Assignees
- Assign a user to checklist item (current user / another user / custom user)
### Clone coverage
- \[Company-managed\] Clone issue with checklist when Checklists custom field is not on the screen
- \[Team-managed\] Clone issue with checklist when Checklists custom field is not on the screen
### Bulk actions
- Check all items when there is at least one not completed item
- Uncheck all items when all items are completed/checked

## Smart Checklist regression mandatory items
### Mandatory items (Issue view)
- Make mandatory exists in the menu for checklist items
- Make non-mandatory exists in the menu for mandatory checklist items
- Asterisk `*` is added to mandatory checklist item
- Asterisk `*` is removed for non-mandatory checklist item
- Make an item mandatory > Check History
- Make it non-mandatory > Check History
### Mandatory items (Templates)
- \[Create Template\] Make mandatory exists in the menu for checklist items
- \[Create Template\] Make non-mandatory exists in the menu for mandatory checklist items
- Add `-! with text` in Full-Screen Editor > item becomes mandatory, asterisk `*` is added
- Mandatory items displayed as `-!` in custom field Checklists
### Pro History behavior
- Using Pro version, change whether items are mandatory > check events on History
- Open version History > confirm behavior

## Smart Checklist regression headings
### Work with headers
- Collapse/Expand all headers button
- Convert to header
- Convert to item
- Check/uncheck items under header
- Add item under header
- Drag and drop headers/items when all expanded
- Drag and drop headers/items when all collapsed
- Delete header with items
- Delete header without items
- Checklist header progress
- Header of different levels (progress, collapse, indent)
- Add details to headers
- Delete details from headers
### Headers in templates
- Header in templates (progress, indent, reorder, edit, delete, add details)
- Collapse/Expand all headers of different levels

## Smart Checklist regression templates
### Checklist templates
- Save Checklist as a Template
- Create a Template
- Import Checklist from a Template
- Set Template as Default for a few issue types
- Set Template as Default to all issue types
- Remove assignment from Template
- Rename a Template
- Edit a Template from Editor
- Edit a Template from Checklist UI
- Delete a Template
- Duplicate a Template
- Convert to Global Template
- Convert to Project Template
- Reorder Templates for issue type
### Template ID
- Template ID exists for Project templates
- Template ID exists for Global templates

## Smart Checklist regression linked templates
### Linked templates
- Create Linked Template
- Convert non-linked template to Linked
- Convert Linked template to non-Linked
- Import Linked Template to issue
- Editor is disabled for Linked Template
- Items imported from Linked template are not displayed in Full-Screen Editor
### Editing + sync
- Edit Linked Template from Checklist UI (add item, delete item, add header, add details, reorder)
- Change status of any item in linked template on issue view
- Update linked template > verify it reflects in linked issues
### Unlink behaviors
- Unlink template and keep items
- Unlink template and remove items (check UI, issue property, custom fields)
### Order + duplication
- Manage order of linked templates assigned to default issue type
- Duplicate Linked Template
- Delete Linked Template
### History events
- Verify events for linked template operations in Smart Checklist History tab

## Smart Checklist regression template categories
### Template categories
- Assign Project template to Category
- Assign Global template to Category
- Unassign Project/Global template from Category
- Create template with defined category
### UI checks
- Verify Categories list on Category dropdown on Template edit popup
- Verify hint icon, hint text, and link for Categories field
- Expand/Collapse category
- Edit template under Category section
### Actions under category
- Convert to linked Project template under Category section
- Convert to non-linked Project template under Category section
- Convert to project/global template with Category
- Delete Project/Global template under Category section
- Import Project/Global template under Category section

## Smart Checklist regression assignment rules
### Template assignment UI
- Advanced and General tabs are displayed in template assignment section
- Check Learn more links for General/Advanced tabs
### General > Advanced mapping scenarios
- \[General\] Select “All issue types” > \[Advanced\] Issue created trigger
- Template appears in Manage order view for All issue types
- Create issue to verify template is applied
- \[General\] Select several issue types > \[Advanced\] Issue created + Issue type field values
- Template appears for selected issue types
- Create issue to verify template is applied
### Advanced-only scenarios
- \[Advanced\] Issue transitioned trigger + Save
- General tab has nothing selected
- Create issue to verify template is applied based on conditions
- \[Advanced\] Issue transitioned trigger + Issue type values + Save
- Create issue to verify template is applied based on conditions
- \[Advanced\] Issue updated trigger + any other fields + Save
- Create issue to verify template is applied based on conditions
### Available fields/conditions check coverage
- Check available fields in Fields dropdown
- Check available options in Conditions dropdown
- Check available options in Value dropdown
### Guardrail
- Template is applied only once per configured trigger even when all conditions match multiple times

## Smart Checklist regression history search and integration
### History
- Track Smart Checklist changes for Free Version
- Track Smart Checklist changes for Pro Version
### Search / JQL examples (smart checklist data)
- Search by currently logged user (`issue.property[SmartChecklist].assignees ~ currentUser()`)
- Search by any user (`issue.property[SmartChecklist].assignees ~ "user_id"`)
- Search by custom mention (`issue.property[SmartChecklist].assignees ~ "team_mention"`)
- Search for not done checklist items (`"Smart Checklist Progress" ~ "-Done"`)
- Search for completed checklist (`"Smart Checklist Progress" ~ "Done"`)
- Search for issue that contains checklist (`Checklists (or cf[custom_field_id]) is not EMPTY`)
- Search for content in checklist (`Checklists (or cf[custom_field_id]) ~ "item_text"`)
- `issue in checklistItemStatus("item_text", "Done")`
- `issue.property[SmartChecklist].hasClosedChecklistItems = 'true'`
- `issue.property[SmartChecklist].hasOpenChecklistItems = 'false'`
- `issue.property[SmartChecklist].itemsDates (=, >, <) 'date_iso'`
- `issue.property[SmartChecklist].itemsDates (=, >, <) 'date_dmy'`
- `issue.property[SmartChecklist].totalChecklistItems > item_count`
- `issue.property[SmartChecklist].totalChecklistItems <= item_count`
- `issue.property[SmartChecklist].totalChecklistItems = item_count`
- `issue.property[SmartChecklist].itemsStatus ~ 'Done'`
- `issue.property[SmartChecklist].itemsStatus ~ 'IN PROGRESS'`
- `issue.property[SmartChecklist].itemsStatus ~ 'custom_status'`
