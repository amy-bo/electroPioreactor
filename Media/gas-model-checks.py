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

    def twin(self, **overrides):
        src = TWIN.read_text()
        for key, value in overrides.items():
            src, count = re.subn(r'(?m)^' + re.escape(key) + r'\s*=.*$',
                                 key + ' = ' + repr(value), src)
            self.assertEqual(count, 1, key)
        ns = {'__name__': 'test_twin', '__file__': str(TWIN)}
        exec(compile(src, str(TWIN), 'exec'), ns)
        return ns

    def test_dry_headspace_co2_conservation(self):
        n = self.twin()
        # Vent loss F*C/Csat must equal pool decay coefficient times stored moles.
        self.assertTrue(math.isclose(n['k_eff_CO2'] * (n['V_L_CO2'] + n['Vg_CO2']),
                                     n['F_gap_sched'] / 3600 / n['C_sat_CO2'], rel_tol=1e-12))
        self.assertTrue(math.isclose(n['n_hs_gas'], n['P_dry'] * n['headspace_V_m3'] /
                                     (n['R_gas'] * n['T_K']), rel_tol=1e-12))

    def test_dashboard_and_operating_schedule_are_identical(self):
        for settings in ({}, dict(user_spg_dur=0.5, user_spg_int=3.25),
                         dict(sched_mode='Manual', spg_dur_man=0.4, spg_int_man=2.5)):
            with self.subTest(settings=settings):
                n = self.twin(**settings)
                self.assertEqual(n['S_D14'], n['spg_dur'])
                self.assertEqual(n['S_D16'], n['spg_int'])
        self.assertTrue(math.isnan(self.twin(user_spg_dur=60, user_spg_int=1)['spg_int']))

    def test_chlorine_requires_electrical_production(self):
        p = dict(self.sens['BASE'], media='UdG phosphate', FE_CER=0)
        self.assertEqual(self.sens['model'](p)['C_eff_Cl2'], 0)
        n = self.twin(media_sel='UdG phosphate', FE_CER=0)
        self.assertEqual(n['NH2Cl_mgL'], 0)
        self.assertEqual(n['Cl_free_frac'], 1)

    def test_lag_peroxide_matches_capped_oxygen_budget(self):
        for settings in ({}, dict(DO_lag_ref=10)):
            n = self.twin(**settings)
            self.assertLessEqual(n['O2_ORR_lag'] * n['n_ORR_eff'] * n['F_const'] / 3600,
                                 n['I_app'] * (1 + 1e-12))
            self.assertTrue(math.isclose(n['r_H2O2_lag'] * n['ec_V_L'] /
                                         (n['M_H2O2'] * 1000), n['f_HOOH'] * n['O2_ORR_lag'], rel_tol=1e-12))

    def test_zero_biological_surplus_is_defined(self):
        n = self.twin(bio_O2=4)
        self.assertEqual(n['O2_excess'], 0)
        self.assertEqual(n['t_O2_ceiling'], 'never (source <= 0)')
        self.assertEqual(n['kLa_margin_g'], 'no positive source')

    def test_power_outside_model_domain_is_rejected(self):
        for power in (0, 2, 11, 25):
            with self.subTest(power=power):
                with self.assertRaises(SystemExit):
                    self.twin(led_intensity=power)
                with self.assertRaises(ValueError):
                    self.sens['model'](dict(self.sens['BASE'], intensity=power))

    def test_full_definition_guard_catches_uncompared_input(self):
        from gas_model_verification import verify_definition, RECORD
        with tempfile.TemporaryDirectory() as directory:
            dst = Path(directory)
            shutil.copy2(HERE / RECORD, dst / RECORD)
            with zipfile.ZipFile(BOOK) as zin, zipfile.ZipFile(dst / BOOK.name, 'w') as zout:
                changed = 0
                for item in zin.infolist():
                    data = zin.read(item.filename)
                    if item.filename == 'xl/worksheets/sheet3.xml':
                        text, changed = re.subn(r'(<c\b[^>]*r="D83"[^>]*>.*?<v>)[^<]*(</v>)',
                                                r'\g<1>0.005\2', data.decode(), flags=re.S)
                        data = text.encode()
                    zout.writestr(item, data)
            self.assertEqual(changed, 1)
            with self.assertRaisesRegex(SystemExit, 'WORKBOOK DEFINITION DRIFT'):
                verify_definition(dst / BOOK.name)

    def test_unknown_medium_rejected(self):
        with self.assertRaises(KeyError):
            self.sens['medium_chemistry'](dict(self.sens['BASE'], media='typo'))

    def test_stale_cache_stops_before_sweeps(self):
        with tempfile.TemporaryDirectory() as directory:
            dst = Path(directory)
            shutil.copy2(SENS, dst / SENS.name)
            shutil.copy2(TWIN, dst / TWIN.name)
            for filename in ('gas_model_verification.py', 'electroPioreactorGasModel-verification.json'):
                shutil.copy2(HERE / filename, dst / filename)
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
