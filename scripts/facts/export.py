"""Export only verified rows; test registries require explicit paths."""
import argparse
import json
from pathlib import Path
from registry import ROOT, read, parse_date, KINDS


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
        for key, row in verified.items():
            if name == 'facts' and row['kind'] not in KINDS:
                parser.error(f'{key}: unknown fact kind')
            row['verified_on'] = parse_date(row['verified_on']).isoformat()
            if name == 'facts':
                row['recheck_by'] = parse_date(row['recheck_by']).isoformat()
        (args.output / (name + '.json')).write_text(json.dumps(verified, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'{name}: exported {len(verified)} verified rows')


if __name__ == '__main__':
    main()
