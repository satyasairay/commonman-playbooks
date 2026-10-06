"""Machine gates: source text and built artefacts, Python standard library only."""
import argparse
import datetime as dt
import html
import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote_plus

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'facts'))
from registry import ROOT, read
from english import allowed, errors as english_errors

GATES = ('G1', 'G2', 'G3', 'G4', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11')
PRIMARY = {'indiacode.nic.in', 'egazette.gov.in', 'rbi.org.in', 'sebi.gov.in', 'uidai.gov.in', 'dot.gov.in', 'i4c.mha.gov.in'}
REF = re.compile(r'{{[<%]\s*(fact|contact)\s+["\']?([A-Z][A-Z0-9-]*)["\']?\s*[>%]}}')
LINK = re.compile(r'(?:https?://|www\.|//)[^\s<>"\']+|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\b(?:[A-Za-z0-9-]+\.)+(?:in|com|org|net|gov|nic|io|invalid)\b(?:/[^\s<>"\']*)?')
PHONE = re.compile(r'(?<!\w)(?:\+?\d[\d ()-]{5,}\d)(?!\w)|\b(?:call|dial|helpline|phone)\s+\d{3,5}\b', re.I)
NUMBER = r'(?:\d+(?:[.,]\d+)*|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|sixty|ninety|hundred|thousand|lakh|crore)'
BARE = re.compile(r'\d|[₹%]|\b' + NUMBER + r'\b|\b(?:within|after|before|by|per|every|each|working|business|calendar)\s+(?:(?:a|an|the|next)\s+)?(?:day|week|month|year|hour|minute)s?\b|\b(?:Act|Rules|Circular|section)\b', re.I)
INTERNAL = re.compile(r'\[\[VERIFY|\bL\d\d[a-z]?(?:-cx)?\b|(?:rules|content|scripts|loops)/|\b(?:STATE|LOOP|AGENTS|CLAUDE|PIPELINE)\.md\b')


@dataclass
class Error:
    gate: str
    note: str
    location: str = ''

    def __str__(self):
        return f'{self.gate} RED {self.location}: {self.note}'


@dataclass
class Context:
    facts: dict
    contacts: dict
    opening: dict
    no_contact: dict
    allowed_words: set
    today: dt.date = field(default_factory=dt.date.today)
    site_host: str = 'satsangee.org'

    @classmethod
    def load(cls, facts=ROOT / 'rules/facts.md', contacts=ROOT / 'rules/contacts.md'):
        f, c, _ = read(facts, contacts)
        labels = {lang: tomllib.loads((ROOT / f'i18n/{lang}.toml').read_text(encoding='utf-8')) for lang in ['en', 'or', 'hi']}
        house = (ROOT / 'rules/house-rules.md').read_text(encoding='utf-8')
        approved = re.search(r'^\| en \| (.+?) \| approved \|', house, re.M)
        if not approved:
            raise ValueError('approved English opening not found in house rules')
        openings = {k: v['opening']['other'] for k, v in labels.items()}
        openings['en'] = approved.group(1)
        return cls(f, c, openings, {k: v['no_contact']['other'] for k, v in labels.items()}, allowed(ROOT / 'rules/allowed-terms.md'))

    @classmethod
    def fixture(cls):
        return cls.load(ROOT / 'tests/fixtures/registries/facts.md', ROOT / 'tests/fixtures/registries/contacts.md')


def same_host(url, ctx):
    if '@' in url and not url.startswith(('http://', 'https://', '//')):
        return False
    if url.startswith('www.') or re.match(r'^(?:[A-Za-z0-9-]+\.)+(?:in|com|org|net|gov|nic|io|invalid)(?:/|$)', url):
        url = 'https://' + url
    parsed = urlsplit(url)
    return not parsed.netloc and not parsed.scheme or parsed.hostname == ctx.site_host and parsed.scheme in {'http', 'https'}


def fact_checks(ids, ctx):
    out = []
    for fid in ids:
        row = ctx.facts.get(fid)
        if not row or row['status'] != 'verified':
            out.append(Error('G2', f'fact {fid} missing or unverified'))
            continue
        try:
            if dt.date.fromisoformat(row['recheck_by']) <= ctx.today:
                out.append(Error('G2', f'fact {fid} is due for recheck'))
            dt.date.fromisoformat(row['verified_on'])
            if not row['verified_by']:
                raise ValueError('no verifier')
        except (ValueError, KeyError):
            out.append(Error('G2', f'fact {fid} lacks valid verification and recheck dates'))
        if row['kind'] in {'rule', 'right', 'deadline'}:
            url = urlsplit(row['source_url'])
            host = url.hostname or ''
            if url.scheme != 'https' or url.username or not any(host == domain or host.endswith('.' + domain) for domain in PRIMARY):
                out.append(Error('G9', f'fact {fid} has non-primary source {host}'))
    return out


def contact_checks(ids, ctx):
    return [Error('G1', f'contact {cid} missing or unverified') for cid in ids if cid not in ctx.contacts or ctx.contacts[cid]['status'] != 'verified']


def bare_contact(text, ctx):
    out = []
    for value in LINK.findall(text):
        if not same_host(value.rstrip('.,)'), ctx):
            out.append(Error('G1', f'bare URL or email: {value}'))
    for match in PHONE.finditer(text):
        if re.fullmatch(r'\d{4}-\d{2}-\d{2}', match.group()):
            continue
        out.append(Error('G1', f'bare phone-like number: {match.group()}'))
    return out


def public_text(text, ctx, language='en', claims=True, contacts=True):
    out = bare_contact(text, ctx) if contacts else []
    if INTERNAL.search(text):
        out.append(Error('G7', 'internal marker or filename'))
    if claims and BARE.search(text):
        out.append(Error('G11', 'bare number, amount, time period or legal claim'))
    if language == 'en':
        clean = LINK.sub('', text)
        out += [Error('G10', e) for e in english_errors(clean, ctx.allowed_words)]
    return out


def frontmatter(path):
    text = Path(path).read_text(encoding='utf-8')
    delim = text.splitlines()[0] if text.splitlines() else ''
    if delim not in {'+++', '---'}:
        raise ValueError('front matter required')
    _, raw, body = text.split(delim, 2)
    if delim == '+++':
        return tomllib.loads(raw), body.strip()
    # The existing archetypes use flat YAML. Fail closed on unsupported structure.
    meta = {}
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        key, sep, value = line.partition(':')
        if not sep or key != key.strip():
            raise ValueError('unsupported YAML; use TOML front matter')
        value = re.sub(r'\s+#.*$', '', value).strip()
        if value in {'true', 'false'}:
            parsed = value == 'true'
        elif value.isdigit():
            parsed = int(value)
        elif value.startswith('[') and value.endswith(']'):
            parsed = [v.strip().strip('"\'') for v in value[1:-1].split(',') if v.strip()]
        else:
            parsed = value.strip('"\'')
        meta[key] = parsed
    return meta, body.strip()


def source_checks(meta, body, ctx, language='en'):
    out = []
    refs = REF.findall(body)
    fids = [v for kind, v in refs if kind == 'fact'] + meta.get('clock', []) + meta.get('warnings', [])
    if meta.get('first_seen'):
        fids.append(meta['first_seen'])
    out += fact_checks(fids, ctx)
    out += contact_checks([v for kind, v in refs if kind == 'contact'], ctx)
    clean = REF.sub('', body)
    if '{{' in clean:
        out.append(Error('G11', 'unsupported or malformed shortcode'))
    clean = re.sub(r'^\s*\d+[.)]\s+', '', clean, flags=re.M)
    for key in ['title', 'scope_covers', 'scope_excludes']:
        out += public_text(str(meta.get(key, '')), ctx, language)
    out += public_text(re.sub(r'<[^>]+>', ' ', clean), ctx, language)
    # Also inspect raw HTML attributes, even if Goldmark removes unsafe HTML.
    out += bare_contact(clean, ctx)
    if re.search(r'<(?:script|form|iframe|input|object|embed)\b|\bon\w+\s*=|javascript:', clean, re.I):
        out.append(Error('G4', 'active or collecting markup in source'))
    if not isinstance(meta.get('draft'), bool):
        out.append(Error('G2', 'draft must be an explicit boolean'))
    if meta.get('draft') is False:
        try:
            if not meta.get('verified_by') or dt.date.fromisoformat(str(meta.get('verified_on', ''))) > ctx.today:
                raise ValueError()
        except ValueError:
            out.append(Error('G2', 'live page lacks a valid human signature'))
    if meta.get('kind') == 'card' and meta.get('confidence') not in {'watch', 'confirmed'}:
        out.append(Error('G2', 'card lacks confidence label'))
    if meta.get('kind') == 'card' and meta.get('confidence') == 'confirmed' and not meta.get('warnings'):
        out.append(Error('G2', 'confirmed card lacks advisory reference'))
    for fid in meta.get('clock', []):
        if ctx.facts.get(fid, {}).get('kind') != 'deadline':
            out.append(Error('G2', f'clock reference {fid} is not a deadline'))
    for fid in meta.get('warnings', []):
        if ctx.facts.get(fid, {}).get('kind') != 'advisory':
            out.append(Error('G2', f'warning {fid} is not an advisory'))
    return out


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.segments, self.elements, self.attrs = [], [], [], []
        self.language = 'en'

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.elements.append((tag, attrs, self.getpos()[0]))
        if tag == 'html':
            self.language = attrs.get('lang', 'en').split('-')[0]
        inherited = dict(self.stack[-1][1]) if self.stack else {}
        inherited.update(attrs)
        inherited['_tag'] = tag
        if tag in {'p', 'li', 'h1', 'h2', 'h3', 'h4', 'td', 'summary'}:
            inherited['_block'] = len(self.elements)
        if tag in {'head', 'script', 'style'}:
            inherited['_hidden'] = True
        if tag == 'blockquote' and 'data-evidence' in inherited:
            inherited['_quote'] = True
        self.attrs.append(inherited)
        if tag not in {'meta', 'link', 'img', 'input', 'br', 'hr', 'source', 'area', 'base', 'wbr'}:
            self.stack.append((tag, inherited))

    def handle_endtag(self, tag):
        for index in range(len(self.stack) - 1, -1, -1):
            if self.stack[index][0] == tag:
                del self.stack[index:]
                break

    def handle_data(self, text):
        attrs = self.stack[-1][1] if self.stack else {}
        if text.strip() and not attrs.get('_hidden'):
            self.segments.append((text.strip(), attrs, self.getpos()[0]))


def norm(text):
    return re.sub(r'\s+', ' ', text).strip()


def check_document(text, ctx, kind='playbook', require_trust=False):
    doc = Document()
    doc.feed(text)
    out = []
    facts, contacts = {}, {}
    for tag, attrs, line in doc.elements:
        if tag in {'script', 'form', 'iframe', 'object', 'embed', 'input', 'base'} or any(k.startswith('on') for k in attrs):
            out.append(Error('G4', f'active or collecting tag/attribute: {tag}', str(line)))
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            target = re.search(r'url\s*=\s*(.+)', attrs.get('content', ''), re.I)
            if target and not same_host(target.group(1).strip('"\''), ctx):
                out.append(Error('G4', 'external meta refresh', str(line)))
        for key, value in attrs.items():
            value = value or ''
            if key in {'src', 'srcset', 'poster', 'data'} or tag == 'link' and key == 'href' and attrs.get('rel') != 'canonical':
                urls = [part.strip().split()[0] for part in value.split(',') if part.strip()] if key == 'srcset' else [value]
                if any(not same_host(url, ctx) for url in urls):
                    out.append(Error('G4', f'external resource: {value}', str(line)))
            if 'javascript:' in value.lower() or 'url(' in value.lower() or '@import' in value.lower():
                out.append(Error('G4', 'active URL or inline CSS resource', str(line)))
            if key == 'href' and not same_host(value, ctx) and 'data-contact' not in attrs:
                out.append(Error('G1', f'unreferenced link: {value}', str(line)))
    visible = [t for t, a, _ in doc.segments if not ('data-evidence' in a or 'data-frame' in a)]
    if kind in {'playbook', 'card'}:
        expected = ctx.opening.get(doc.language, '')
        if not expected or not visible or norm(visible[0]) != expected:
            out.append(Error('G8', 'approved opening is not first'))
        if kind == 'card' and not any('data-confidence' in a for _, a, _ in doc.elements):
            out.append(Error('G2', 'built card lacks confidence label'))
    lines = [norm(t) for t, _, _ in doc.segments]
    if not ctx.no_contact.get(doc.language) or ctx.no_contact[doc.language] not in lines:
        out.append(Error('G6', 'no-contact line missing or changed'))
    if require_trust:
        for name in ['data-verified-by', 'data-checked-on', 'data-next-check', 'data-build-commit']:
            if not any(name in a and t.strip() for t, a, _ in doc.segments):
                out.append(Error('G3', f'trust field missing: {name}'))
    prose = {}
    for content, attrs, line in doc.segments:
        if 'data-fact' in attrs:
            facts.setdefault(attrs['data-fact'], []).append(content)
            out += public_text(content, ctx, doc.language, claims=False)
        elif 'data-contact' in attrs:
            contacts.setdefault(attrs['data-contact'], []).append(content)
        elif 'data-evidence' in attrs:
            out += bare_contact(content, ctx)
            # Quote is the sole prose exemption. Identifier/date fields are metadata.
            if not attrs.get('_quote') and 'data-evidence-checked' not in attrs:
                clean = re.sub(r'\b[A-Z]+(?:-[A-Z0-9]+)+\b', '', content)
                out += public_text(clean, ctx, doc.language, claims=False, contacts=False)
        elif 'data-frame' in attrs:
            if not any(k in attrs for k in ['data-verified-by', 'data-checked-on', 'data-next-check', 'data-build-commit']):
                out += public_text(content, ctx, doc.language, claims=False)
        else:
            out += public_text(content, ctx, doc.language)
            prose.setdefault(attrs.get('_block', line), []).append(content)
    # Preserve sentence boundaries across inline elements; a split sentence must not evade G10.
    blocks = '\n'.join(' '.join(parts) for parts in prose.values())
    out += [Error('G10', e) for e in english_errors(blocks, ctx.allowed_words)] if doc.language == 'en' else []
    out += fact_checks(facts, ctx) + contact_checks(contacts, ctx)
    for fid, parts in facts.items():
        expected = ctx.facts.get(fid, {}).get('statements', {}).get(doc.language)
        if not expected or any(norm(p) != norm(expected) for p in parts):
            out.append(Error('G2', f'rendered fact {fid} differs from registry'))
    for cid, parts in contacts.items():
        row = ctx.contacts.get(cid, {})
        share_elements = [a for _, a, _ in doc.elements if a.get('data-contact') == cid and 'data-share-text' in a]
        if not share_elements and any(p != row.get('value') for p in parts):
            out.append(Error('G1', f'rendered contact {cid} differs from registry'))
        for _, attrs, _ in doc.elements:
            if attrs.get('data-contact') == cid:
                if 'data-share-text' in attrs:
                    base, target = row.get('value', ''), attrs.get('href', '')
                    if row.get('type') != 'url-base' or not base or not target.startswith(base) or unquote_plus(target[len(base):]) != attrs['data-share-text']:
                        out.append(Error('G1', f'contact {cid} share target or text differs from its verified base'))
                    continue
                expected = ('tel:' if row.get('type') in {'phone', 'whatsapp'} else 'mailto:' if row.get('type') == 'email' else '') + row.get('value', '')
                if attrs.get('href') != expected:
                    out.append(Error('G1', f'contact {cid} points elsewhere'))
    return out


def run(content, public, ctx):
    out = []
    paths = sorted(Path(content).rglob('*.md'))
    if not paths:
        return [Error('G3', 'no content pages found; check --content path')]
    languages_with_pages = {p.relative_to(content).parts[0] for p in paths}
    for path in paths:
        language = path.relative_to(content).parts[0]
        meta, body = frontmatter(path)
        errors = source_checks(meta, body, ctx, language)
        slug = path.relative_to(Path(content) / language).with_suffix('')
        built = Path(public) / ('' if language == 'en' else language) / slug / 'index.html'
        if built.exists():
            built_text = built.read_text(encoding='utf-8')
            errors += check_document(built_text, ctx, meta.get('kind', ''), meta.get('draft') is False)
            doc = Document()
            doc.feed(built_text)
            shares = [a['data-share-text'] for _, a, _ in doc.elements if 'data-share-text' in a]
            if shares:
                from formats import project
                permalink = ('/' if language == 'en' else '/' + language + '/') + slug.as_posix() + '/'
                canonical = project(meta, body, ctx, language, permalink)['whatsapp']
                if any(text != canonical for text in shares):
                    errors.append(Error('G12', 'share link text differs from source page'))
        elif meta.get('draft') is False:
            errors.append(Error('G3', 'live page missing from build'))
        for error in errors:
            error.location = str(path) + (':' + error.location if error.location else '')
        out += errors
    for path in Path(public).rglob('*.html'):
        # All generated list, error and redirect pages must also have no active resources.
        text = path.read_text(encoding='utf-8')
        doc = Document()
        doc.feed(text)
        redirect = any(tag == 'meta' and a.get('http-equiv', '').lower() == 'refresh' for tag, a, _ in doc.elements)
        gates = {'G1', 'G2', 'G4', 'G7', 'G9', 'G10', 'G11'}
        if doc.language in languages_with_pages and not redirect:
            gates.add('G6')
        out += [e for e in check_document(text, ctx, kind='') if e.gate in gates]
    for path in Path(public).rglob('*.css'):
        if re.search(r'url\s*\(|@import|@font-face', path.read_text(encoding='utf-8'), re.I):
            out.append(Error('G4', 'CSS resource or web font', str(path)))
    for path in ['method/index.html', 'corrections/index.html', '.well-known/security.txt']:
        if not (Path(public) / path).exists():
            out.append(Error('G3', f'required site path missing: {path}'))
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--content', type=Path, default=ROOT / 'content')
    parser.add_argument('--public', type=Path, default=ROOT / 'public')
    parser.add_argument('--facts', type=Path, default=ROOT / 'rules/facts.md')
    parser.add_argument('--contacts', type=Path, default=ROOT / 'rules/contacts.md')
    args = parser.parse_args()
    try:
        errors = run(args.content, args.public, Context.load(args.facts, args.contacts))
    except (OSError, ValueError, KeyError) as exc:
        raise SystemExit(f'GATES RED: {exc}')
    for error in errors:
        print(error)
    for gate in GATES:
        print(f'{gate}: {"RED" if any(e.gate == gate for e in errors) else "GREEN"}')
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
