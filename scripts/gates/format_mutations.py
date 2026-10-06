"""G12 control and PDF mutations in TemporaryDirectory copies only."""
import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from gates import Context, ROOT, frontmatter
from format_gate import check_format, pdf_pages, extract_pdf_text
sys.path.insert(0, str(ROOT / 'tests'))
from site_mutations import copy_repo, run, build
sys.path.insert(0, str(ROOT / 'scripts/facts'))
from formats import project

CONTROLS = [
    ('WhatsApp limit', 'if len(text) > 700:', 'if False:'),
    ('PDF page limit', 'if pages != 1:', 'if False:'),
    ('WhatsApp parity', "if text != record['whatsapp']:", 'if False:'),
    ('whole print parity', 'if actual != expected:', 'if False:'),
    ('font minimum', "if any(not re.fullmatch(r'(?:\\d+(?:\\.\\d+)?)pt', size.strip()) or float(size.strip()[:-2]) < 12 for size in sizes) or re.search(r'\\bfont\\s*:', text, re.I):", 'if False:'),
    ('PDF text parity', "if pdf_text is not None and re.sub(r'\\s+', '', normalized_pdf) != re.sub(r'\\s+', '', visible):", 'if False:'),
    ('C01 required', "if phone.get('status') != 'verified' or not phone.get('value') or not re.search(r'(?<!\\d)' + re.escape(phone['value']) + r'(?!\\d)', text):", 'if False:'),
    ('capital words', "if re.search(r'\\b[A-Z]{2,}\\b', text):", 'if False:'),
    ('print address', "if record['page_url'] not in actual:", 'if False:'),
    ('print status', "if record['checked'] not in actual:", 'if False:'),
    ('print shrink', "if re.search(r'\\b(?:transform|zoom)\\s*:|<small\\b', text, re.I):", 'if False:'),
    ('address size', 'if not address_sizes or any(float(size) < 18 for size in address_sizes):', 'if False:'),
]

PROJECT_CONTROLS = [
    ('scope projection', "'scope': scope", "'scope': records"),
    ('clock projection', "'clock': clock", "'clock': records"),
    ('unsigned i18n', "status = labels['unsigned']['other']", "status = 'Draft awaiting review'"),
    ('checked i18n', 'labels["checked"]["other"]', '"Checked on"'),
    ('project verified C01', "if contact_checks(['C01'], ctx):", 'if False:'),
]

TEMPLATE_CONTROLS = [
    ('formats above trust', 'layouts/_default/single.html', '{{ partial "formats.html" . }}\n{{ partial "trust.html" . }}', '{{ partial "trust.html" . }}\n{{ partial "formats.html" . }}'),
    ('print scope', 'layouts/_default/single.print.html', '<p class="scope">{{ .html | safeHTML }}</p>', '<p class="scope"></p>'),
    ('print clock', 'layouts/_default/single.print.html', '<aside class="clock"><h2>{{ $record.clock_label }}</h2><ul>{{ range . }}<li>{{ .html | safeHTML }}</li>{{ end }}</ul></aside>', '<aside class="clock"></aside>'),
    ('print address size', 'layouts/_default/single.print.html', 'font-size: 18pt', 'font-size: 14pt'),
    ('print check status', 'layouts/_default/single.print.html', '<p data-format-checked>{{ $record.checked }}</p>', '<p data-format-checked></p>'),
    ('share template hash', 'layouts/partials/formats.html', 'sha256 .whatsapp', 'sha256 "Read"'),
]

def template_controls(root):
    result = run(root, [sys.executable, 'scripts/facts/formats.py', '--content', 'tests/fixtures/site', '--facts', 'tests/fixtures/registries/facts.md', '--contacts', 'tests/fixtures/registries/contacts.md', '--output', '.cache/fixture-data/generated'])
    if result.returncode:
        raise RuntimeError(result.stderr)
    for label, path, old, new in TEMPLATE_CONTROLS:
        file = root / path
        text = file.read_text(encoding='utf-8')
        if text.count(old) != 1:
            raise RuntimeError(f'{label}: template target count {text.count(old)}')
        backup = file.with_name(file.name + '.backup')
        shutil.copy2(file, backup)
        file.write_text(text.replace(old, new), encoding='utf-8')
        build(root)
        command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_format_fix.py', '-v']
        red = run(root, command)
        if red.returncode == 0 or 'FAIL:' not in red.stderr or 'ERROR:' in red.stderr:
            raise RuntimeError(f'{label}: no assertion detected changed template\n{red.stderr}')
        print(f'{label} disabled alone: RED exit {red.returncode}', flush=True)
        print(red.stderr.replace(str(root), '<temp-repo>'))
        shutil.copy2(backup, file)
        build(root)
        green = run(root, command)
        if green.returncode:
            raise RuntimeError(f'{label}: restore failed\n{green.stderr}')
        print(f'{label} backup restored: GREEN exit {green.returncode}', flush=True)

def unit_controls(root):
    targets = [('scripts/gates/format_gate.py', *control) for control in CONTROLS]
    targets += [('scripts/facts/formats.py', *control) for control in PROJECT_CONTROLS]
    for path, label, old, new in targets:
        file = root / path
        text = file.read_text(encoding='utf-8')
        if text.count(old) != 1:
            raise RuntimeError(f'{label}: target count {text.count(old)}')
        backup = file.with_name(file.name + '.backup')
        shutil.copy2(file, backup)
        file.write_text(text.replace(old, new), encoding='utf-8')
        command = [sys.executable, '-B', '-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_format*.py', '-v']
        red = run(root, command)
        if red.returncode == 0 or 'FAIL:' not in red.stderr or 'ERROR:' in red.stderr:
            raise RuntimeError(f'{label}: no assertion detected disabled control\n{red.stderr}')
        print(f'G12 {label} disabled alone: RED exit {red.returncode}', flush=True)
        print(red.stderr.replace(str(root), '<temp-repo>'))
        shutil.copy2(backup, file)
        green = run(root, command)
        if green.returncode:
            raise RuntimeError(f'{label}: restore failed\n{green.stderr}')
        print(f'G12 {label} backup restored: GREEN exit {green.returncode}', flush=True)

def artefacts(root):
    folder = root / '.cache/test-public/playbooks/test-page'
    ctx = Context.fixture()
    meta, body = frontmatter(ROOT / 'tests/fixtures/site/en/playbooks/test-page.md')
    record = project(meta, body, ctx, 'en', '/playbooks/test-page/')
    files = [folder / name for name in ('whatsapp.txt', 'print.html', 'print.pdf')]
    for file in files:
        shutil.copy2(file, file.with_name(file.name + '.backup'))
    mutations = json.loads((ROOT / 'tests/fixtures/gates/format-mutations.json').read_text(encoding='utf-8'))
    for mutation in mutations:
        if mutation['target'] in {'whatsapp', 'step'}:
            file = files[0]
            text = file.read_text(encoding='utf-8')
            text = text + mutation['new'] * mutation['repeat'] if mutation['target'] == 'whatsapp' else text.replace(mutation['old'], mutation['new'])
            file.write_text(text, encoding='utf-8')
            errors = check_format('whatsapp', text, record, ctx)
        else:
            file = files[1]
            text = file.read_text(encoding='utf-8').replace('</main>', '<section style="break-before: page">Extra test page.</section></main>')
            file.write_text(text, encoding='utf-8')
            subprocess.run(['weasyprint', str(file), str(files[2])], check=True)
            pages = pdf_pages(files[2])
            if pages != 2:
                raise RuntimeError(f'two-page mutation generated {pages} pages')
            errors = check_format('print', text, record, ctx, pages, extract_pdf_text(files[2]))
        if not any(e.gate == 'G12' for e in errors):
            raise RuntimeError(mutation['name'] + ': mutation survived')
        print(f'G12 {mutation["name"]}: RED (expected)')
        for error in errors:
            print(error)
        for file in files:
            shutil.copy2(file.with_name(file.name + '.backup'), file)
        errors = check_format('whatsapp', files[0].read_text(encoding='utf-8'), record, ctx)
        errors += check_format('print', files[1].read_text(encoding='utf-8'), record, ctx, pdf_pages(files[2]), extract_pdf_text(files[2]))
        if errors:
            raise RuntimeError(f'backup restore not green: {errors}')
        print(f'G12 {mutation["name"]}: GREEN after backup restore')

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser()
    parser.add_argument('--controls-only', action='store_true')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp) / 'repo'
        root.mkdir()
        copy_repo(root)
        shutil.copytree(ROOT / '.cache/test-public', root / '.cache/test-public')
        unit_controls(root)
        if args.controls_only:
            template_controls(root)
        else:
            artefacts(root)

if __name__ == '__main__':
    main()
