"""Machine gates: source text and built artefacts, Python standard library only."""
import argparse
import datetime as dt
import html
import hashlib
import json
import re
import sys
import tomllib
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote_plus

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'facts'))
from registry import ROOT, read, parse_date, KINDS
from english import allowed, errors as english_errors

GATES = ('G1', 'G2', 'G3', 'G4', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11', 'G12')
PRIMARY = {'indiacode.nic.in', 'egazette.gov.in', 'rbi.org.in', 'sebi.gov.in', 'uidai.gov.in', 'dot.gov.in', 'i4c.mha.gov.in'}
REF = re.compile(r'{{[<%]\s*(fact|contact)\s+["\']?([A-Z][A-Z0-9-]*)["\']?\s*[>%]}}')
LINK = re.compile(r'(?:https?://|www\.|//)[^\s<>"\']+|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\b(?:[a-z0-9-]+\.)+[a-z]{2,}\b|\b\w+\s*(?:\[at\]|\(at\))\s*\w+(?:\s*(?:\[dot\]|\(dot\))\s*\w+)+', re.I)
PHONE = re.compile(r'(?<!\w)(?:\+?\d[\d ()-]{5,}\d)(?!\w)|\b(?:call|dial|helpline|phone)\s+\d{3,5}\b', re.I)
NUMBER = r'(?:\d+(?:[.,]\d+)*|zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|lakh|crore|half|dozen|few|several|couple)'
BARE = re.compile(r'\d|[₹%]|\b' + NUMBER + r'\b|\b(?:seconds?|minutes?|hours?|days?|weeks?|fortnights?|months?|years?|percent|per\s+cent)\b|\b(?:rules?|circulars?|sections?|regulations?|sanhitas?|adhiniyams?|ordinances?|notifications?)\b', re.I)
LEGAL_CAPITAL = re.compile(r'\b(?:Acts?|Codes?|Schemes?|Directions?|January|February|March|April|May|June|July|August|September|October|November|December)\b')
INTERNAL = re.compile(r'\[+\s*verify|\bL\d\d[a-z]?(?:-cx)?\b|(?:rules|content|scripts|loops)[/\\]|\b[\w-]+\.md\b', re.I)


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
    labels: dict = field(default_factory=dict)

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
        no_contacts = {k: v['no_contact']['other'] for k, v in labels.items()}
        no_section = re.search(r'## [^\n]*[Nn]o-contact[^\n]*\n(.*?)(?=\n## |\Z)', house, re.S)
        if no_section:
            row = re.search(r'^\| en \| (.+?) \| approved \|', no_section[1], re.M)
            if row:
                no_contacts['en'] = row[1]
        terms = allowed(ROOT / 'rules/allowed-terms.md')
        signature = re.search(r'"Verified by (.+?) on \d+ [A-Za-z]+ \d{4}\.', house)
        if signature:
            terms.add(signature[1].lower())
        return cls(f, c, openings, no_contacts, terms, labels=labels)

    @classmethod
    def fixture(cls):
        return cls.load(ROOT / 'tests/fixtures/registries/facts.md', ROOT / 'tests/fixtures/registries/contacts.md')


def same_host(url, ctx):
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
            if parse_date(row['recheck_by']) <= ctx.today:
                out.append(Error('G2', f'fact {fid} is due for recheck'))
            parse_date(row['verified_on'])
            if not row['verified_by']:
                raise ValueError('no verifier')
        except (ValueError, KeyError) as exc:
            out.append(Error('G2', f'fact {fid} lacks valid verification and recheck dates: {exc}'))
        if row['kind'] not in KINDS:
            out.append(Error('G9', f'fact {fid} has unknown kind'))
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
    if claims and (BARE.search(text) or LEGAL_CAPITAL.search(text)):
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
    numbered = []
    expected = 1
    for line in clean.splitlines():
        step = re.match(r'^\s*(\d+)[.)]\s+', line)
        if step and int(step[1]) == expected:
            line = line[step.end():]
            expected += 1
        elif line.lstrip().startswith('#'):
            expected = 1
        numbered.append(line)
    clean = '\n'.join(numbered)
    for key in ['title', 'scope_covers', 'scope_excludes', 'verified_by']:
        out += public_text(str(meta.get(key, '')), ctx, language)
    out += public_text(re.sub(r'<[^>]+>', ' ', clean), ctx, language)
    if INTERNAL.search(body):
        out.append(Error('G7', 'raw source contains internal marker or filename'))
    # Also inspect raw HTML attributes, even if Goldmark removes unsafe HTML.
    out += bare_contact(clean, ctx)
    if re.search(r'<(?:script|form|iframe|input|object|embed)\b|\bon\w+\s*=|javascript:', clean, re.I):
        out.append(Error('G4', 'active or collecting markup in source'))
    if not isinstance(meta.get('draft'), bool):
        out.append(Error('G2', 'draft must be an explicit boolean'))
    if meta.get('draft') is False:
        try:
            if not meta.get('verified_by') or parse_date(meta.get('verified_on', '')) > ctx.today:
                raise ValueError()
        except ValueError as exc:
            out.append(Error('G2', f'live page lacks a valid human signature: {exc}'))
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
        self.stack, self.segments, self.elements, self.attrs, self.styles = [], [], [], [], []
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
        if attrs.get('_tag') == 'style':
            self.styles.append(text)
        if text.strip() and not attrs.get('_hidden'):
            self.segments.append((text.strip(), attrs, self.getpos()[0]))


def norm(text):
    return re.sub(r'\s+', ' ', text).strip()


def page_address(text, ctx):
    url = urlsplit(text)
    return url.scheme == 'https' and url.hostname == ctx.site_host and not url.username and not url.query and not url.fragment and url.path.startswith('/') and url.path.endswith('/')


def share_parity(shares, canonical):
    return [Error('G12', 'share link text differs from source page')] if any(text != canonical for text in shares) else []


def check_document(text, ctx, kind='playbook', require_trust=False):
    doc = Document()
    doc.feed(text)
    out = []
    if len(text.encode('utf-8')) >= 50000:
        out.append(Error('G12', 'web page must be under 50 KB'))
    if INTERNAL.search(text):
        out.append(Error('G7', 'raw HTML contains internal marker or filename'))
    if re.search(r'url\s*\(|@import|@font-face', ''.join(doc.styles), re.I):
        out.append(Error('G4', 'style block resource or web font'))
    facts, contacts = {}, {}
    for tag, attrs, line in doc.elements:
        if tag == 'ol' and str(attrs.get('start', '1')) != '1':
            out.append(Error('G1', 'ordered list must start at 1', str(line)))
            out.append(Error('G11', 'ordered list must start at 1', str(line)))
        if tag in {'script', 'form', 'iframe', 'object', 'embed', 'input', 'base'} or any(k.startswith('on') for k in attrs):
            out.append(Error('G4', f'active or collecting tag/attribute: {tag}', str(line)))
        if tag == 'meta' and attrs.get('http-equiv', '').lower() == 'refresh':
            target = re.search(r'url\s*=\s*(.+)', attrs.get('content', ''), re.I)
            if target and not same_host(target.group(1).strip('"\''), ctx):
                out.append(Error('G4', 'external meta refresh', str(line)))
        for key, value in attrs.items():
            value = value or ''
            if re.search(r'(?:https?:)?//', value, re.I) and not (key == 'href' and 'data-contact' in attrs):
                out.append(Error('G4', f'absolute URL in {tag} {key}', str(line)))
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
        identities = [a for _, a, _ in doc.elements if 'data-build-commit' in a]
        for identity in identities:
            if not re.fullmatch(r'[0-9a-fA-F]{7,40}', identity.get('data-build-commit') or ''):
                out.append(Error('G3', 'build commit must be a hex SHA'))
            try:
                parse_date(identity.get('data-build-date', ''))
            except ValueError as exc:
                out.append(Error('G3', f'invalid build date: {exc}'))
        if not any('data-ai-line' in a and a.get('data-frame') == 'footer' for a in doc.attrs):
            out.append(Error('G3', 'footer AI-line element missing'))
    prose = {}
    for content, attrs, line in doc.segments:
        if doc.language == 'en' and re.search(r'[\u0900-\u097f\u0b00-\u0b7f]', content):
            out.append(Error('G10', 'non-English script'))
        if INTERNAL.search(content):
            out.append(Error('G7', 'internal marker or filename'))
        if 'data-fact' in attrs:
            facts.setdefault(attrs['data-fact'], []).append(content)
            out += public_text(content, ctx, doc.language, claims=False)
            prose.setdefault(attrs.get('_block', line), []).append(content)
        elif 'data-contact' in attrs:
            contacts.setdefault(attrs['data-contact'], []).append(content)
        elif 'data-confidence' in attrs:
            out += public_text(content, ctx, doc.language, claims=False)
        elif 'data-evidence' in attrs:
            out += bare_contact(content, ctx)
            # Quote is the sole prose exemption. Identifier/date fields are metadata.
            if not attrs.get('_quote') and 'data-evidence-checked' not in attrs:
                clean = re.sub(r'\b[A-Z]+(?:-[A-Z0-9]+)+\b', '', content)
                out += public_text(clean, ctx, doc.language, claims=False, contacts=False)
        elif 'data-frame' in attrs:
            if attrs.get('data-frame') == 'trust' and 'data-page-url' in attrs and page_address(content, ctx):
                continue
            out += bare_contact(content, ctx)
            if 'data-verified-by' in attrs:
                out += public_text(content, ctx, doc.language, claims=False)
            if not any(k in attrs for k in ['data-verified-by', 'data-checked-on', 'data-next-check', 'data-build-commit']):
                out += public_text(content, ctx, doc.language, claims=False)
        else:
            out += public_text(content, ctx, doc.language)
            prose.setdefault(attrs.get('_block', line), []).append(content)
    # Preserve sentence boundaries across inline elements; a split sentence must not evade G10.
    blocks = '\n\n'.join(' '.join(parts) for parts in prose.values())
    out += [Error('G10', e) for e in english_errors(blocks, ctx.allowed_words)] if doc.language == 'en' else []
    out += fact_checks(facts, ctx) + contact_checks(contacts, ctx)
    for fid, parts in facts.items():
        expected = ctx.facts.get(fid, {}).get('statements', {}).get(doc.language)
        if not expected or any(norm(p) != norm(expected) for p in parts):
            out.append(Error('G2', f'rendered fact {fid} differs from registry'))
    for cid, parts in contacts.items():
        row = ctx.contacts.get(cid, {})
        shares = [a for _, a, _ in doc.elements if a.get('data-contact') == cid and 'data-share' in a]
        expected_label = ctx.labels.get(doc.language, {}).get('share', {}).get('other', 'WhatsApp')
        if any(p != (expected_label if shares else row.get('value')) for p in parts):
            out.append(Error('G1', f'rendered contact {cid} differs from registry'))
        for _, attrs, _ in doc.elements:
            if attrs.get('data-contact') == cid:
                if 'data-share' in attrs:
                    base, target = row.get('value', ''), attrs.get('href', '')
                    decoded = unquote_plus(target[len(base):])
                    if row.get('type') != 'url-base' or not base or not target.startswith(base) or hashlib.sha256(decoded.encode()).hexdigest() != attrs.get('data-share-sha256'):
                        out.append(Error('G1', f'contact {cid} share base or hash differs'))
                    continue
                expected = ('tel:' if row.get('type') in {'phone', 'whatsapp'} else 'mailto:' if row.get('type') == 'email' else '') + row.get('value', '')
                if attrs.get('href') != expected:
                    out.append(Error('G1', f'contact {cid} points elsewhere'))
    return out


def run(content, public, ctx, production=False):
    out = []
    files = sorted(p for p in Path(content).rglob('*') if p.is_file())
    paths = [p for p in files if p.suffix == '.md']
    for path in files:
        if path.suffix != '.md':
            out.append(Error('G2', 'content files must use .md', str(path)))
    if not paths:
        return out + [Error('G3', 'no content pages found; check --content path')]
    languages_with_pages = {p.relative_to(content).parts[0] for p in paths}
    live_reader_pages = False
    for path in paths:
        language = path.relative_to(content).parts[0]
        meta, body = frontmatter(path)
        errors = source_checks(meta, body, ctx, language)
        section = path.relative_to(Path(content) / language).parts[0]
        if section in {'playbooks', 'cards'} and meta.get('kind') != {'playbooks': 'playbook', 'cards': 'card'}[section]:
            errors.append(Error('G8', 'missing or unknown kind in reader section'))
        if meta.get('draft') is False and meta.get('kind') in {'playbook', 'card'}:
            live_reader_pages = True
        slug = path.relative_to(Path(content) / language).with_suffix('')
        built = Path(public) / ('' if language == 'en' else language) / slug / 'index.html'
        if built.exists():
            if production and meta.get('draft') is True:
                errors.append(Error('G3', 'draft page has production output'))
            built_text = built.read_text(encoding='utf-8')
            errors += check_document(built_text, ctx, meta.get('kind', ''), meta.get('draft') is False)
            doc = Document()
            doc.feed(built_text)
            shares = []
            for _, attrs, _ in doc.elements:
                if 'data-share' in attrs:
                    base = ctx.contacts.get(attrs.get('data-contact'), {}).get('value', '')
                    shares.append(unquote_plus(attrs.get('href', '')[len(base):]))
            if shares:
                from formats import project
                permalink = ('/' if language == 'en' else '/' + language + '/') + slug.as_posix() + '/'
                errors += share_parity(shares, project(meta, body, ctx, language, permalink)['whatsapp'])
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
        gates = {'G1', 'G4', 'G7'}
        if doc.language in languages_with_pages and not redirect:
            gates.add('G6')
        out += [e for e in check_document(text, ctx, kind='') if e.gate in gates]
    for path in Path(public).rglob('*.css'):
        if re.search(r'url\s*\(|@import|@font-face', path.read_text(encoding='utf-8'), re.I):
            out.append(Error('G4', 'CSS resource or web font', str(path)))
    for path in ['method/index.html', 'corrections/index.html', '.well-known/security.txt'] if live_reader_pages else []:
        if not (Path(public) / path).exists():
            out.append(Error('G3', f'required site path missing: {path}'))
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--content', type=Path, default=ROOT / 'content')
    parser.add_argument('--public', type=Path, default=ROOT / 'public')
    parser.add_argument('--facts', type=Path, default=ROOT / 'rules/facts.md')
    parser.add_argument('--contacts', type=Path, default=ROOT / 'rules/contacts.md')
    parser.add_argument('--production', action='store_true')
    args = parser.parse_args()
    try:
        errors = run(args.content, args.public, Context.load(args.facts, args.contacts), production=args.production)
    except (OSError, ValueError, KeyError) as exc:
        raise SystemExit(f'GATES RED: {exc}')
    for error in errors:
        print(error)
    for gate in GATES:
        print(f'{gate}: {"RED" if any(e.gate == gate for e in errors) else "GREEN"}')
    raise SystemExit(bool(errors))


if __name__ == '__main__':
    main()
