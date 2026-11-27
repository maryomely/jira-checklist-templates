import importlib.util
import json
import sys
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
from search_templates import search

spec = importlib.util.spec_from_file_location('lint_checklist', ROOT/'skills/write-jira-checklist/scripts/lint_checklist.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
lint = module.lint


class ChecklistSyntaxTests(unittest.TestCase):
    def errors(self, text, ready=False):
        return {f['code'] for f in lint(text, ready) if f['severity'] == 'error'}

    def test_supported_states_and_header_details(self):
        text = '## Stage\n> Section context\n- Prepare\n> * Evidence\n> > * Build identifier\n~! Review\n+ Complete\nx Skip\n'
        self.assertEqual(self.errors(text), set())

    def test_generic_checkbox_is_not_silently_accepted(self):
        self.assertIn('github-checkbox', self.errors('- [ ] Review the release'))
        self.assertIn('github-checkbox', self.errors('- [x] Review the release'))

    def test_all_mandatory_markers_require_space(self):
        for marker in '-+~x':
            with self.subTest(marker=marker):
                self.assertIn('status-space', self.errors(f'{marker}!Approve\n- Review'))
                self.assertEqual(self.errors(f'{marker}! Approve'), set())
        self.assertEqual(self.errors('xml is the input format\n- Review'), set())

    def test_allow_list_preserves_unresolved_query_values(self):
        text = '- Check `custom_field = "item_text"` and log `request_id`'
        findings = lint(text, ready=True, allowed_identifiers=['custom_field', 'request_id'])
        placeholders = [f for f in findings if f['code'] == 'placeholder']
        self.assertEqual(len(placeholders), 1)
        self.assertEqual(placeholders[0]['severity'], 'error')
        self.assertIn('item_text', placeholders[0]['message'])
        self.assertEqual(lint(text.replace('item_text', 'approved'), ready=True,
                              allowed_identifiers=['custom_field', 'request_id']), [])

    def test_allow_list_is_exact_and_does_not_skip_attribute_validation(self):
        self.assertEqual(module.find_placeholders('request_id request_id_suffix', ['request_id']),
                         ['request_id_suffix'])
        findings = lint('- [dueDate="not_a_date"] Review', ready=True,
                        allowed_identifiers=['not_a_date'])
        self.assertTrue(any(f['code'] == 'date' for f in findings))

    def test_cli_allow_list_and_exit_status(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)/'draft.md'
            path.write_text('- Check `request_id` and `custom_field`\n', encoding='utf-8')
            command = [sys.executable, str(ROOT/'skills/write-jira-checklist/scripts/lint_checklist.py'),
                       str(path), '--ready', '--json']
            unresolved = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(unresolved.returncode, 1)
            resolved = subprocess.run(command + ['--allow-identifier', 'request_id',
                                                '--allow-identifier', 'custom_field'],
                                      capture_output=True, text=True)
            self.assertEqual(resolved.returncode, 0, resolved.stderr)
            self.assertEqual(json.loads(resolved.stdout), [])

    def test_mandatory_asterisk_error_and_real_marker(self):
        self.assertIn('asterisk-marker', self.errors('- *Approve release'))
        self.assertEqual(self.errors('-! Approve release'), set())

    def test_real_calendar_dates_and_attribute_values(self):
        self.assertEqual(self.errors('- [dueDate="2028-02-29"][priority="High"][assignee="abc:123"] Review'), set())
        self.assertIn('date', self.errors('- [dueDate="2027-02-29"] Review'))
        self.assertIn('date', self.errors('- [dueDate="29/02/2028"] Review'))
        self.assertIn('priority', self.errors('- [priority="Urgent"] Review'))
        self.assertIn('attribute-format', self.errors('- [dueDate=“2028-02-29”] Review'))
        self.assertIn('duplicate-attribute', self.errors('- [priority="High"][priority="Low"] Review'))

    def test_placeholders_are_draft_only(self):
        text = '- [assignee="qa_user_id"][dueDate="qa_due_date"] Check [evidence](evidence_url)'
        self.assertEqual(self.errors(text), set())
        self.assertIn('placeholder', self.errors(text, ready=True))
        self.assertIn('placeholder-format', self.errors('- Review {{Due Date}}'))

    def test_typed_values_preserve_syntax_when_resolved(self):
        draft = ('- [assignee="qa_user_id"][dueDate="review_due_date"] Review the release\n'
                 '> Read [the test report](test_report_url) and ask @reviewer_user_id for feedback.\n'
                 '> Compare the result with ![the approved design](design_image_url).\n')
        self.assertEqual(self.errors(draft), set())
        self.assertIn('placeholder', self.errors(draft, ready=True))
        values = {'qa_user_id':'712020:example-qa-id', 'review_due_date':'2028-02-29',
                  'test_report_url':'https://example.org/reports/release',
                  'reviewer_user_id':'712020:example-reviewer-id',
                  'design_image_url':'https://example.org/images/design.png'}
        resolved = draft
        for key, value in values.items():
            resolved = resolved.replace(key, value)
        self.assertEqual(lint(resolved, ready=True), [])
        self.assertIn('date', self.errors(resolved.replace('2028-02-29','2027-02-29'), ready=True))
        self.assertIn('assignee', self.errors(resolved.replace('712020:example-qa-id','QA Lead'), ready=True))
        self.assertIn('link', self.errors(resolved.replace('https://example.org/images/design.png',''), ready=True))

    def test_link_url_placeholders_are_not_ready_urls(self):
        for text in ['- Read [guide](guide_url)', '- Inspect ![diagram](diagram_url)']:
            with self.subTest(text=text):
                self.assertEqual(self.errors(text), set())
                self.assertIn('placeholder', self.errors(text, ready=True))
        self.assertEqual(self.errors('- Read [guide](https://example.org/guide_url)', ready=True), set())

    def test_catalog_preserves_unbraced_link_placeholders(self):
        catalog = json.loads((ROOT/'templates/catalog.json').read_text(encoding='utf-8'))
        incident = next(e for e in catalog['templates'] if e['id'] == 'T028')
        self.assertIn('incident_log_url', incident['placeholders'])

    def test_all_placeholder_types_remain_detectable_without_braces(self):
        draft = ('## Review by review_date\n'
                 '- Welcome employee_name and notify @team_mention\n'
                 '- [dueDate="due_date"][assignee="assignee_user_id"] Review\n'
                 '- Search `cf[custom_field_id] ~ "item_text"`\n'
                 '- Confirm approval_threshold currency_code for calendar_year')
        expected = {'review_date', 'employee_name', 'team_mention', 'due_date',
                    'assignee_user_id', 'custom_field_id', 'item_text',
                    'approval_threshold', 'currency_code', 'calendar_year'}
        self.assertEqual(set(module.find_placeholders(draft)), expected)
        self.assertEqual(self.errors(draft), set())
        self.assertIn('placeholder', self.errors(draft, ready=True))
        self.assertIn('placeholder-format', self.errors('- Review {{due_date}}'))

    def test_real_urls_emoji_and_ordinary_prose_are_not_placeholders(self):
        text = ('- Plan the year and confirm currency :white_check_mark: @QA_Lead\n'
                '- Read [guide](https://example.org/a_(b)/review_date)\n'
                '- [dueDate="2029-03-28"] Review')
        self.assertEqual(module.find_placeholders(text), [])
        self.assertEqual(self.errors(text, ready=True), set())

    def test_owner_required_but_standalone_text_is_supported(self):
        self.assertIn('orphan-detail', self.errors('> Unattached\n- Review'))
        self.assertEqual(self.errors('Context\n> More context\n- Review'), set())

    def test_links_with_parentheses_and_missing_closers(self):
        self.assertEqual(self.errors('- Read [guide](https://example.org/a_(b))'), set())
        self.assertIn('link', self.errors('- Read [guide](https://example.org/a'))
        self.assertIn('link', self.errors('- Read [guide]()'))

    def test_code_and_escaped_labels_survive(self):
        text = '- \\[Production\\] Check `issue.property[SmartChecklist]`\n- Verify `*` and `-!` are shown'
        self.assertEqual(lint(text), [])

    def test_custom_status_is_a_configuration_warning(self):
        findings = lint('- [In Review] Review evidence')
        self.assertEqual(self.errors('- [In Review] Review evidence'), set())
        self.assertTrue(any(f['code']=='custom-status' and f['severity']=='warning' for f in findings))


class DiscoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = json.loads((ROOT/'templates/catalog.json').read_text(encoding='utf-8'))['templates']

    def test_exact_id_lookup(self):
        self.assertEqual(search('T017', self.entries)[0]['id'], 'T017')

    def test_search_cli_finds_relocated_index_outside_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(ROOT/'tools/search_templates.py'), 'T010', '--json'],
                cwd=directory, capture_output=True, text=True,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        entries = json.loads(result.stdout)
        self.assertEqual(entries[0]['id'], 'T008')
        self.assertTrue((ROOT/entries[0]['path']).is_file())

    def test_consolidated_ids_resolve_to_successor(self):
        active_ids = {entry['id'] for entry in self.entries}
        for old_id, successor in [('T010', 'T008'), ('T022', 'T008'), ('T068', 'T070'), ('T069', 'T070')]:
            with self.subTest(old_id=old_id):
                self.assertNotIn(old_id, active_ids)
                self.assertEqual(search(old_id.lower(), self.entries)[0]['id'], successor)

    def test_new_tutorial_is_discoverable(self):
        self.assertEqual(search('get started', self.entries)[0]['id'], 'T082')

    def test_team_filter_and_relevant_workflow(self):
        found = search('onboarding', self.entries, team='HR and Recruiting')
        self.assertTrue(found)
        self.assertTrue(all(e['team']=='HR and Recruiting' for e in found))
        self.assertIn('T008', [e['id'] for e in found])

    def test_general_regression_precedes_product_example(self):
        self.assertEqual(search('general regression', self.entries)[0]['id'], 'T073')
        product = next(e for e in self.entries if e['id']=='T075')
        self.assertEqual(product['kind'], 'product-regression-example')
        self.assertTrue(product['notes'])

    def test_search_matches_whole_words(self):
        entries = [dict(self.entries[0], id='T900', title='Qatar launch', tags=[],
                        summary='Prepare launch', team='Marketing'),
                   dict(self.entries[0], id='T901', title='QA review', tags=[],
                        summary='Check release', team='Quality Assurance')]
        self.assertEqual([e['id'] for e in search('qa', entries)], ['T901'])

    def test_search_normalizes_common_plurals(self):
        for singular, plural in [('release', 'releases'), ('checklist', 'checklists'),
                                 ('policy', 'policies'), ('process', 'processes')]:
            with self.subTest(query=singular):
                self.assertEqual(search(singular, self.entries), search(plural, self.entries))

    def test_team_filter_is_exact_but_ignores_case_and_whitespace(self):
        self.assertEqual(search('', self.entries, team='IT'), [])
        self.assertEqual(search('', self.entries, team='security'), [])
        found = search('', self.entries, team='  information   SECURITY ')
        self.assertTrue(found)
        self.assertTrue(all(e['team'] == 'Information Security' for e in found))

    def test_empty_query_limit_and_duplicate_words(self):
        self.assertEqual(len(search('', self.entries, limit=3)), 3)
        self.assertEqual(search('release release', self.entries), search('release', self.entries))


if __name__ == '__main__': unittest.main()
