#!/usr/bin/env python3
"""Conservative, dependency-free Smart Checklist checks; not the app parser."""
import argparse
import datetime
import json
import re
from pathlib import Path

PLACEHOLDER = re.compile(r'(?<![\w])([a-z][a-z0-9]*(?:_[a-z0-9]+)+)(?![\w])')


def find_placeholders(text):
    """Find repository draft names, excluding real URLs and emoji shortcodes."""
    text = re.sub(r'https?://[^\s<>"`]+', '', text)
    text = re.sub(r':[a-z][a-z0-9_+-]*:', '', text)
    return PLACEHOLDER.findall(text)


ITEM = re.compile(r'^([-+~x])(!?) (.*)$')
ATTRIBUTE = re.compile(r'^\[(priority|dueDate|assignee)="([^"\n]*)"\]')


def without_links(text):
    """Remove balanced inline links, returning malformed-link locations separately."""
    errors = []
    cursor = 0
    chunks = []
    pattern = re.compile(r'(?<!\\)!?\[[^\]\n]+\]\(')
    while match := pattern.search(text, cursor):
        chunks.append(text[cursor:match.start()])
        end = match.end()
        depth = 1
        while end < len(text) and depth:
            if text[end] == '(' and text[end-1] != '\\': depth += 1
            if text[end] == ')' and text[end-1] != '\\': depth -= 1
            end += 1
        if depth:
            errors.append('Close the link destination with a parenthesis.')
        else:
            destination = text[match.end():end-1]
            if not destination or re.search(r'\s', destination):
                errors.append('Use a nonempty link destination without raw whitespace.')
        cursor = end
    chunks.append(text[cursor:])
    return ''.join(chunks), errors


def lint(text, ready=False):
    findings = []
    owner = False
    items = 0

    def add(line, code, message, severity='error'):
        findings.append({'line': line, 'severity': severity, 'code': code, 'message': message})

    for number, line in enumerate(text.splitlines(), 1):
        if not line.strip(): continue
        if line.startswith(('```', '~~~')):
            add(number, 'code-fence', 'Remove wrapping code fences from the raw checklist file.')
            continue
        if line == '---' and number == 1:
            add(number, 'frontmatter', 'Keep YAML metadata outside the checklist payload.')
        if re.match(r'^\s+[-+~x]!? ', line):
            add(number, 'indented-item', 'Use a top-level item or > detail list; do not indent checkable items.')
        if re.match(r'^#{7,}(?: |$)', line):
            add(number, 'heading-level', 'Use at most six heading markers.')
        if re.match(r'^#{1,6}[^#\s]', line):
            add(number, 'heading-space', 'Add a space after the heading markers.')
        if re.match(r'^[-+~](?:!)?\S', line) and not line.startswith('---'):
            # A valid mandatory marker has a space after !.
            if not re.match(r'^[-+~]! ', line):
                add(number, 'status-space', 'Add a space after the status or mandatory marker.')
        item = ITEM.match(line)
        body = line
        if item:
            owner = True
            items += 1
            body = item.group(3)
            if not body.strip(): add(number, 'empty-item', 'Give the checklist item a meaningful action or result.')
            if re.match(r'^\[(?: |x|X)\](?: |$)', body):
                add(number, 'github-checkbox', 'Use - for To Do or + for Done, without a GitHub checkbox.')
            if re.match(r'^\*\s', body) or (body.startswith('*') and body.count('*') == 1):
                add(number, 'asterisk-marker', 'Use -! for a mandatory item; a leading asterisk is not a mandatory marker.')
            # Attributes precede text. Allow a configured custom status before them.
            custom_status = re.match(r'^\[([^\]\n=]+)\](?!\()', body)
            if custom_status and not re.match(r'^\[(?: |x|X)\]', body):
                add(number, 'custom-status', f'Confirm that custom status {custom_status.group(1)!r} exists; escape brackets for a literal label.', 'warning')
                body = body[custom_status.end():].lstrip()
            seen = set()
            while body.startswith('['):
                attribute = ATTRIBUTE.match(body)
                if not attribute:
                    if re.match(r'^\[(?:priority|dueDate|assignee)\s*=', body):
                        add(number, 'attribute-format', 'Use a supported attribute name and straight double-quoted value.')
                    break
                key, value = attribute.groups()
                if key in seen: add(number, 'duplicate-attribute', f'Use {key} only once per item.')
                seen.add(key)
                if not value: add(number, 'empty-attribute', f'{key} must not be empty.')
                if not PLACEHOLDER.fullmatch(value):
                    if key == 'priority' and value not in {'High', 'Medium', 'Low'}:
                        add(number, 'priority', 'Priority must be High, Medium, or Low.')
                    if key == 'dueDate':
                        try:
                            if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value): raise ValueError()
                            datetime.date.fromisoformat(value)
                        except ValueError:
                            add(number, 'date', 'Use a real calendar date in YYYY-MM-DD format.')
                    if key == 'assignee' and re.search(r'\s', value):
                        add(number, 'assignee', 'Use a Jira user ID, not a display name with spaces.')
                body = body[attribute.end():].lstrip()
            if not body: add(number, 'empty-item', 'Add item text after the attributes.')
        elif line.startswith('>'):
            if not owner: add(number, 'orphan-detail', 'Place details after an item, header, or text owner.')
            if not line.startswith('> '):
                add(number, 'detail-space', 'Prefer a space after > for consistent detail formatting.', 'warning')
            body = re.sub(r'^>\s*(?:>\s*)?[*-]?\s*', '', line)
        else:
            # Both headers and standalone text may own details.
            owner = True
        if '#must' in line:
            add(number, 'literal-must', '#must is descriptive text, not a mandatory flag. Use -! if enforcement is intended.', 'warning')
        if '{{' in line or '}}' in line:
            add(number, 'placeholder-format', 'Remove curly brackets from placeholders; use bare lowercase_snake_case names.')
        for placeholder in sorted(set(find_placeholders(line))):
            add(number, 'placeholder', f'Replace {placeholder} before pasting into Jira.', 'error' if ready else 'info')
        if body.count('`') % 2:
            add(number, 'code-span', 'Balance inline backticks on the same line.')
        visible = re.sub(r'`[^`]*`', '', body)
        visible, link_errors = without_links(visible)
        for message in link_errors: add(number, 'link', message)
        visible = visible.replace(r'\[', '').replace(r'\]', '')
        if '[' in visible or ']' in visible:
            add(number, 'literal-brackets', 'Escape literal brackets or use a balanced link or code span.', 'warning')
        # Stars used as bullet syntax have already been removed from detail lines.
        if len(re.findall(r'(?<!\\)\*', visible)) % 2:
            add(number, 'emphasis', 'Check unmatched emphasis or protect a literal asterisk with a code span.', 'warning')
    if not items: add(1, 'no-items', 'Include at least one checkable item.')
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    parser.add_argument('--ready', action='store_true', help='Treat unresolved placeholders as errors.')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        findings = lint(args.path.read_text(encoding='utf-8'), ready=args.ready)
    except (OSError, UnicodeError) as error:
        parser.error(str(error))
    if args.json:
        print(json.dumps(findings, indent=2))
    else:
        for finding in findings:
            print(f"{args.path}:{finding['line']}: {finding['severity']} [{finding['code']}] {finding['message']}")
        print(f"{sum(f['severity']=='error' for f in findings)} errors; {sum(f['severity']=='warning' for f in findings)} warnings; {sum(f['severity']=='info' for f in findings)} placeholders")
    return 1 if any(f['severity'] == 'error' for f in findings) else 0


if __name__ == '__main__':
    raise SystemExit(main())
