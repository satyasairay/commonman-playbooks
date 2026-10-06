"""Fetch registry sources; emit hash proposals without editing protected rules."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'facts'))
from registry import ROOT, read
from fetch_text import fetch, to_text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', action='append', help='source ids; default all registry sources')
    args = parser.parse_args()
    _, _, sources = read(ROOT / 'rules/facts.md', ROOT / 'rules/contacts.md')
    folder = ROOT / '.cache/sources'
    folder.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for sid in args.id or sources:
        if sid not in sources:
            parser.error(f'unknown source: {sid}')
        raw, ctype, final = fetch(sources[sid]['url'])
        # Stop on an access challenge; never try another identity or route.
        if b'captcha' in raw.lower() or b'cf-chl-' in raw.lower():
            raise SystemExit(f'{sid}: access challenge; Satya must supply a snapshot')
        ext = '.pdf' if raw[:5] == b'%PDF-' else '.html'
        path = folder / (sid + ext)
        path.write_bytes(raw)
        text = to_text(path, raw)
        (folder / (sid + '.txt')).write_text(text, encoding='utf-8')
        manifest[sid] = {'sha256': hashlib.sha256(raw).hexdigest(), 'final_url': final, 'content_type': ctype}
        print(sid, manifest[sid]['sha256'])
    (folder / 'hash-proposals.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print('Hash proposals saved; only Satya may update rules/facts.md.')


if __name__ == '__main__':
    main()
