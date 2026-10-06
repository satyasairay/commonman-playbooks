"""Project the unchanged first source steps into all short formats."""
import argparse
import hashlib
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'gates'))
from gates import Context, REF, ROOT, frontmatter, source_checks


def render_step(source, ctx, language):
    plain, markup, segments = [], [], []
    cursor = 0
    for match in REF.finditer(source):
        text = source[cursor:match.start()]
        plain.append(text)
        markup.append(html.escape(text))
        segments.append({'text': text})
        kind, rid = match.groups()
        if kind == 'fact':
            value = ctx.facts[rid]['statements'][language]
            markup.append(f'<span data-fact="{rid}">{html.escape(value)}</span>')
        else:
            row = ctx.contacts[rid]
            value = row['value']
            href = ('tel:' if row['type'] in {'phone', 'whatsapp'} else 'mailto:' if row['type'] == 'email' else '') + value
            markup.append(f'<a data-contact="{rid}" href="{html.escape(href, quote=True)}">{html.escape(value)}</a>')
        plain.append(value)
        segments.append({'text': value, 'kind': kind, 'id': rid})
        cursor = match.end()
    text = source[cursor:]
    plain.append(text)
    markup.append(html.escape(text))
    segments.append({'text': text})
    return {'text': ''.join(plain), 'html': ''.join(markup), 'segments': segments, 'source': source}


def project(meta, body, ctx, language, permalink):
    errors = source_checks(meta, body, ctx, language)
    if errors:
        raise ValueError('\n'.join(str(e) for e in errors))
    lines = body.splitlines()
    steps, started = [], False
    for line in lines:
        match = re.match(r'^\s*(?:\d+\.|-)\s+(.+)$', line)
        if match:
            started = True
            steps.append(match.group(1))
        elif started and line.strip():
            if line.startswith((' ', '\t')):
                raise ValueError('multi-line steps need an explicit shared format parser; do not drop continuation text')
            break
    count = meta.get('first_steps', min(3, len(steps)))
    if not isinstance(count, int) or count < 1 or count > len(steps):
        raise ValueError('first_steps must select a non-empty prefix of the first source list')
    # Supported steps are single lines, plain prose and references. Do not silently
    # strip Markdown emphasis, links or continuation lines and change the words.
    for step in steps[:count]:
        bare = REF.sub('', step)
        if any(token in bare for token in ['<', '>', '[', ']', '*', '`']):
            raise ValueError('short-format steps must use plain prose and references')
    opening = ctx.opening.get(language, '')
    if not opening:
        raise ValueError(f'no approved opening for {language}')
    title = str(meta['title'])
    url = 'https://' + ctx.site_host + permalink
    checked = str(meta.get('verified_on', ''))
    status = 'Draft awaiting review'
    if checked:
        import datetime as dt
        date = dt.date.fromisoformat(checked)
        status = f'Checked on {date.day} {date.strftime("%B")} {date.year}'
    records = [render_step(s, ctx, language) for s in steps[:count]]
    no_contact = ctx.no_contact[language]
    parts = [opening, '*' + title + '*'] + [f'{i}. {row["text"]}' for i, row in enumerate(records, 1)] + [status, url, no_contact]
    text = '\n\n'.join(parts) + '\n'
    return {'opening': opening, 'title': title, 'steps': records, 'checked': status, 'no_contact': no_contact, 'page_url': url, 'language': language, 'kind': meta['kind'], 'whatsapp': text, 'source_sha256': hashlib.sha256(body.encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--content', type=Path, default=ROOT / 'content')
    parser.add_argument('--facts', type=Path, default=ROOT / 'rules/facts.md')
    parser.add_argument('--contacts', type=Path, default=ROOT / 'rules/contacts.md')
    parser.add_argument('--output', type=Path, default=ROOT / 'data/generated')
    args = parser.parse_args()
    ctx = Context.load(args.facts, args.contacts)
    records = {}
    for path in args.content.rglob('*.md'):
        meta, body = frontmatter(path)
        if meta.get('kind') not in {'playbook', 'card'} or not set(meta.get('formats', [])) & {'whatsapp', 'print'}:
            continue
        relative = path.relative_to(args.content)
        language = relative.parts[0]
        slug = relative.relative_to(language).with_suffix('').as_posix()
        permalink = ('/' if language == 'en' else '/' + language + '/') + slug + '/'
        records[permalink] = project(meta, body, ctx, language, permalink)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / 'formats.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'formats: projected {len(records)} source pages')


if __name__ == '__main__':
    main()
