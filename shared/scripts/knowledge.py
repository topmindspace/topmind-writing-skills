#!/usr/bin/env python3
"""Search small knowledge catalogs, read selected cards, or capture a candidate locally.

Standard library only. No network, global discovery, execution of card contents,
implicit promotion, or writes to the bundled knowledge pack.
"""
from __future__ import annotations

import argparse
from datetime import date
import json
import os
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
BUNDLED = ROOT / 'knowledge'
SKILLS = {'topmind-briefs', 'topmind-cover', 'topmind-format', 'topmind-poster',
          'topmind-revise', 'topmind-viral-posts', 'topmind-wechat-post', 'topmind-x-article'}
KINDS = {'direction', 'technique', 'example', 'case', 'lesson'}
EVIDENCE = {'illustrative', 'observed', 'sourced', 'user-confirmed', 'unverified'}
STATES = {'candidate', 'active', 'retired'}
ID = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')


def card_path(root, value):
    rel = PurePosixPath(value)
    if rel.is_absolute() or '..' in rel.parts or '\\' in value or rel.suffix != '.md':
        raise ValueError(f'Invalid card path: {value}')
    target = (root / value).resolve()
    if not target.is_relative_to(root.resolve()):
        raise ValueError(f'Card escapes pack directory: {value}')
    return target


def validate(data, root, check_bodies=True):
    if not isinstance(data, dict) or data.get('schema_version') != 1:
        raise ValueError('Knowledge catalog requires schema_version=1')
    if not ID.fullmatch(str(data.get('id', ''))) or not isinstance(data.get('version'), str):
        raise ValueError('Pack requires a stable id and string version')
    if not isinstance(data.get('entries'), list):
        raise ValueError('Pack requires an entries list')
    ids, paths = set(), set()
    for item in data['entries']:
        if not isinstance(item, dict):
            raise ValueError('Each entry must be an object')
        ident = item.get('id', '')
        if not isinstance(ident, str) or not ID.fullmatch(ident) or ident in ids:
            raise ValueError(f'Invalid or duplicate card id: {ident}')
        ids.add(ident)
        for field in ['title', 'summary', 'scope', 'limits', 'path']:
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f'{ident}: requires nonempty {field}')
        for field in ['skills', 'tags']:
            value = item.get(field)
            if not isinstance(value, list) or not value or any(not isinstance(v, str) or not v.strip() for v in value):
                raise ValueError(f'{ident}: requires a nonempty string list: {field}')
        if not set(item['skills']) <= SKILLS | {'*'}:
            raise ValueError(f'{ident}: unknown skill')
        for field, choices in [('kind', KINDS), ('evidence', EVIDENCE), ('status', STATES)]:
            if item.get(field) not in choices:
                raise ValueError(f'{ident}: invalid {field}')
        sources = item.get('sources')
        if not isinstance(sources, list) or not sources or any(
                not isinstance(s, dict) or not isinstance(s.get('ref'), str) or not s['ref'].strip()
                or s.get('kind') not in {'original', 'source', 'observation', 'feedback'} for s in sources):
            raise ValueError(f'{ident}: requires source/provenance records')
        target = card_path(root, item['path'])
        if target in paths or not target.is_file() or (not target.read_text(encoding='utf-8').strip() if check_bodies else target.stat().st_size == 0):
            raise ValueError(f'{ident}: duplicate, missing or empty card: {item["path"]}')
        paths.add(target)
    return data


def load(root, check_bodies=False):
    root = Path(root).resolve()
    index = (root / 'index.json').resolve()
    if not index.is_relative_to(root):
        raise ValueError('Catalog escapes pack directory')
    with index.open(encoding='utf-8') as stream:
        data = json.load(stream)
    return root, validate(data, root, check_bodies)


def tokens(text):
    result = set()
    for word in re.findall(r'[a-z0-9][a-z0-9_-]*|[\u3400-\u9fff]+', text.lower()):
        result.add(word)
        if re.fullmatch(r'[\u3400-\u9fff]+', word):
            result.update(word[i:i + 2] for i in range(len(word) - 1))
    return result


def search(packs, query, skill, include_candidates=False, limit=5):
    wanted = tokens(query)
    found = []
    for root, data in packs:
        for item in data['entries']:
            if item['status'] != 'active' and not (include_candidates and item['status'] == 'candidate'):
                continue
            if skill != 'all' and skill not in item['skills'] and '*' not in item['skills']:
                continue
            score, matched = 0, set()
            for field, weight in [('title', 6), ('tags', 5), ('summary', 3), ('scope', 1)]:
                value = ' '.join(item[field]) if isinstance(item[field], list) else item[field]
                hits = wanted & tokens(value)
                score += len(hits) * weight
                matched.update(hits)
            if not score:
                continue
            result = {**item, 'key': f'{data["id"]}:{item["id"]}',
                      'file': str(card_path(root, item['path'])), 'matched': sorted(matched)}
            found.append((score, result))
    found.sort(key=lambda pair: (-pair[0], pair[1]['key']))
    return [item for _, item in found[:limit]]


def read_card(packs, key, max_chars):
    matches = [(root, data, item) for root, data in packs for item in data['entries']
               if key in (item['id'], f'{data["id"]}:{item["id"]}')]
    if len(matches) != 1:
        raise ValueError('Card not found or id is ambiguous; use pack-id:card-id from search')
    root, data, item = matches[0]
    body = card_path(root, item['path']).read_text(encoding='utf-8')
    header = f'{data["id"]}:{item["id"]} | {item["status"]} | evidence={item["evidence"]}\nScope: {item["scope"]}\nLimits: {item["limits"]}\n'
    text = header + body
    if len(text) > max_chars:
        text = text[:max_chars] + f'\n[Truncated; {len(text)} characters total. Raise --max-chars or read the named file.]'
    return text


def add_candidate(args):
    if len(args.pack or []) != 1:
        raise ValueError('add requires exactly one explicit --pack output directory')
    root = Path(args.pack[0]).resolve()
    if root == BUNDLED.resolve() or (root.parent / 'SKILL.md').is_file() or (
            root.parent.name == 'shared' and (root.parent / 'manifest.json').is_file()):
        raise ValueError('add cannot modify a bundled pack; use a separate explicit local pack')
    if not ID.fullmatch(args.id):
        raise ValueError('Card id must be lowercase words separated by hyphens')
    body = Path(args.body).read_text(encoding='utf-8')
    if not body.strip():
        raise ValueError('Candidate body is empty')
    skills = [s.strip() for s in args.skills.split(',') if s.strip()]
    if not skills or not set(skills) <= SKILLS | {'*'}:
        raise ValueError('Unknown or empty --skills')
    tags = [s.strip() for s in args.tags.split(',') if s.strip()]
    if not tags:
        raise ValueError('At least one tag is required')
    path = f'cards/{args.id}.md'
    target = card_path(root, path)
    if target.exists():
        raise ValueError('Card already exists; add never overwrites a card')
    item = dict(id=args.id, title=args.title, summary=args.summary, skills=skills,
                tags=tags, kind=args.kind, status='candidate', evidence='unverified',
                scope=args.scope, limits=args.limits, path=path,
                sources=[{'kind': 'source' if args.source else 'original',
                          'ref': args.source or 'Local task note; not externally verified'}],
                updated=date.today().isoformat())
    root.mkdir(parents=True, exist_ok=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    lock = root / '.write-lock'
    lock.mkdir()  # refuse concurrent writers instead of losing a candidate
    temporary = None
    created = False
    try:
        data = load(root)[1] if (root / 'index.json').exists() else {
            'schema_version': 1, 'id': args.pack_id, 'version': '0.1.0', 'entries': []}
        if any(entry['id'] == args.id for entry in data['entries']):
            raise ValueError('Card id already exists')
        with target.open('x', encoding='utf-8') as stream:
            created = True
            stream.write(body)
        data['entries'].append(item)
        validate(data, root)
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=root, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
        os.replace(temporary, root / 'index.json')
        temporary = None
    except Exception:
        if created:
            target.unlink(missing_ok=True)
        raise
    finally:
        if temporary:
            temporary.unlink(missing_ok=True)
        lock.rmdir()
    print(f'Captured candidate (not active): {data["id"]}:{args.id}\n{target}')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    for command in ['search', 'show', 'validate', 'add']:
        p = sub.add_parser(command)
        p.add_argument('--pack', action='append', help='Explicit pack directory; repeat to read multiple packs')
        if command == 'search':
            p.add_argument('query')
            p.add_argument('--skill', choices=sorted(SKILLS) + ['all'], default=ROOT.name if ROOT.name in SKILLS else 'all')
            p.add_argument('--limit', type=int, default=5)
            p.add_argument('--include-candidates', action='store_true')
            p.add_argument('--json', action='store_true')
        elif command == 'show':
            p.add_argument('id')
            p.add_argument('--max-chars', type=int, default=6000)
        elif command == 'add':
            for flag in ['id', 'title', 'summary', 'skills', 'tags', 'body', 'scope', 'limits']:
                p.add_argument('--' + flag, required=True)
            p.add_argument('--pack-id', default='local-knowledge')
            p.add_argument('--kind', choices=sorted(KINDS), default='lesson')
            p.add_argument('--source')
    args = parser.parse_args(argv)
    try:
        if args.command == 'add':
            add_candidate(args)
            return 0
        roots = args.pack or [BUNDLED]
        packs = [load(root, args.command == 'validate') for root in roots]
        if len({data['id'] for _, data in packs}) != len(packs):
            raise ValueError('Duplicate pack ids; give each pack a distinct id')
        if args.command == 'validate':
            for root, data in packs:
                print(f'Valid pack: {data["id"]} {data["version"]}, {len(data["entries"])} cards ({root})')
        elif args.command == 'show':
            if args.max_chars < 1:
                raise ValueError('--max-chars must be positive')
            print(read_card(packs, args.id, args.max_chars))
        else:
            if not 1 <= args.limit <= 50:
                raise ValueError('--limit must be between 1 and 50')
            results = search(packs, args.query, args.skill, args.include_candidates, args.limit)
            if args.json:
                print(json.dumps(results, ensure_ascii=False, indent=2))
            elif not results:
                print('No matching cards. Continue from task materials or search relevant references; do not invent a rule.')
            else:
                for item in results:
                    print(f'{item["key"]} | {item["status"]} | {item["evidence"]}\n  {item["title"]}: {item["summary"]}\n  Scope: {item["scope"]}\n  Limits: {item["limits"]}\n  File: {item["file"]}')
        return 0
    except (OSError, ValueError, TypeError) as error:
        print(f'Knowledge error: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
