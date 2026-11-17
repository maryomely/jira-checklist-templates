#!/usr/bin/env python3
"""Rank template metadata; does not load all checklist bodies into an LLM context."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def search(query, entries, team=None, limit=10):
    tokens = re.findall(r'[a-z0-9]+', query.lower())
    ranked = []
    for entry in entries:
        if team and team.lower() not in entry['team'].lower(): continue
        title = entry['title'].lower()
        tags = ' '.join(entry['tags']).lower()
        summary = entry['summary'].lower()
        score = sum(5*(token in title) + 3*(token in tags) + (token in summary) + 2*(token in entry['team'].lower()) for token in tokens)
        lookup_ids = [entry['id'], *entry.get('superseded_ids', [])]
        if query.strip().lower() in {value.lower() for value in lookup_ids}: score += 100
        if score or not tokens: ranked.append((score, entry))
    ranked.sort(key=lambda pair:(-pair[0], pair[1]['id']))
    return [dict(entry, score=score) for score, entry in ranked[:limit]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--team')
    parser.add_argument('--limit', type=int, default=10)
    parser.add_argument('--json', action='store_true')
    args = parser.parse_args()
    if args.limit < 1: parser.error('--limit must be positive')
    entries = json.loads((ROOT/'catalog.json').read_text())['templates']
    results = search(args.query, entries, args.team, args.limit)
    if args.json: print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for entry in results:
            print(f"{entry['id']}  {entry['title']}  [{entry['team']}]\n  {entry['summary']}\n  {entry['path']}")
            if entry['notes']: print('  Note: ' + ' '.join(entry['notes']))
        if not results: print('No matching templates. Try a broader process name or omit --team.')


if __name__ == '__main__': main()
