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
                self.assertEqual(n['S_D19'], n['spg_dur'])
                self.assertEqual(n['S_D21'], n['spg_int'])
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
                        text, changed = re.subn(r'(<c\b[^>]*r="D165"[^>]*>.*?<v>)[^<]*(</v>)',
                                                r'\g<1>0.005\2', data.decode(), flags=re.S)
                        data = text.encode()
                    zout.writestr(item, data)
            self.assertEqual(changed, 1)
            with self.assertRaisesRegex(SystemExit, 'WORKBOOK DEFINITION DRIFT'):
                verify_definition(dst / BOOK.name)

    def test_calibrated_km_and_tau_reach_the_model(self):
        n = self.twin()
        # Limiting-current definition: 0.5 mA at 2 cm2 and 5 mM ferricyanide.
        k_fcn = n['km_ferricyanide'](0.5, 2.0, 5.0)
        self.assertTrue(math.isclose(k_fcn, 0.5e-3 / (96485.33212 * 2e-4 * 5) * 100, rel_tol=1e-12))
        D_fcn = 7.2e-10
        k_O2 = n['km_O2_from_ferricyanide'](k_fcn, D_fcn, n['D_O2'])
        self.assertTrue(math.isclose(k_O2, k_fcn * (n['D_O2'] / D_fcn) ** 0.644, rel_tol=1e-12))
        row = ('ED04', 'MMO tube', 1000.0, 30.0, 0.5, 2.0, 5.0, D_fcn, 'Y')     # Excel criteria ignore case
        off = [('ed04', 'MMO tube', 500.0, 30.0, 0.5, 2.0, 5.0, D_fcn, 'y'),   # other rpm: not used
               ('ed04', 'MMO tube', 1000.0, 25.0, 9.9, 2.0, 5.0, D_fcn, 'y'),  # outside the 1 K tolerance
               ('ed06', 'MMO tube', 1000.0, 30.0, 9.9, 2.0, 5.0, D_fcn, 'y'),  # other reactor
               ('ed04', 'Pt-Ti rod', 1000.0, 30.0, 9.9, 2.0, 5.0, D_fcn, 'y'), # other electrode
               ('ed04', 'MMO tube', 1000.0, 30.0, 9.9, 2.0, 5.0, None, 'y'),    # missing D: skipped, as AVERAGEIFS skips ""
               ('ed04', 'MMO tube', 1000.0, 30.0, 9.9, 2.0, 5.0, D_fcn, 'n')]  # not included
        self.assertTrue(math.isnan(n['cal_km_O2_of'](off, n['D_O2'])))
        cal = self.twin(KM_CAL=[row] + off)
        self.assertTrue(math.isclose(cal['km_O2'], k_O2, rel_tol=1e-12))
        self.assertTrue(math.isclose(cal['i_ORR_design'] / n['i_ORR_design'], k_O2 / 4e-3, rel_tol=1e-12))
        # Lifetime: forward steady state at a known tau, then invert it (both branches).
        u = self.twin(media_sel='UdG phosphate')
        self.assertEqual(u['tau_NH2Cl'], 1)
        k, pool, P = u['k_Cl_turn'], u['pH_Cl'], u['P_Cl_max']
        for tau_true in (0.05, 1.0, 3.0, 40.0):
            ts = tau_true * 3600
            B = min(pool * k * ts / (1 + k * ts), P * ts)
            C_mgL = B * 70906
            back = u['tau_from_dpd'](C_mgL, k, pool, P)
            self.assertTrue(math.isclose(back, tau_true, rel_tol=1e-9), (tau_true, back))
        self.assertTrue(math.isnan(u['tau_from_dpd'](pool * 70906, k, pool, P)))
        t = self.twin(media_sel='UdG phosphate',
                      TAU_CAL=[('ed04', 'UdG phosphate', B * 70906, k, pool, P, 'y'),
                               ('ed04', 'MC02', 9.0, k, pool, P, 'y')])
        self.assertTrue(math.isclose(t['tau_NH2Cl'], 40.0, rel_tol=1e-9))
        self.assertNotEqual(t['Cl_bound'], u['Cl_bound'])

    def test_calibration_formulas_match_the_twin(self):
        """The calibration rows are hand-written XML; pin their formula text to the twin's algebra."""
        with zipfile.ZipFile(BOOK) as z:
            sh = z.read('xl/worksheets/sheet8.xml').decode()
        f = lambda ref: re.search(r'<c r="%s"[^>]*><f>([^<]*)</f>' % ref, sh).group(1).replace('&quot;', '"').replace('&gt;', '>').replace('&lt;', '<').replace('&amp;', '&')
        self.assertEqual(f('K168'), 'IF(OR(G168="",H168="",I168=""),"",IFERROR((G168/1000)/(n_e_fcn*F_const*(H168/10000)*I168)*100,""))')
        self.assertEqual(f('L168'), 'IF(OR(K168="",J168=""),"",IFERROR(K168*(D_O2/J168)^km_exp,""))')
        self.assertEqual(f('I181'), 'IF(OR(E181="",F181="",G181="",H181=""),"",IF(E181/M_Cl2>=G181,"not invertible: plateau at or above the chloride pool",IFERROR(MAX(E181/M_Cl2/(F181*(G181-E181/M_Cl2)),E181/M_Cl2/H181)/3600,"")))')
        self.assertIn('AVERAGEIFS(L168:L175,C168:C175,Reactor_sel,D168:D175,electrode_sel,N168:N175,"y",E168:E175,stir_rpm_set,'
                      'F168:F175,"&gt;="&amp;(temp_C-km_T_tol),F168:F175,"&lt;="&amp;(temp_C+km_T_tol))', sh)
        self.assertIn('AVERAGEIFS(I181:I188,C181:C188,Reactor_sel,D181:D188,media_sel,K181:K188,"y")', sh.replace('&quot;', '"'))

    def test_added_alkalinity_is_coupled(self):
        base = self.twin()
        dose = base['alk_NaHCO3_gL']                   # first-order NaHCO3 for the pH 6.5 floor
        n = self.twin(NaHCO3_add_gL=dose)
        add = dose / 84.007
        self.assertTrue(math.isclose(n['pH_SID'] - base['pH_SID'], add, rel_tol=1e-12))
        self.assertTrue(math.isclose(n['I_ionic'] - base['I_ionic'], add, rel_tol=1e-12))
        self.assertGreater(n['kappa_med'], base['kappa_med'])
        self.assertGreater(n['pH_meas'], base['pH_meas'])
        self.assertNotEqual(n['DIC_cap'], base['DIC_cap'])     # CO2 storage responds (dDIC/dCO2 falls as HCO3 rises)
        # Coupled result lands near the target the first-order estimate aimed for, and what is
        # still needed shrinks to a residual of the CO2-storage and ionic-strength feedback.
        self.assertLess(abs(n['pH_meas'] - 6.5), 0.01)
        self.assertLess(n['alk_needed'], 0.25 * base['alk_needed'])
        # Independent sensitivity model agrees at the non-default input.
        m = self.sens['model'](dict(self.sens['BASE'], NaHCO3_add_gL=dose))
        for k_t, k_s in (('kappa_med', 'kappa'), ('DIC_cap', 'DIC_cap'), ('pH_meas', 'pH_meas')):
            self.assertTrue(math.isclose(n[k_t], m[k_s], rel_tol=5e-3), (k_t, n[k_t], m[k_s]))

    def test_alkalinity_formulas_in_workbook(self):
        """The coupling is inert at baseline, so pin the workbook formula text and name scopes."""
        with zipfile.ZipFile(BOOK) as z:
            ch = z.read('xl/worksheets/sheet4.xml').decode()
            wb = z.read('xl/workbook.xml').decode()
        f = lambda ref: re.search(r'<c r="%s"[^>]*><f>([^<]*)</f>' % ref, ch).group(1).replace('&amp;', '&')
        self.assertTrue(f('D44').endswith(')))+alk_add_M'))
        self.assertTrue(f('D185').endswith(')))+alk_add_M'))
        self.assertIn('+alk_add_M*(lam_Na+lam_HCO3)/10)*kappa_fI', f('D180'))
        self.assertEqual(f('D317'), 'Summary!$D$13')
        self.assertEqual(f('D318'), 'NaHCO3_add_gL/M_NaHCO3')
        for name, sid, ref in (('NaHCO3_add_gL', 0, 'Summary!$D$13'), ('NaHCO3_add_gL', 3, 'Chemistry!$D$317'),
                               ('alk_add_M', 3, 'Chemistry!$D$318')):
            self.assertIn('<definedName name="%s" localSheetId="%d">%s</definedName>' % (name, sid, ref), wb)

    def test_n2_sweep_dilutes_without_co2(self):
        base = self.twin()
        self.assertEqual(base['F_dil'], base['F_vent_ex'])
        q = base['N2_for_DO']
        self.assertGreater(q, 0)
        n = self.twin(N2_sweep_set=q)
        self.assertTrue(math.isclose(n['F_dil'] - n['F_vent_ex'], n['F_N2'], rel_tol=1e-12))
        # At the sweep that holds DO with CO2 at the carbon duty, the O2 and carbon bounds coincide.
        self.assertTrue(math.isclose(n['spg_int_DO'], n['spg_int_carbon'], rel_tol=1e-6))
        self.assertGreater(n['spg_int'], base['spg_int'])
        self.assertGreater(n['pH_meas'], base['pH_meas'])
        # Lag H2 mean-field screen: the sweep from Biology D88 alone takes H2 to the LFL.
        h = self.twin(N2_sweep_set=base['N2_sweep_H2safe'])
        self.assertLessEqual(h['y_H2_hs_lag'], 0.04 * (1 + 1e-9))
        # Independent sensitivity model agrees at the non-default sweep.
        m = self.sens['model'](dict(self.sens['BASE'], N2_sweep=q))
        for k_t, k_s in (('spg_int', 'spg_int_run'), ('pH_meas', 'pH_meas'), ('DO_ss', 'DO_ss')):
            self.assertTrue(math.isclose(n[k_t], m[k_s], rel_tol=5e-3), (k_t, n[k_t], m[k_s]))

    def test_ph_ceiling_interval(self):
        base = self.twin()
        # Inert at baseline: far above the carbon and DO bounds.
        self.assertGreater(base['spg_int_pH'], base['spg_int_carbon'])
        self.assertEqual(base['opt_binding'], 'O2-DILUTION (headspace O2 sets the interval)')
        # The early (pre-schedule) pool constants equal the late ones, with and without a sweep.
        for kw in ({}, dict(N2_sweep_set=1.0), dict(N2_sweep_set=1.0, O2_phase_sel='Lag'),
                   dict(N2_sweep_set=1.0, vent_model_sel='Air exchange'), dict(user_spg_dur=1.0)):
            n = self.twin(**kw)
            for e, l in (('_k_eff_e', 'k_eff_CO2'), ('_pool_b_e', 'pool_b'), ('_pool_ret_e', 'pool_ret'),
                         ('_V_L_CO2_e', 'V_L_CO2'), ('_Vg_e', 'Vg_CO2'), ('_dur_eq_e', 'spg_dur_eq')):
                self.assertTrue(math.isclose(n[e], n[l], rel_tol=1e-12), (kw, e))
            self.assertTrue(math.isclose(n['co2_mean_at'](n['spg_int']), n['CO2_cyc_avg_new'], rel_tol=1e-12), kw)
        # With the sweep that frees CO2 from O2 duty, the pH ceiling binds and pH lands at the band ceiling.
        n = self.twin(N2_sweep_set=base['N2_for_DO'])
        self.assertTrue(n['opt_binding'].startswith('pH CEILING ('))
        self.assertTrue(math.isclose(n['spg_int_opt'], n['spg_int_pH_opt'], rel_tol=1e-12))
        self.assertLessEqual(n['spg_int'], n['spg_int_pH'] + 1e-9)
        self.assertLess(n['spg_int_pH'] - n['spg_int'], 0.011)
        self.assertTrue(7.47 < n['pH_meas'] <= 7.5 + 1e-9, n['pH_meas'])
        # Any pulse override: the executable interval is converted back, so pH still holds the ceiling.
        for dur in (0.3, 1.0, 2.0):
            o = self.twin(N2_sweep_set=1.0, user_spg_dur=dur)
            self.assertTrue(7.47 < o['pH_meas'] <= 7.5 + 1e-9, (dur, o['pH_meas']))
        # Unreachable ceiling: no schedule rather than the carbon interval.
        u = self.twin(N2_sweep_set=20.0, pH_band_hi=6.0)
        self.assertTrue(u['ph_unreach'])
        self.assertTrue(math.isnan(u['spg_int_opt']))
        self.assertTrue(u['opt_binding'].startswith('pH CEILING UNREACHABLE'))
        # MC02 never reaches the ceiling: no bound, and the carbon bound stands with a sweep.
        mc = self.twin(media_sel='MC02', N2_sweep_set=1.0)
        self.assertEqual(mc['spg_int_pH'], 'no pH bound')
        self.assertTrue(mc['opt_binding'].startswith('CARBON'))
        # The sensitivity model's independent bisection agrees with the workbook grid across states.
        for kw, skw in ((dict(N2_sweep_set=base['N2_for_DO']), dict(N2_sweep=base['N2_for_DO'])),
                        (dict(N2_sweep_set=1.0), dict(N2_sweep=1.0)),
                        (dict(N2_sweep_set=1.0, media_sel='UdG phosphate'), dict(N2_sweep=1.0, media='UdG phosphate')),
                        (dict(N2_sweep_set=1.0, vent_model_sel='Outflow only'), dict(N2_sweep=1.0, vent_model='Outflow only')),
                        (dict(N2_sweep_set=2.0, vent_model_sel='Air exchange'), dict(N2_sweep=2.0, vent_model='Air exchange'))):
            t = self.twin(**kw)
            m = self.sens['model'](dict(self.sens['BASE'], **skw))
            self.assertTrue(math.isclose(t['spg_int_pH'], m['spg_int_pH'], rel_tol=5e-3), (kw, t['spg_int_pH'], m['spg_int_pH']))
            self.assertTrue(math.isclose(t['spg_int'], m['spg_int_run'], rel_tol=5e-3), (kw, t['spg_int'], m['spg_int_run']))

    def test_ph_ceiling_formulas_in_workbook(self):
        with zipfile.ZipFile(BOOK) as z:
            mt = z.read('xl/worksheets/sheet6.xml').decode()
        f = lambda ref: re.search(r'<c r="%s"[^>]*><f>([^<]*)</f>' % ref, mt).group(1).replace('&quot;', '"').replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        self.assertEqual(f('D433'), 'IF(ISNUMBER(spg_int_pH),spg_int_pH*spg_dur_eq_opt/spg_dur_eq,"no pH bound")')
        self.assertIn('IF(ph_unreach,NA(),MIN(spg_int_carbon,IF(ISNUMBER(spg_int_DO),spg_int_DO,spg_int_max),IF(ISNUMBER(spg_int_pH_opt),spg_int_pH_opt,spg_int_carbon)))', f('D91'))
        self.assertEqual(f('I441'), 'MIN(C_sat_CO2,MAX(C_air_CO2,(pool_ret*H441+pool_b)*E441+G441*F441))')
        self.assertEqual(f('H441'), '(G441*E441+pool_b*D441)/(1-pool_ret*D441)')
        self.assertEqual(f('B441'), 'MAX(0,A441*60-spg_dur)')

    def test_no_cell_carries_two_names_in_one_scope(self):
        """A new parameter written over an existing named input would leave two names on one cell."""
        with zipfile.ZipFile(BOOK) as z:
            wb = z.read('xl/workbook.xml').decode()
        seen = {}
        for m in re.finditer(r'<definedName name="([^"]+)"(?: localSheetId="(\d+)")?[^>]*>([^<]*)</definedName>', wb):
            if ':' in m.group(3):
                continue
            key = (m.group(2), m.group(3))
            seen.setdefault(key, []).append(m.group(1))
        dup = {k: v for k, v in seen.items() if len(v) > 1}
        self.assertEqual(dup, {})

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
