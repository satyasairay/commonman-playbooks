import hashlib
from pathlib import Path
import sys
import unittest
from urllib.parse import quote, quote_plus
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/gates'))
import gates

class ShareControlTests(unittest.TestCase):
    def setUp(self):
        self.ctx = gates.Context.fixture()
        self.ctx.contacts['C18'] = {'type': 'url-base', 'value': 'https://wa.me/?text=', 'status': 'verified'}
        self.html = (ROOT / '.cache/test-public/playbooks/test-page/index.html').read_text(encoding='utf-8')

    def test_S12_share_link_parity_control(self):
        self.assertEqual(gates.share_parity(['Read the note.'], 'Read the note.'), [])
        self.assertIn('G12', {e.gate for e in gates.share_parity(['Send the note.'], 'Read the note.')})

    def test_verified_share_base_hash_and_label(self):
        text = 'Read the note.\nhttps://satsangee.org/test/'
        digest = hashlib.sha256(text.encode()).hexdigest()
        share = '<a data-contact="C18" data-share data-share-sha256="' + digest + '" href="https://wa.me/?text=' + quote(text, safe='') + '">WhatsApp</a>'
        html = self.html.replace('</article>', share + '</article>')
        self.assertEqual(gates.check_document(html, self.ctx), [])
        for changed in (html.replace(digest, '0' * 64), html.replace('https://wa.me/?text=', 'https://example.invalid/?text='), html.replace('>WhatsApp<', '>paisa<')):
            self.assertIn('G1', {e.gate for e in gates.check_document(changed, self.ctx)})

    def test_hugo_share_space_encoding(self):
        text = 'Read the note.'
        digest = hashlib.sha256(text.encode()).hexdigest()
        share = '<a data-contact="C18" data-share data-share-sha256="' + digest + '" href="https://wa.me/?text=' + quote_plus(text) + '">WhatsApp</a>'
        self.assertEqual(gates.check_document(self.html.replace('</article>', share + '</article>'), self.ctx), [])

    def test_canonical_print_address_frame(self):
        html = self.html.replace('<p data-no-contact>', '<p data-page-url>https://satsangee.org/test/</p><p data-no-contact>')
        self.assertEqual(gates.check_document(html, self.ctx), [])
        self.assertIn('G1', {e.gate for e in gates.check_document(html.replace('https://satsangee.org/test/', 'https://example.invalid/test/'), self.ctx)})

if __name__ == '__main__':
    unittest.main()
