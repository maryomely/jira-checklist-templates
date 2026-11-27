#!/usr/bin/env python3
"""Optional hook: regenerate, validate, test, and require regenerated files to be staged."""
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for script in ['rebuild_indexes.py', 'build_skill.py', 'validate_repository.py']:
    subprocess.run([sys.executable, str(ROOT/'tools'/script)], cwd=ROOT, check=True)
subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tools/tests'], cwd=ROOT, check=True)
# Never stage or silently include unrelated edits.
result = subprocess.run(['git', 'diff', '--exit-code', '--', 'templates/catalog.json', 'templates/index.json',
                         'llms.txt', 'docs/sources.md', 'templates', 'skills/write-jira-checklist.zip'], cwd=ROOT)
if result.returncode:
    print('Stage regenerated files and retry the commit. The hook did not stage anything.')
raise SystemExit(result.returncode)
