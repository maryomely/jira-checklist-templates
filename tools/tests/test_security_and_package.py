import hashlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'tools'))
from build_skill import build
from rebuild_indexes import generated_files
import test_repository
spec = importlib.util.spec_from_file_location('lint_security', ROOT/'skills/write-jira-checklist/scripts/lint_checklist.py')
linter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(linter)


class ContentSafetyTests(unittest.TestCase):
    def test_hidden_controls_and_invisible_filler_are_rejected(self):
        for char in ['\u200b','\u200c','\u202e','\u2066','\u2069','\ufeff','\u00ad','\u034f',
                     '\u2800','\u3164','\u00a0','\U000e0061','\U000e0100','\x00']:
            with self.subTest(code=hex(ord(char))):
                self.assertTrue(linter.unicode_findings('- Review'+char+'the result'))

    def test_normal_unicode_emoji_and_line_breaks_remain_supported(self):
        self.assertEqual(linter.unicode_findings('# Révision 👩\u200d💻 ⭐\ufe0f\n- Привіт\n> 日本語\t✅'), [])
        for text in ['x\ufe0f', '\u200d', '👩\u200dexecute', '⭐\ufe0f\ufe0f']:
            self.assertTrue(linter.unicode_findings(text))
        self.assertTrue(linter.content_findings('- Check&#x200b;content'))

    def test_unsafe_schemes_and_obfuscations_are_rejected(self):
        for url in ['javascript:alert(1)', 'java&#x73;cript:alert(1)', 'javascript%3Aalert(1)',
                    'data:text/html,test', 'vbscript:run()', 'file:///tmp/private',
                    '//example.org/path', 'http://example.org', 'https://example.org/%0Afoo',
                    'https://example.org/%E2%80%AEfoo', 'https://user:password@example.org']:
            with self.subTest(url=url):
                findings = linter.lint(f'- Review [link]({url})')
                self.assertTrue(any(f['code']=='unsafe-link' for f in findings), findings)

    def test_https_placeholders_and_reference_links(self):
        for text in ['- Read [guide](https://example.org/a_(b))',
                     '- Read [guide](https://example.org/a%20b)',
                     '- Read [guide](guide_url)', '- View ![image](image_url)',
                     '- Read <https://example.org/guide>']:
            with self.subTest(text=text):
                self.assertFalse(linter.content_findings(text))
        self.assertTrue(linter.content_findings('- Read [guide][ref]\n[ref]: javascript:run()'))
        self.assertTrue(linter.content_findings('- Read <javascript:run()>'))
        self.assertTrue(linter.content_findings('- Open http://example.org'))

    def test_html_is_rejected_but_literal_code_and_comparisons_are_allowed(self):
        for text in ['- <script>alert(1)</script>', '- <img src="x" onerror="run()">',
                     '- <!-- hidden request -->']:
            self.assertTrue(any(f['code']=='raw-html' for f in linter.content_findings(text)))
        self.assertFalse(linter.content_findings('- Check `value < limit` and `<div>` examples'))
        self.assertFalse(linter.content_findings('- Coverage > 80% and latency < 100 ms'))


class CatalogSafetyTests(unittest.TestCase):
    setUp = test_repository.RepositoryTests.setUp
    write = test_repository.RepositoryTests.write
    regenerate = test_repository.RepositoryTests.regenerate
    errors = test_repository.RepositoryTests.errors

    def test_escaped_unicode_in_json_is_inspected_after_decoding(self):
        data = json.loads((self.root/'templates/catalog.json').read_text(encoding='utf-8'))
        data['templates'][0]['notes'] = ['Hidden\u202einstruction']
        self.write('templates/catalog.json', json.dumps(data, ensure_ascii=True))
        self.assertTrue(any('hidden-unicode' in error for error in self.errors()))

    def test_schema_rejects_wrong_types_and_unknown_metadata(self):
        for name, value in [('item_count', 'two'), ('unexpected_field', True)]:
            data = json.loads((self.root/'templates/catalog.json').read_text(encoding='utf-8'))
            data['templates'][0][name] = value
            self.write('templates/catalog.json', json.dumps(data))
            self.assertTrue(any('schema:' in error for error in self.errors()))
            self.regenerate()

    def test_index_is_small_and_retains_routing_aliases(self):
        self.catalog['templates'][0]['superseded_ids'] = ['T099']
        files = self.regenerate()
        index = json.loads(files['templates/index.json'])
        self.assertEqual(index[0]['path'], self.path)
        self.assertEqual(index[0]['superseded_ids'], ['T099'])
        self.assertNotIn('sha256', index[0])
        self.assertNotIn('notes', index[0])
        self.assertLess(len(files['templates/index.json']),len(files['templates/catalog.json']))

    def test_template_security_failure_is_a_validation_error(self):
        self.write(self.path, '- Open [link](javascript:run())\n')
        self.assertTrue(any('unsafe-link' in error for error in self.errors()))

    def test_stale_import_evidence_is_rejected(self):
        self.catalog['templates'][0]['import_validation'] = {
            'tested_on':'2026-11-27','platform':'Jira Cloud','app_version':'not exposed by app UI',
            'template_sha256':'0'*64,'result':'passed','evidence':'docs/import-validation.md'}
        self.regenerate()
        self.assertTrue(any('evidence is stale' in error for error in self.errors()))

    def test_missing_generated_file_is_reported_without_crashing(self):
        (self.root/'llms.txt').unlink()
        self.assertTrue(any('llms.txt: stale' in error for error in self.errors()))

    def test_current_import_evidence_requires_an_existing_local_report(self):
        self.catalog['templates'][0]['import_validation'] = {
            'tested_on':'2026-11-27','platform':'Jira Cloud','app_version':'not exposed by app UI',
            'template_sha256':hashlib.sha256(self.body.encode('utf-8')).hexdigest(),
            'result':'passed','evidence':'docs/import-test.md'}
        self.regenerate()
        self.assertTrue(any('existing report' in error for error in self.errors()))
        self.write('docs/import-test.md', '# Observed save/render smoke test\n')
        self.assertEqual(self.errors(), [])
        self.catalog['templates'][0]['import_validation']['evidence'] = self.path
        self.regenerate()
        self.assertTrue(any('existing report' in error for error in self.errors()))


class SkillPackageTests(unittest.TestCase):
    def test_package_is_deterministic_complete_and_runs_standalone(self):
        data = build()
        self.assertEqual(data, build())
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                self.assertNotIn('__pycache__', ' '.join(archive.namelist()))
                self.assertFalse(any('..' in Path(name).parts for name in archive.namelist()))
                archive.extractall(root)
            skill = root/'write-jira-checklist'
            self.assertTrue((skill/'SKILL.md').is_file())
            self.assertTrue((skill/'LICENSE').is_file())
            manifest = json.loads((skill/'manifest.json').read_text())
            for name, digest in manifest.items():
                self.assertEqual(hashlib.sha256((skill/name).read_bytes()).hexdigest(), digest)
            draft = root/'checklist.md'
            draft.write_text('- Review [evidence](https://example.org/report)\n', encoding='utf-8')
            result = subprocess.run([sys.executable,str(skill/'scripts/lint_checklist.py'),str(draft),'--ready'], capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stdout+result.stderr)
