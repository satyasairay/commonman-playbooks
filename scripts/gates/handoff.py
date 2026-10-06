"""Prepare reviewable PR bodies and retained logs; never publish or sign."""
import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load(path):
    raw = Path(path).read_bytes()
    return raw.decode('utf-16' if raw.startswith((b'\xff\xfe', b'\xfe\xff')) else 'utf-8-sig')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('loop', choices=['L03b', 'L03c'])
    args = parser.parse_args()
    folder = ROOT / 'tests/evidence' / args.loop
    folder.mkdir(parents=True, exist_ok=True)
    names = ['real-export', 'real-preview-build', 'real-gates', 'test-export', 'test-build', 'test-gates', 'tests', 'mutations']
    if args.loop == 'L03c':
        names += ['real-formats', 'test-formats', 'format-controls', 'formats', 'format-gates', 'real-format-gates', 'format-mutations']
    sections = [load(ROOT / f'tests/evidence/{args.loop}.md'), '## Filled loop card\n\n' + load(ROOT / 'loops/L03-cx.md')]
    for name in names:
        path = ROOT / '.cache/evidence' / (name + '.txt')
        if not path.exists():
            sections.append(f'{name}: NOT CHECKED; output missing.')
            continue
        shutil.copyfile(path, folder / path.name)
        output = load(path)
        if 'mutations' in name or 'controls' in name:
            output = '\n'.join(line for line in output.splitlines() if re.match(r'^(?:G\d+|verified-only|source script|built resource|page network|format)', line))
            output += f'\nFull output: tests/evidence/{args.loop}/{name}.txt'
        sections.append(f'## {name}\n\n```text\n{output}\n```')
    html_path = ROOT / '.cache/test-public/playbooks/test-page/index.html'
    shutil.copyfile(html_path, folder / 'test-page.html')
    sections.append('## TEST HTML\n\n```html\n' + load(html_path) + '\n```')
    for name in ['whatsapp.txt', 'print.html', 'print.pdf', 'format-manifest.json']:
        path = ROOT / '.cache/test-public/playbooks/test-page' / name
        if path.exists():
            shutil.copyfile(path, folder / name)
    for name in ['print-1.png', 'web-320-closed.png', 'web-320-expanded.png', 'browser-evidence.json', 'browser-page-network.json']:
        path = ROOT / '.cache/evidence' / name
        if path.exists():
            shutil.copyfile(path, folder / name)
    for name in ['L03b-tests-first.txt', 'L03c-tests-first.txt']:
        path = ROOT / '.cache/evidence' / name
        if path.exists():
            shutil.copyfile(path, folder / name)
    result = ROOT / '.cache' / f'{args.loop}-pr.md'
    result.write_text('\n\n'.join(sections), encoding='utf-8')
    print(f'{result}: {result.stat().st_size} bytes')


if __name__ == '__main__':
    main()
