import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts/facts'))
from registry import read


class RegistryTests(unittest.TestCase):
    def test_real_registry_exports_nothing(self):
        facts, contacts, _ = read(ROOT / 'rules/facts.md', ROOT / 'rules/contacts.md')
        self.assertFalse([r for r in facts.values() if r['status'] == 'verified'])
        self.assertFalse([r for r in contacts.values() if r['status'] == 'verified'])

    def test_fixture_has_one_fact_and_contact(self):
        facts, contacts, _ = read(ROOT / 'tests/fixtures/registries/facts.md', ROOT / 'tests/fixtures/registries/contacts.md')
        self.assertEqual(facts['TEST-STEP-01']['statements']['en'], 'Read the test note.')
        self.assertEqual(contacts['C99']['status'], 'verified')

    def test_port_keeps_text_normalisation(self):
        spec = importlib.util.spec_from_file_location('fetch_text', ROOT / 'scripts/sources/fetch_text.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        raw = b'<p>A  quote.</p><script>hidden</script><p>Next&nbsp;line.</p>'
        self.assertEqual(module.html_to_text(raw), 'A quote.\nNext line.\n')


if __name__ == '__main__':
    unittest.main()
