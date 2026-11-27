#!/usr/bin/env python3
"""Conservative, dependency-free Smart Checklist checks; not the app parser."""
import argparse
import datetime
import html
import unicodedata
from urllib.parse import urlsplit, unquote
import json
import re
from pathlib import Path

PLACEHOLDER = re.compile(r'(?<![\w])([a-z][a-z0-9]*(?:_[a-z0-9]+)+)(?![\w])')



def emoji_base(char):
    return bool(char) and (0x1F000 <= ord(char) <= 0x1FAFF or
                           0x2190 <= ord(char) <= 0x23FF or 0x2600 <= ord(char) <= 0x27BF or 0x2B00 <= ord(char) <= 0x2BFF or char in '#*0123456789©®™‼⁉〰〽㊗㊙')


def unicode_findings(text):
    """Reject hidden controls; permit contextual emoji ZWJ and presentation selectors."""
    findings = []
    for index, char in enumerate(text):
        value = ord(char)
        previous = text[index-1] if index else ''
        following = text[index+1] if index+1 < len(text) else ''
        if char == '\u200d':
            base = text[index-2] if previous in ('\ufe0e', '\ufe0f') and index > 1 else previous
            allowed = emoji_base(base) and emoji_base(following)
        elif char in ('\ufe0e', '\ufe0f'):
            allowed = emoji_base(previous)
        else:
            forbidden = (unicodedata.category(char) in {'Cf', 'Cs', 'Zl', 'Zp'} or
                         (unicodedata.category(char) == 'Cc' and char not in '\t\r\n') or
                         (unicodedata.category(char) == 'Zs' and char != ' ') or
                         value in {0x034F, 0x115F, 0x1160, 0x17B4, 0x17B5, 0x2800, 0x3164, 0xFFA0} or
                         0xFE00 <= value <= 0xFE0D or 0xE0100 <= value <= 0xE01EF)
            allowed = not forbidden
        if not allowed:
            findings.append({'line': text.count('\n', 0, index)+1, 'severity': 'error',
                             'code': 'hidden-unicode',
                             'message': f'Remove unexpected U+{value:04X} {unicodedata.name(char, "control") }.'})
    return findings


def safe_destination(destination, allow_local=False):
    destination = html.unescape(destination.strip())
    if destination.startswith('<') and destination.endswith('>'):
        destination = destination[1:-1]
    destination = re.sub(r'\\([!"#$%&\'()*+,\-./:;<=>?@\[\]\\^_`{|}~])', r'\1', destination)
    decoded = unquote(destination)
    if unicode_findings(decoded) or any(ord(char) < 32 or ord(char) == 127 for char in decoded) or any(char.isspace() for char in destination):
        return False
    if re.fullmatch(r'[a-z][a-z0-9_]*_url', destination):
        return True
    try:
        parts = urlsplit(decoded)
        if parts.scheme:
            return parts.scheme.lower() == 'https' and bool(parts.hostname) and not any(char.isspace() for char in parts.hostname) and not parts.username and not parts.password
        return allow_local and not decoded.startswith(('//', '\\')) and bool(decoded)
    except ValueError:
        return False


def content_findings(text, allow_local=False):
    """Check visible Markdown destinations and HTML; this is not an injection detector."""
    findings = unicode_findings(html.unescape(text))
    visible = re.sub(r'```.*?```|`[^`\n]*`', '', text, flags=re.S)
    for number, line in enumerate(visible.splitlines(), 1):
        if re.search(r'<(?:/?[A-Za-z][A-Za-z0-9-]*(?:\s[^<>]*|/?)>|!--|!DOCTYPE|\?)', line, re.I):
            findings.append({'line':number, 'severity':'error', 'code':'raw-html', 'message':'Use checklist Markdown instead of raw HTML.'})
        destinations = []
        for match in re.finditer(r'(?<!\\)!?\[[^\]\n]*\]\(', line):
            start = end = match.end()
            depth = 1
            while end < len(line) and depth:
                if line[end] == '(' and line[end-1] != '\\': depth += 1
                if line[end] == ')' and line[end-1] != '\\': depth -= 1
                end += 1
            destinations.append(line[start:end-1] if not depth else line[start:])
        ref = re.match(r'^\s*\[[^\]]+\]:\s*(\S+)', line)
        if ref: destinations.append(ref.group(1))
        destinations += re.findall(r'<([A-Za-z][A-Za-z0-9+.-]*:[^<>]+)>', line)
        # Raw URLs and dangerous schemes must not bypass the inline-link checks.
        destinations += re.findall(r'\b(?:https?://|javascript:|data:|vbscript:|file:)[^\s<>`]+', line, re.I)
        for destination in destinations:
            if not safe_destination(destination, allow_local):
                findings.append({'line':number, 'severity':'error', 'code':'unsafe-link',
                                 'message':'Use an HTTPS destination or a documented URL placeholder.'})
    return findings


def find_placeholders(text, allowed_identifiers=()):
    """Find repository draft names, excluding real URLs and emoji shortcodes."""
    text = re.sub(r'https?://[^\s<>"`]+', '', text)
    text = re.sub(r':[a-z][a-z0-9_+-]*:', '', text)
    allowed = set(allowed_identifiers)
    return [name for name in PLACEHOLDER.findall(text) if name not in allowed]


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


def lint(text, ready=False, allowed_identifiers=()):
    findings = content_findings(text)
    allowed_identifiers = set(allowed_identifiers)
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
        # Do not mistake ordinary text starting with x (for example, xml) for a marker.
        if re.match(r'^x!(?! )', line):
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
                if not PLACEHOLDER.fullmatch(value) or value in allowed_identifiers:
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
        for placeholder in sorted(set(find_placeholders(line, allowed_identifiers))):
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
    parser.add_argument('--allow-identifier', action='append', default=[], metavar='NAME',
                        help='Treat this exact snake_case name as a literal identifier, not a placeholder. Repeat for multiple names.')
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        findings = lint(args.path.read_text(encoding='utf-8'), ready=args.ready,
                        allowed_identifiers=args.allow_identifier)
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
