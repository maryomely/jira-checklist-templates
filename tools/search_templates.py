#!/usr/bin/env python3
"""Rank template metadata; does not load all checklist bodies into an LLM context."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def normalize_word(word):
    """Fold common English plurals; deliberately avoid aggressive verb stemming."""
    if len(word) > 4 and word.endswith('ies'):
        return word[:-3] + 'y'
    if len(word) > 4 and word.endswith(('sses', 'ches', 'shes', 'xes', 'zes')):
        return word[:-2]
    if len(word) > 3 and word.endswith('s') and not word.endswith(('ss', 'us', 'is')):
        return word[:-1]
    return word


def words(text):
    return {normalize_word(word) for word in re.findall(r'[a-z0-9]+', text.casefold())}


def team_name(text):
    return ' '.join(text.casefold().split())


def search(query, entries, team=None, limit=10):
    tokens = words(query)
    ranked = []
    for entry in entries:
        if team and team_name(team) != team_name(entry['team']): continue
        title = words(entry['title'])
        tags = words(' '.join(entry['tags']))
        summary = words(entry['summary'])
        team_words = words(entry['team'])
        score = sum(5*(token in title) + 3*(token in tags) + (token in summary) + 2*(token in team_words) for token in tokens)
        lookup_ids = [entry['id'], *entry.get('superseded_ids', [])]
        if query.strip().lower() in {value.lower() for value in lookup_ids}: score += 100
        if score or not tokens: ranked.append((score, entry))
    ranked.sort(key=lambda pair:(-pair[0], pair[1]['id']))
    return [dict(entry, score=score) for score, entry in ranked[:limit]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--team', help='Full team name; case and repeated whitespace are ignored.')
    parser.add_argument('--limit', type=int, default=10)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if args.limit < 1: parser.error('--limit must be positive')
    entries = json.loads((ROOT/'templates/index.json').read_text(encoding='utf-8'))
    results = search(args.query, entries, args.team, args.limit)
    if args.json: print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for entry in results:
            print(f"{entry['id']}  {entry['title']}  [{entry['team']}]\n  {entry['summary']}\n  {entry['path']}")
            print('  Read full catalog notes before adapting this template.')
        if not results: print('No matching templates. Try a broader process name or omit --team.')


if __name__ == '__main__': main()
