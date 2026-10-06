"""G12 mutations of real built artefacts, with backup restore after each."""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path
from gates import Context, ROOT, frontmatter
from format_gate import check_format, pdf_pages, extract_pdf_text

sys.path.insert(0, str(ROOT / 'scripts/facts'))
from formats import project


def unit_control_mutations():
    control = ROOT / 'scripts/gates/format_gate.py'
    folder = ROOT / '.cache/mutations'
    folder.mkdir(parents=True, exist_ok=True)
    backup = folder / 'format_gate.py.backup'
    shutil.copyfile(control, backup)
    mutations = [
        ('WhatsApp limit', 'if len(text) > 700:', 'if False:'),
        ('PDF page limit', 'if pages != 1:', 'if False:'),
        ('WhatsApp step parity', "if text != record['whatsapp']:", 'if False:'),
        ('print step parity', 'if actual != expected:', 'if False:'),
        ('print font minimum', "if any(not re.fullmatch(r'(?:\\d+(?:\\.\\d+)?)pt', size.strip()) or float(size.strip()[:-2]) < 12 for size in sizes) or re.search(r'\\bfont\\s*:', text, re.I):", 'if False:'),
        ('PDF text parity', "if pdf_text is not None and re.sub(r'\\s+', '', pdf_text) != re.sub(r'\\s+', '', visible):", 'if False:'),
    ]
    command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_formats.py', '-v']
    try:
        for label, old, new in mutations:
            original = backup.read_text(encoding='utf-8')
            assert old in original
            control.write_text(original.replace(old, new), encoding='utf-8')
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
            assert result.returncode, f'{label} disabled control survived'
            print(f'G12 {label} disabled control: TESTS RED (expected)')
            print(result.stdout + result.stderr)
            shutil.copyfile(backup, control)
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
            assert not result.returncode, result.stdout + result.stderr
            print(f'G12 {label} restored control: TESTS GREEN')
            print(result.stdout + result.stderr)
    finally:
        shutil.copyfile(backup, control)


def artefact_mutations():
    if os.environ.get('GITHUB_ACTIONS') != 'true':
        raise SystemExit('the real two-page mutation uses WeasyPrint only in L03c CI')
    folder = ROOT / '.cache/test-public/playbooks/test-page'
    backups = ROOT / '.cache/mutations/format-backups'
    backups.mkdir(parents=True, exist_ok=True)
    files = [folder / 'whatsapp.txt', folder / 'print.html', folder / 'print.pdf']
    for file in files:
        shutil.copyfile(file, backups / file.name)
    ctx = Context.fixture()
    meta, body = frontmatter(ROOT / 'tests/fixtures/site/en/playbooks/test-page.md')
    record = project(meta, body, ctx, 'en', '/playbooks/test-page/')
    import json
    mutations = json.loads((ROOT / 'tests/fixtures/gates/format-mutations.json').read_text())
    try:
        for mutation in mutations:
            target = mutation['target']
            if target in {'whatsapp', 'step'}:
                file = folder / 'whatsapp.txt'
                text = file.read_text(encoding='utf-8')
                text = text + mutation['new'] * mutation['repeat'] if target == 'whatsapp' else text.replace(mutation['old'], mutation['new'])
                file.write_text(text, encoding='utf-8')
                errors = check_format('whatsapp', file.read_text(encoding='utf-8'), record, ctx)
            else:
                file = folder / 'print.html'
                text = file.read_text(encoding='utf-8').replace('</main>', '<section style="break-before: page">Extra test page.</section></main>')
                file.write_text(text, encoding='utf-8')
                subprocess.run(['weasyprint', str(file), str(folder / 'print.pdf')], check=True)
                pages = pdf_pages(folder / 'print.pdf')
                assert pages == 2, f'two-page mutation generated {pages} pages'
                errors = check_format('print', text, record, ctx, pages=pages, pdf_text=extract_pdf_text(folder / 'print.pdf'))
            hits = [e for e in errors if e.gate == 'G12']
            assert hits, mutation['name'] + ' survived'
            print(f'G12 {mutation["name"]}: RED (expected)')
            for error in hits:
                print(error)
            for file in files:
                shutil.copyfile(backups / file.name, file)
            errors = check_format('whatsapp', files[0].read_text(encoding='utf-8'), record, ctx)
            errors += check_format('print', files[1].read_text(encoding='utf-8'), record, ctx, pages=pdf_pages(files[2]), pdf_text=extract_pdf_text(files[2]))
            assert not errors, errors
            print(f'G12 {mutation["name"]}: GREEN after backup restore')
    finally:
        for file in files:
            shutil.copyfile(backups / file.name, file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--controls-only', action='store_true')
    args = parser.parse_args()
    unit_control_mutations()
    if not args.controls_only:
        artefact_mutations()


if __name__ == '__main__':
    main()
