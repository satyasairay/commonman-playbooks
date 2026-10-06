"""G12 parity and limits. All contact/claim checks retain source provenance."""
import argparse
import re
import sys
from pathlib import Path
from gates import Context, Document, Error, ROOT, check_document, frontmatter, norm, public_text

sys.path.insert(0, str(ROOT / 'scripts/facts'))
from formats import project


def check_format(kind, text, record, ctx, pages=None, pdf_text=None):
    out = []
    if kind == 'whatsapp':
        if len(text) > 700:
            out.append(Error('G12', f'WhatsApp has {len(text)} characters; limit 700'))
        if text != record['whatsapp']:
            out.append(Error('G12', 'WhatsApp differs from source steps or frame'))
        # Reference segments are validated by project/source_checks, and canonical
        # byte equality proves the plain text did not acquire an unreferenced value.
        if not text.startswith(record['opening'] + '\n'):
            out.append(Error('G8', 'WhatsApp opening missing or not first'))
        if record['no_contact'] not in text:
            out.append(Error('G6', 'WhatsApp no-contact line missing'))
        for row in record['steps']:
            for segment in row['segments']:
                if 'kind' not in segment:
                    out += public_text(segment['text'], ctx, record['language'])
                elif segment['kind'] == 'fact':
                    out += public_text(segment['text'], ctx, record['language'], claims=False)
    elif kind == 'print':
        out += check_document(text, ctx, record['kind'])
        doc = Document()
        doc.feed(text)
        actual = norm(' '.join(t for t, a, _ in doc.segments if 'data-reader' in a))
        expected = norm(' '.join(row['text'] for row in record['steps']))
        if actual != expected:
            out.append(Error('G12', 'print steps differ from source prefix'))
        if pages != 1:
            out.append(Error('G12', f'print has {pages if pages is not None else "unknown"} pages; exactly one required'))
        if not re.search(r'font-size:\s*12pt', text):
            out.append(Error('G12', 'print base text must be at least 12pt'))
        sizes = re.findall(r'font-size\s*:\s*([^;}]+)', text, re.I)
        if any(not re.fullmatch(r'(?:\d+(?:\.\d+)?)pt', size.strip()) or float(size.strip()[:-2]) < 12 for size in sizes) or re.search(r'\bfont\s*:', text, re.I):
            out.append(Error('G12', 'print font override below 12pt or unsupported font sizing'))
        if record['page_url'] not in text or record['checked'] not in text:
            out.append(Error('G12', 'print lacks source page address or check status'))
        visible = ''.join(t for t, _, _ in doc.segments)
        normalized_pdf = pdf_text or ''
        # CSS-generated list labels are visible in PDF text but not HTML text nodes.
        # Remove at most one expected label per step; never strip arbitrary numbers.
        for ordinal in range(1, len(record['steps']) + 1):
            normalized_pdf = re.sub(rf'(?m)^[ \t]*{ordinal}\.(?=[ \t\r\n]|$)[ \t]*', '', normalized_pdf, count=1)
        if pdf_text is not None and re.sub(r'\s+', '', normalized_pdf) != re.sub(r'\s+', '', visible):
            out.append(Error('G12', 'PDF text differs from print HTML'))
    else:
        out.append(Error('G12', f'unsupported format: {kind}'))
    return out


def pdf_pages(path):
    # WeasyPrint output has an uncompressed page tree. A structural /Type /Page
    # count is insufficient; pdfinfo must parse the actual file in PC and CI.
    import subprocess
    result = subprocess.run(['pdfinfo', str(path)], capture_output=True, text=True, check=True)
    match = re.search(r'^Pages:\s+(\d+)', result.stdout, re.M)
    if not match:
        raise ValueError('pdfinfo did not report a page count')
    return int(match.group(1))


def extract_pdf_text(path):
    import subprocess
    result = subprocess.run(['pdftotext', '-enc', 'UTF-8', str(path), '-'], capture_output=True, check=True)
    return result.stdout.decode('utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--content', type=Path, default=ROOT / 'tests/fixtures/site')
    parser.add_argument('--public', type=Path, default=ROOT / '.cache/test-public')
    parser.add_argument('--facts', type=Path, default=ROOT / 'tests/fixtures/registries/facts.md')
    parser.add_argument('--contacts', type=Path, default=ROOT / 'tests/fixtures/registries/contacts.md')
    args = parser.parse_args()
    ctx, errors, count = Context.load(args.facts, args.contacts), [], 0
    for path in args.content.rglob('*.md'):
        meta, body = frontmatter(path)
        if meta.get('kind') not in {'playbook', 'card'}:
            continue
        relative = path.relative_to(args.content)
        language = relative.parts[0]
        slug = relative.relative_to(language).with_suffix('').as_posix()
        permalink = ('/' if language == 'en' else '/' + language + '/') + slug + '/'
        record = project(meta, body, ctx, language, permalink)
        folder = args.public / permalink.strip('/')
        for kind in set(meta.get('formats', [])) & {'whatsapp', 'print'}:
            file = folder / ('whatsapp.txt' if kind == 'whatsapp' else 'print.html')
            if not file.exists():
                errors.append(Error('G12', f'{file}: format output missing'))
                continue
            pages = pdf_pages(folder / 'print.pdf') if kind == 'print' else None
            text = file.read_text(encoding='utf-8')
            pdf_text = extract_pdf_text(folder / 'print.pdf') if kind == 'print' else None
            errors += check_format(kind, text, record, ctx, pages, pdf_text)
            count += 1
            print(f'{file}: {len(text)} characters' if kind == 'whatsapp' else f'{file}: PDF {pages} page(s)')
    if not count:
        errors.append(Error('G12', 'no formats checked'))
    for error in errors:
        print(error)
    print('G12: ' + ('RED' if errors else 'GREEN'))
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
