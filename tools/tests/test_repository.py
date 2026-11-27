"""Exercise generation and validation in isolated repositories, never the working tree."""
import copy
import hashlib
import json
from pathlib import Path, PureWindowsPath
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
from rebuild_indexes import generated_files
from validate_repository import catalog_path, validate


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.path = 'templates/engineering/t001-review.md'
        self.body = '# Révision 🚀\n- Check `request_id` and `custom_field = "item_text"`\n- Read [evidence](evidence_url)\n'
        self.write(self.path, self.body)
        self.write('tools/index_sources/llms-intro.txt', '# Checklist guide\n\nFind a template.\n')
        self.write('skills/write-jira-checklist/references/formatting-guide.md', '# Formatting guide\n')
        self.catalog = {
            'schema_version': 1, 'format': 'smart-checklist-cloud-markdown',
            'reviewed_on': '2026-11-27', 'repository_url': 'https://example.org/repo',
            'description': 'Test repository',
            'templates': [{
                'id': 'T001', 'title': 'Révision', 'team': 'Engineering',
                'summary': 'Review a release.', 'tags': ['review'], 'kind': 'workflow',
                'path': self.path, 'source_urls': ['https://example.org/article'], 'notes': [],
                'literal_identifiers': ['request_id', 'custom_field'],
                'placeholders': [], 'item_count': 0, 'sha256': '',
            }],
            'sources': [{'url': 'https://example.org/article', 'title': 'Review guide'}],
        }
        self.regenerate()

    def write(self, relative, content):
        path = self.root/relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding='utf-8')

    def regenerate(self):
        files = generated_files(self.catalog, root=self.root)
        for relative, content in files.items():
            self.write(relative, content)
        return files

    def errors(self):
        return validate(self.root)[0]

    def test_generated_repository_validates_with_unicode_and_raw_placeholder_links(self):
        errors, warnings, count = validate(self.root)
        self.assertEqual(errors, [])
        self.assertEqual(dict(warnings), {})
        self.assertEqual(count, 1)

    def test_generation_is_repeatable_and_does_not_mutate_input(self):
        original = copy.deepcopy(self.catalog)
        first = self.regenerate()
        self.assertEqual(self.catalog, original)
        refreshed = json.loads(first['templates/catalog.json'])
        self.assertEqual(generated_files(refreshed, root=self.root), first)

    def test_generation_computes_content_metadata_and_applies_allow_list(self):
        generated = json.loads(self.regenerate()['templates/catalog.json'])
        entry = generated['templates'][0]
        self.assertEqual(entry['placeholders'], ['evidence_url', 'item_text'])
        self.assertEqual(entry['item_count'], 2)
        self.assertEqual(entry['sha256'], hashlib.sha256(self.body.encode('utf-8')).hexdigest())
        self.assertEqual(generated['template_count'], 1)
        self.assertEqual(generated['team_count'], 1)
        self.write(self.path, self.body + '- Confirm approval\n')
        changed = json.loads(self.regenerate()['templates/catalog.json'])['templates'][0]
        self.assertEqual(changed['item_count'], 3)
        self.assertNotEqual(changed['sha256'], entry['sha256'])

    def test_llms_prose_comes_from_source_and_teams_from_catalog(self):
        self.write('tools/index_sources/llms-intro.txt', '# Updated guide\n\nChoose carefully.\n')
        self.assertTrue(any('llms.txt: stale' in error for error in self.errors()))
        rendered = self.regenerate()['llms.txt']
        self.assertIn('Choose carefully.', rendered)
        self.assertIn('[Engineering](templates/engineering/README.md)', rendered)
        self.assertEqual(self.errors(), [])

    def test_manual_generated_edits_are_reported_as_stale(self):
        self.write('llms.txt', '# Manual edit\n')
        self.assertTrue(any('llms.txt: stale' in error for error in self.errors()))

    def test_missing_and_unlisted_template_files_are_reported(self):
        (self.root/self.path).unlink()
        errors = self.errors()
        self.assertTrue(any('Invalid template path' in error for error in errors))
        self.assertTrue(any('Catalog/file mismatch' in error for error in errors))
        self.write(self.path, self.body)
        self.write('templates/engineering/unlisted.md', '- Review\n')
        self.assertTrue(any('Catalog/file mismatch' in error for error in self.errors()))

    def test_missing_metadata_and_malformed_allow_list_are_reported(self):
        broken = json.loads((self.root/'templates/catalog.json').read_text(encoding='utf-8'))
        del broken['templates'][0]['path']
        self.write('templates/catalog.json', json.dumps(broken))
        self.assertTrue(any('schema:' in error for error in self.errors()))
        self.regenerate()
        broken = json.loads((self.root/'templates/catalog.json').read_text(encoding='utf-8'))
        broken['templates'][0]['literal_identifiers'] = 'request_id'
        self.write('templates/catalog.json', json.dumps(broken))
        self.assertTrue(any('literal_identifiers' in error for error in self.errors()))

    def test_duplicate_ids_and_paths_are_reported(self):
        broken = json.loads((self.root/'templates/catalog.json').read_text(encoding='utf-8'))
        broken['templates'].append(copy.deepcopy(broken['templates'][0]))
        self.write('templates/catalog.json', json.dumps(broken))
        self.assertIn('Duplicate template IDs.', self.errors())
        self.assertIn('Duplicate template paths.', self.errors())

    def test_broken_document_links_are_reported(self):
        self.write('README.md', '[Missing](missing.md)\n')
        self.assertTrue(any('broken local link missing.md' in error for error in self.errors()))

    def test_unsafe_catalog_paths_are_reported_without_generation(self):
        broken = json.loads((self.root/'templates/catalog.json').read_text(encoding='utf-8'))
        broken['templates'][0]['path'] = '../outside.md'
        self.write('templates/catalog.json', json.dumps(broken))
        self.assertTrue(any('schema:' in error for error in self.errors()))

    def test_windows_paths_match_catalog_forward_slashes(self):
        root = PureWindowsPath('C:/repository')
        path = root/'templates'/'engineering'/'t001-review.md'
        self.assertEqual(catalog_path(path, root), self.path)


if __name__ == '__main__':
    unittest.main()
