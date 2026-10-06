"""Read the repository's Markdown registries without third-party packages."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def table(text, headers):
    rows = []
    for line in text.splitlines():
        if not line.startswith('|'):
            continue
        cells = [c.strip().strip('`') for c in re.split(r'(?<!\\)\|', line.strip().strip('|'))]
        if len(cells) != len(headers) or cells[0] in {headers[0], '(none yet)'} or re.fullmatch(r'[-: ]+', cells[0]):
            continue
        rows.append(dict(zip(headers, cells)))
    return rows


def read(facts_path, contacts_path):
    text = Path(facts_path).read_text(encoding='utf-8')
    source_section = text.split('## Sources', 1)[1].split('\n## ', 1)[0]
    sources = {r['id']: r for r in table(source_section, ['id', 'title', 'owner', 'url', 'sha256', 'fetched']) if r['url'].startswith('https://')}
    body = text.split('\n## Facts', 1)[1].split('\n## Candidate facts', 1)[0]
    facts = {}
    for block in re.split(r'\n### ', body)[1:]:
        fid, _, body = block.partition('\n')
        fields = dict(re.findall(r'^- \*\*(.+?):\*\*\s*(.*)$', body, re.M))
        src = fields.get('source', '').split(',', 1)
        source = sources.get(src[0].strip(), {})
        checked = fields.get('verified on / by', '').split('/', 1)
        facts[fid.strip()] = {
            'status': fields.get('status', ''), 'kind': fields.get('kind', ''),
            'statements': {k.split('.', 1)[1]: v for k, v in fields.items() if k.startswith('statement.')},
            'conditions': fields.get('conditions', ''), 'quote': fields.get('quote', '').strip('"“”').replace('\\|', '|'),
            'source': src[0].strip(), 'source_url': source.get('url', ''), 'source_title': source.get('title', ''),
            'source_location': src[1].strip() if len(src) > 1 else '',
            'verified_on': fields.get('verified on', checked[0].strip()),
            'verified_by': fields.get('verified by', checked[1].strip() if len(checked) > 1 else ''),
            'recheck_by': fields.get('recheck by', ''), 'applies_to': fields.get('applies to', ''),
        }
    headers = ['id', 'name', 'value', 'type', 'owner', 'source', 'quote', 'verified_on', 'verified_by', 'status']
    contacts = {r['id']: r for r in table(Path(contacts_path).read_text(encoding='utf-8'), headers) if re.fullmatch(r'C\d+', r['id'])}
    return facts, contacts, sources
