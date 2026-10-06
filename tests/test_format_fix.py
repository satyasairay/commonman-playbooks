import copy
from pathlib import Path
import sys
import unittest
import tempfile
import hashlib
import re
import shutil
from urllib.parse import quote_plus
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/gates'))
sys.path.insert(0, str(ROOT / 'scripts/facts'))
from gates import Context, frontmatter, run
from formats import project
from format_gate import check_format
import build_pdfs

class FixFormatTests(unittest.TestCase):
    def setUp(self):
        self.ctx = Context.fixture()
        self.meta, self.body = frontmatter(ROOT / 'tests/fixtures/site/en/playbooks/test-page.md')
        self.record = project(self.meta, self.body, self.ctx, 'en', '/playbooks/test-page/')
        self.print = (ROOT / 'tests/fixtures/gates/print.html').read_text(encoding='utf-8')

    def errors(self, html):
        return check_format('print', html, self.record, self.ctx, pages=1)

    def test_S15_scope_and_clock_are_projected(self):
        self.assertEqual([s['text'] for s in self.record['scope']], ['This page covers a test.', 'It does not cover real advice.'])
        self.assertIn('three days', self.record['clock'][0]['text'])
        for old in ('This page covers a test.', 'It does not cover real advice.', 'Read the test note within three days of this test under the test rule.'):
            self.assertTrue(any('whole visible' in e.note for e in self.errors(self.print.replace(old, ''))))

    def test_S20_status_uses_i18n(self):
        self.ctx.labels['en']['unsigned']['other'] = 'TEST unsigned label'
        record = project(self.meta, self.body, self.ctx, 'en', '/playbooks/test-page/')
        self.assertEqual(record['checked'], 'TEST unsigned label')
        self.ctx.labels['en']['checked']['other'] = 'TEST checked label'
        meta = dict(self.meta, verified_on='6 October 2026')
        self.assertEqual(project(meta, self.body, self.ctx, 'en', '/playbooks/test-page/')['checked'], 'TEST checked label 6 October 2026')

    def test_whatsapp_requires_C01(self):
        self.assertIn(self.ctx.contacts['C01']['value'], self.record['whatsapp'])
        self.ctx.contacts['C01']['status'] = 'pending'
        with self.assertRaisesRegex(ValueError, 'C01'):
            project(self.meta, self.body, self.ctx, 'en', '/playbooks/test-page/')

    def test_whatsapp_missing_C01_even_if_canonical(self):
        text = self.record['whatsapp'].replace(self.ctx.contacts['C01']['value'], '')
        record = dict(self.record, whatsapp=text)
        self.assertTrue(any('C01' in e.note for e in check_format('whatsapp', text, record, self.ctx)))

    def test_whatsapp_capitals_even_if_canonical(self):
        text = self.record['whatsapp'].replace('*Test page*', '*URGENT*')
        record = dict(self.record, whatsapp=text)
        self.assertTrue(any('capital' in e.note for e in check_format('whatsapp', text, record, self.ctx)))

    def test_print_whole_visible_sheet(self):
        for changed in (self.print.replace('<h1>Test page</h1>', '<h1>Wrong title</h1>'), self.print.replace('</main>', '<p>Read the note.</p></main>'), self.print.replace('</body>', '<p>Read the note.</p></body>')):
            self.assertTrue(any('whole visible' in e.note for e in self.errors(changed)))

    def test_print_rejects_scaling_and_small(self):
        for addition in ('p { transform: scale(0.5); }', 'body { zoom: 0.5; }'):
            self.assertTrue(any('shrink' in e.note for e in self.errors(self.print.replace('</style>', addition + '</style>'))))
        self.assertTrue(any('shrink' in e.note for e in self.errors(self.print.replace('Read the test note.', '<small>Read the test note.</small>'))))

    def test_S12_print_address_control(self):
        self.assertTrue(any('address' in e.note for e in self.errors(self.print.replace(self.record['page_url'], ''))))

    def test_S12_print_status_control(self):
        self.assertTrue(any('check status' in e.note for e in self.errors(self.print.replace(self.record['checked'], ''))))

    def test_address_is_large(self):
        self.assertTrue(any('18pt' in e.note for e in self.errors(self.print.replace('font-size: 18pt', 'font-size: 14pt'))))

    def test_empty_production_has_no_pdf_to_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(build_pdfs.build(Path(tmp)), 0)

    def test_formats_nav_precedes_trust(self):
        html = (ROOT / '.cache/test-public/playbooks/test-page/index.html').read_text(encoding='utf-8')
        self.assertLess(html.index('data-frame="formats"'), html.index('data-frame="trust"'))

    def test_built_print_has_whole_source_frame(self):
        html = (ROOT / '.cache/test-public/playbooks/test-page/print.html').read_text(encoding='utf-8')
        self.assertEqual(self.errors(html), [])

    def test_built_share_is_exact_and_G12_checks_source(self):
        html = (ROOT / '.cache/test-public/playbooks/test-page/index.html').read_text(encoding='utf-8')
        self.assertIn('data-share-sha256="' + hashlib.sha256(self.record['whatsapp'].encode()).hexdigest() + '"', html)
        self.assertNotIn('data-share-text', html)
        with tempfile.TemporaryDirectory() as tmp:
            public = Path(tmp) / 'public'
            shutil.copytree(ROOT / '.cache/test-public', public)
            wrong = self.record['whatsapp'].replace('Read the test note.', 'Send the test note.')
            digest = hashlib.sha256(wrong.encode()).hexdigest()
            changed = re.sub(r'data-share-sha256="[^"]+"', 'data-share-sha256="' + digest + '"', html)
            changed = re.sub(r'href="https://wa.me/\?text=[^"]+"', lambda m: 'href="https://wa.me/?text=' + quote_plus(wrong) + '"', changed)
            (public / 'playbooks/test-page/index.html').write_text(changed, encoding='utf-8')
            self.assertTrue(any(e.gate == 'G12' and 'share link text differs' in e.note for e in run(ROOT / 'tests/fixtures/site', public, self.ctx)))

if __name__ == '__main__':
    unittest.main()
