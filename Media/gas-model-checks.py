#!/usr/bin/env python3
"""Regression checks for medium selection and fail-closed sensitivity verification."""
import contextlib
import io
import math
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile

HERE = Path(__file__).resolve().parent
SENS = HERE / 'electroPioreactorGasModel-sensitivity.py'
TWIN = HERE / 'electroPioreactorGasModel.py'
BOOK = HERE / 'electroPioreactorGasModel.xlsx'


class GasModelChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()):
            cls.sens = runpy.run_path(str(SENS))

    def test_all_media_against_independent_twin(self):
        for medium in ('MC02', 'UdG phosphate', 'AMYBO03'):
            with self.subTest(medium=medium):
                src = re.sub(r'^media_sel\s*=\s*"[^"]*"',
                             f'media_sel = "{medium}"', TWIN.read_text(), flags=re.M)
                ns = {'__name__': 'test_twin', '__file__': str(TWIN)}
                exec(compile(src, str(TWIN), 'exec'), ns)
                got = self.sens['medium_chemistry'](dict(self.sens['BASE'], media=medium))
                expected = [ns[k] for k in ('pH_SID', 'pH_PT', 'pH_NT', 'pH_Cl', 'I_ionic')]
                expected.append(ns[{'MC02': 'kappa0_mc02', 'UdG phosphate': 'kappa0_udg',
                                    'AMYBO03': 'kappa0_amy'}[medium]])
                for a, b in zip(got, expected):
                    self.assertTrue(math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-14), (a, b))

    def test_unknown_medium_rejected(self):
        with self.assertRaises(KeyError):
            self.sens['medium_chemistry'](dict(self.sens['BASE'], media='typo'))

    def test_stale_cache_stops_before_sweeps(self):
        with tempfile.TemporaryDirectory() as directory:
            dst = Path(directory)
            shutil.copy2(SENS, dst / SENS.name)
            shutil.copy2(TWIN, dst / TWIN.name)
            with zipfile.ZipFile(BOOK) as zin, zipfile.ZipFile(dst / BOOK.name, 'w') as zout:
                changed = 0
                for item in zin.infolist():
                    data = zin.read(item.filename)
                    if item.filename == 'xl/worksheets/sheet3.xml':
                        text, changed = re.subn(r'(<c\b[^>]*r="D88"[^>]*>.*?<v>)[^<]*(</v>)',
                                                r'\g<1>999\2', data.decode(), flags=re.S)
                        data = text.encode()
                    zout.writestr(item, data)
            self.assertEqual(changed, 1)
            result = subprocess.run([sys.executable, str(dst / SENS.name)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('WORKBOOK MISMATCH', result.stdout)
            self.assertNotIn('HEADSPACE SELECTORS -- headline', result.stdout)


if __name__ == '__main__':
    unittest.main()
