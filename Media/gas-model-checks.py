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
        self.assertEqual(f('K142'), 'IF(OR(G142="",H142="",I142=""),"",IFERROR((G142/1000)/(n_e_fcn*F_const*(H142/10000)*I142)*100,""))')
        self.assertEqual(f('L142'), 'IF(OR(K142="",J142=""),"",IFERROR(K142*(D_O2/J142)^km_exp,""))')
        self.assertEqual(f('I155'), 'IF(OR(E155="",F155="",G155="",H155=""),"",IF(E155/M_Cl2>=G155,"not invertible: plateau at or above the chloride pool",IFERROR(MAX(E155/M_Cl2/(F155*(G155-E155/M_Cl2)),E155/M_Cl2/H155)/3600,"")))')
        self.assertIn('AVERAGEIFS(L142:L149,C142:C149,Reactor_sel,D142:D149,electrode_sel,N142:N149,"y",E142:E149,stir_rpm_set,'
                      'F142:F149,"&gt;="&amp;(temp_C-km_T_tol),F142:F149,"&lt;="&amp;(temp_C+km_T_tol))', sh)
        self.assertIn('AVERAGEIFS(I155:I162,C155:C162,Reactor_sel,D155:D162,media_sel,K155:K162,"y")', sh.replace('&quot;', '"'))

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
        self.assertEqual(f('D317'), 'Summary!NaHCO3_add_gL')
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
        self.assertIn('IF(ph_unreach,NA(),MIN(spg_int_carbon,IF(ISNUMBER(spg_int_DO),spg_int_DO,spg_int_max),IF(ISNUMBER(spg_int_pH_opt),spg_int_pH_opt,spg_int_carbon),IF(O2_sizing_phase=phase_name_2,IF(ISNUMBER(spg_int_H2safe_opt),spg_int_H2safe_opt,spg_int_carbon),spg_int_carbon))))', f('D91'))
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

    def test_startup_schedule_and_resolution_input(self):
        base = self.twin()
        self.assertIn('legacy', base['su_binding'])
        self.assertLess(base['y_H2_end_su'], 0.04)
        self.assertEqual(base['_H2safe_e'], base['spg_int_H2safe_saw'])    # early H2 screen = Biology D92
        # The start-up schedule is exactly the Lag-sized headline, whichever bound binds (review finding 3).
        for kw in ({}, dict(kLa_meas=100.0), dict(N2_sweep_set=20.0, NaHCO3_add_gL=2.0), dict(vent_model_sel='Outflow only')):
            g = self.twin(**kw)
            l = self.twin(O2_phase_sel='Lag', **kw)
            if isinstance(g['spg_int_su_run'], float) and math.isnan(g['spg_int_su_run']):
                self.assertTrue(math.isnan(l['spg_int']), kw)
            else:
                self.assertEqual(g['spg_int_su_run'], l['spg_int'], (kw, g['su_binding'], l['opt_binding']))
        hk = self.twin(kLa_meas=100.0)
        self.assertIn('H\u2082', hk['su_binding'])
        self.assertTrue(self.twin(O2_phase_sel='Lag', kLa_meas=100.0)['opt_binding'].startswith('H\u2082 FLAMMABILITY'))
        # Lag pH ceiling now bounds the start-up schedule (review finding 2).
        x = self.twin(N2_sweep_set=20.0, NaHCO3_add_gL=2.0)
        self.assertTrue(isinstance(x['spg_int_pH_l'], float))
        self.assertLessEqual(x['spg_int_su_opt'], x['spg_int_pH_l'] * x['spg_dur_eq_opt'] / x['spg_dur_eq'] + 1e-9)
        # Command resolution is an input; the floor is rounded up to it too (review finding 1).
        r = self.twin(pulse_res_set=0.1)
        self.assertTrue(math.isclose(r['spg_dur_run'], 0.7, rel_tol=1e-12))
        c = self.twin(pulse_res_set=1.0, media_volume=16.0)
        self.assertTrue(math.isclose(c['spg_dur_run'] % 1.0, 0.0, abs_tol=1e-9) or math.isclose(c['spg_dur_run'] % 1.0, 1.0, abs_tol=1e-9), c['spg_dur_run'])
        m = self.sens['model'](dict(self.sens['BASE'], pulse_res=0.1))
        self.assertTrue(math.isclose(r['spg_int'], m['spg_int_run'], rel_tol=5e-3))
        # An unlisted schedule mode returns no schedule, as the workbook does (review finding 5).
        self.assertTrue(math.isnan(self.twin(sched_mode='typo')['spg_int']))

    def test_review2_fixes(self):
        # DO sizing uses the commanded pulse: the evaluated mean DO sits on the target even when the
        # commanded pulse is far from the ideal one (review 2, finding 1).
        for kw in ({}, dict(media_volume=16.0, pulse_res_set=1.0), dict(user_spg_dur=2.0)):
            n = self.twin(**kw)
            self.assertLess(abs(n['DO_ss'] / (n['DO_target'] * n['M_O2']) - 1), 0.01, (kw, n['DO_ss']))
        # The pH grid starts at the shortest executable interval, so a short ceiling is found, not
        # mistaken for infeasibility (finding 2).
        x = self.twin(media_volume=16.0, N2_sweep_set=20.0, NaHCO3_add_gL=8.0)
        self.assertFalse(x['ph_unreach_l'])
        self.assertTrue(math.isclose(x['grid_t_min'], math.floor(x['spg_dur'] / 60 / 0.01 + 1e-12) * 0.01 + 0.01, rel_tol=1e-12))
        self.assertGreater(x['grid_t_min'] * 60, x['spg_dur'])                      # executable
        # Knallgas ratios are averaged per run on an H2 basis (finding 3): pinned formula text.
        with zipfile.ZipFile(BOOK) as z:
            cal = z.read('xl/worksheets/sheet8.xml').decode().replace('&quot;', '"').replace('&gt;', '>')
        self.assertIn('knall_H2_basis*AVERAGEIFS(I112:I119,C112:C119,organism_sel,G112:G119,"y")', cal)
        self.assertIn('IFERROR(IF(D112>0,E112/D112,""),"")', cal)
        # Lag H2 time mean exists for time-weighted comparisons (finding 4) and lies between the flux mean and the top.
        self.assertTrue(self.twin()['y_H2_avg_l'] > 0)

    def test_review3_fixes(self):
        # The grid starts at the first command step above the pulse (0.4 s pulse -> 0.01 min).
        g = self.twin(user_spg_dur=0.4)
        self.assertTrue(math.isclose(g['grid_t_min'], 0.01, rel_tol=1e-9))
        # The sensitivity model's O2 ceiling uses the standard atmosphere, as Biology D26 (finding 2).
        for patm in (80000.0, 101325.0):
            t = self.twin(P_atm_set=patm)
            m = self.sens['model'](dict(self.sens['BASE'], P_atm=patm))
            self.assertTrue(math.isclose(t['DO_target'], m['DO_target'], rel_tol=1e-6), (patm, t['DO_target'], m['DO_target']))
        # Sinter grades outside the listed classes are not invented (finding 4): formula text pinned.
        with zipfile.ZipFile(BOOK) as z:
            cal = z.read('xl/worksheets/sheet8.xml').decode().replace('&quot;', '"').replace('&gt;', '>').replace('&lt;', '<')
        self.assertIn('"between or below the listed grades – not used"', cal)
        self.assertIn('AND((bp_const/D81)>=por_p5_lo,(bp_const/D81)<=por_p5_hi),5', cal)

    def test_review4_fixes(self):
        # Peroxide: judged on the lag plateau, not the 1-hour level (finding 1).
        n = self.twin(km_O2_default=0.0003)
        if isinstance(n['t_H2O2_thresh'], float) and not math.isnan(n['t_H2O2_thresh']):
            self.assertTrue(n['H2O2_flag'].startswith('watch'))
        # Voltage cross-check: 25 % for Gerrit's default fit, the 10 % clamp for a Calibrations fit (finding 4).
        self.assertEqual(self.twin()['gerrit_check_pct'], 25.0)
        self.assertEqual(self.twin(cal_gerrit_slope=1.2)['gerrit_check_pct'], 10.0)
        # Physical depth is never replaced by the volume-equivalent calibration depth (finding 3).
        with zipfile.ZipFile(BOOK) as z:
            geo = z.read('xl/worksheets/sheet2.xml').decode()
        d22 = re.search(r'<c r="D22"[^>]*><f>([^<]*)</f>', geo).group(1)
        self.assertNotIn('cal_Dint', d22)

    def test_review5_fixes(self):
        # A measured toxic DO caps the target and the peak checks (finding 1).
        t = self.twin(DO_toxic=2.0)
        self.assertLessEqual(t['DO_target'] * t['M_O2'], 2.0 + 1e-9)
        self.assertTrue(math.isclose(t['O2_ceil_org'] * t['M_O2'], 2.0, rel_tol=1e-12))
        # Sinter: graded once from the averaged bubble point, never a fractional grade (finding 3).
        with zipfile.ZipFile(BOOK) as z:
            cal = z.read('xl/worksheets/sheet8.xml').decode().replace('&quot;', '"').replace('&gt;', '>')
        d89 = re.search(r'<c r="D89"[^>]*><f>([^<]*)</f>', cal).group(1)
        self.assertIn('(bp_const/cal_bp)', d89)
        self.assertNotIn('AVERAGEIFS(E81', d89)

    def test_review6_fixes(self):
        # The sensitivity model carries the organism toxic ceiling too (finding 1).
        t = self.twin(DO_toxic=2.0)
        m = self.sens['model'](dict(self.sens['BASE'], DO_toxic=2.0))
        self.assertTrue(math.isclose(t['DO_target'], m['DO_target'], rel_tol=1e-9))
        self.assertTrue(math.isclose(t['spg_int'], m['spg_int_run'], rel_tol=5e-3), (t['spg_int'], m['spg_int_run']))
        # Anodic peroxide oxidation closes the O2 balance (finding 3): growth and lag sources
        # equal anode O2 + returned O2 - cathode loss, with the charge taken off the OER.
        n = self.twin()
        F = n['F_const']
        self.assertTrue(math.isclose(n['f_H2O2_anode'], 2 * F * n['r_H2O2_an_g'] / 3600 / n['I_app'], rel_tol=1e-12))
        oer_lag = n['I_app'] * (n['etaF_OER'] + n['f_H2O2_anode']) / (4 * F) * 3600 - n['r_H2O2_an_l'] / 2
        self.assertTrue(math.isclose(n['O2_net_lag'], oer_lag + n['r_H2O2_an_l'] - n['O2_ORR_lag'], rel_tol=1e-12))
        self.assertTrue(math.isclose(n['O2_net_lag'], self.sens['model'](self.sens['BASE'])['O2_net_lag'], rel_tol=1e-9))

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
