"""Export only verified rows; test registries require explicit paths."""
import argparse
import json
from pathlib import Path
from registry import ROOT, read


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--facts', type=Path, default=ROOT / 'rules/facts.md')
    parser.add_argument('--contacts', type=Path, default=ROOT / 'rules/contacts.md')
    parser.add_argument('--output', type=Path, default=ROOT / 'data/generated')
    args = parser.parse_args()
    if args.output.resolve() == (ROOT / 'data/generated').resolve() and (args.facts.resolve() != (ROOT / 'rules/facts.md').resolve() or args.contacts.resolve() != (ROOT / 'rules/contacts.md').resolve()):
        parser.error('non-production registries require an explicit separate --output')
    facts, contacts, _ = read(args.facts, args.contacts)
    args.output.mkdir(parents=True, exist_ok=True)
    for name, rows in [('facts', facts), ('contacts', contacts)]:
        verified = {key: row for key, row in rows.items() if row['status'] == 'verified'}
        (args.output / (name + '.json')).write_text(json.dumps(verified, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'{name}: exported {len(verified)} verified rows')


if __name__ == '__main__':
    main()
