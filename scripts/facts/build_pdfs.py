"""CI-only PDF authoring via the WeasyPrint CLI; no dependency in gate code."""
import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'scripts/gates'))
from format_gate import pdf_pages


def build(public):
    count = 0
    for page in sorted(Path(public).rglob('print.html')):
        output = page.with_suffix('.pdf')
        subprocess.run(['weasyprint', str(page), str(output)], check=True)
        pages = pdf_pages(output)
        print(f'{output}: {pages} page(s)')
        count += 1
    if not count:
        print('No enabled print formats in this build.')
    return count


def main():
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        raise SystemExit('WeasyPrint authoring is restricted to the L03c CI job by the loop card.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--public', action='append', type=Path, required=True)
    args = parser.parse_args()
    for public in args.public:
        build(public)


if __name__ == '__main__':
    main()
