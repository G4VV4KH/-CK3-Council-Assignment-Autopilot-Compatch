"""Portable merge regression checks; these do not replace native CK3 tests."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).absolute().parents[1]
TOOL = ROOT / 'tools/merge_council_window.py'
if not TOOL.exists():
    TOOL = Path(__file__).with_name('merge_council_window.py')
spec = importlib.util.spec_from_file_location('merge_tool', TOOL)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class MergeRegression(unittest.TestCase):
    def setUp(self):
        self.vanilla = b'header\n' + m.ANCHOR + b'\nfooter\n'
        self.insertion = m.MARKER + b'\nname = "caa_open_settings_button"\n'
        self.caa = self.vanilla.replace(m.ANCHOR, self.insertion + m.ANCHOR)
        self.autopilot = self.vanilla + b"GetScriptedGui('autopilot_fixture')\n"
        self.license = b'LICENSE FIXTURE ONLY\n'
        self.lock = {'inputs': {key: {'sha256': m.sha(value)} for key, value in
                     dict(caa=self.caa, autopilot=self.autopilot, vanilla=self.vanilla,
                          autopilot_license=self.license).items()}}

    def run_merge(self, caa=None, cap=None):
        return m.merge(self.caa if caa is None else caa, self.autopilot if cap is None else cap,
                       self.vanilla, self.license, self.lock)

    def test_autopilot_preserved_outside_exact_caa_insertion(self):
        output = self.run_merge()
        self.assertEqual(output.replace(self.insertion, b'', 1), self.autopilot)
        self.assertEqual(output.count(self.insertion), 1)

    def test_upstream_drift_requires_review(self):
        with self.assertRaisesRegex(ValueError, 'Upstream changed'):
            self.run_merge(cap=self.autopilot + b'change')

    def test_ambiguous_anchor_rejected_even_when_rehashed(self):
        cap = self.autopilot + m.ANCHOR
        self.lock['inputs']['autopilot']['sha256'] = m.sha(cap)
        with self.assertRaisesRegex(ValueError, 'ambiguous'):
            self.run_merge(cap=cap)

    def test_extra_caa_change_rejected_even_when_rehashed(self):
        caa = self.caa + b'not the button'
        self.lock['inputs']['caa']['sha256'] = m.sha(caa)
        with self.assertRaisesRegex(ValueError, 'exceed'):
            self.run_merge(caa=caa)


if __name__ == '__main__':
    unittest.main()
