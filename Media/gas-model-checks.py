#!/usr/bin/env python3
"""Regression checks for medium selection and fail-closed sensitivity verification."""
import contextlib
import html
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


def _shift(formula, dr, dc):
    """Move the relative A1 references of a shared formula by (dr, dc), leaving strings and names alone."""
    def col2n(c):
        n = 0
        for ch in c:
            n = n * 26 + ord(ch) - 64
        return n

    def n2col(n):
        s = ''
        while n:
            n, r = divmod(n - 1, 26)
            s = chr(65 + r) + s
        return s

    def ref(m):
        cd, c, rd, r = m.groups()
        return cd + (c if cd else n2col(col2n(c) + dc)) + rd + (r if rd else str(int(r) + dr))
    parts = re.split(r'("(?:[^"]|"")*")', formula)
    tok = re.compile(r'(?<![A-Za-z_0-9.$])(\$?)([A-Z]{1,3})(\$?)(\d+)(?![A-Za-z_0-9(])')
    return ''.join(p if p.startswith('"') else tok.sub(ref, p) for p in parts)


def cell_formula(sheet_xml, ref):
    """Formula text of one cell, unescaped; a shared-formula child is rebuilt from its master."""
    import html
    m = re.search(r'<c r="%s"[^>]*>(?:(?!</c>).)*?<f([^>]*?)(?:/>|>([^<]*)</f>)' % ref, sheet_xml, re.S)
    if not m:
        return None
    attrs, text = m.group(1), m.group(2)
    if text:
        return html.unescape(text)
    si = re.search(r'si="(\d+)"', attrs).group(1)
    mm = re.search(r'<c r="([A-Z]+)(\d+)"[^>]*>(?:(?!</c>).)*?<f t="shared" ref="[^"]*" si="%s"[^>]*>([^<]*)</f>' % si, sheet_xml, re.S)
    c0, r0 = mm.group(1), int(mm.group(2))
    c1, r1 = re.fullmatch(r'([A-Z]+)(\d+)', ref).groups()
    n = lambda c: sum((ord(ch) - 64) * 26 ** i for i, ch in enumerate(reversed(c)))
    return _shift(html.unescape(mm.group(3)), int(r1) - r0, n(c1) - n(c0))


def book_sheet(tab):
    """Decoded XML of the worksheet with this tab name (sheet parts are not in tab order)."""
    with zipfile.ZipFile(BOOK) as z:
        wb = z.read('xl/workbook.xml').decode()
        rels = z.read('xl/_rels/workbook.xml.rels').decode()
        rid = re.search(r'<sheet name="%s" sheetId="\d+" r:id="([^"]+)"' % re.escape(html.escape(tab)), wb).group(1)
        target = re.search(r'Id="%s"[^>]*Target="([^"]+)"|Target="([^"]+)"[^>]*Id="%s"' % (rid, rid), rels)
        target = target.group(1) or target.group(2)
        return z.read('xl/' + target.lstrip('/').replace('xl/', '')).decode()


def named_cell(name):
    """(tab, cell) of a workbook-scoped defined name that points at one cell."""
    with zipfile.ZipFile(BOOK) as z:
        wb = z.read('xl/workbook.xml').decode()
    m = re.search(r'<definedName name="%s">\'?([^<!\']+)\'?!\$([A-Z]+)\$(\d+)</definedName>' % re.escape(name), wb)
    return m.group(1), m.group(2) + m.group(3)


class GasModelChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with contextlib.redirect_stdout(io.StringIO()):
            cls.sens = runpy.run_path(str(SENS))

    def test_all_media_against_independent_twin(self):
        for medium in ('AM001', 'AM002', 'UdG phosphate', 'AM003'):
            with self.subTest(medium=medium):
                src = re.sub(r'^media_sel\s*=\s*"[^"]*"',
                             f'media_sel = "{medium}"', TWIN.read_text(), flags=re.M)
                ns = {'__name__': 'test_twin', '__file__': str(TWIN)}
                exec(compile(src, str(TWIN), 'exec'), ns)
                got = self.sens['medium_chemistry'](dict(self.sens['BASE'], media=medium))
                expected = [ns[k] for k in ('pH_SID', 'pH_PT', 'pH_NT', 'pH_Cl', 'I_ionic', 'med_kappa0_rec')]
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
                               ('ed04', 'AM002', 9.0, k, pool, P, 'y')])
        self.assertTrue(math.isclose(t['tau_NH2Cl'], 40.0, rel_tol=1e-9))
        self.assertNotEqual(t['Cl_bound'], u['Cl_bound'])

    def test_calibration_formulas_match_the_twin(self):
        """The calibration rows are hand-written XML; pin their formula text to the twin's algebra."""
        km, ch, cal = book_sheet('Cal km'), book_sheet('Cal chloramine'), book_sheet('Calibrations')
        row = lambda t, h: '%s[[#This Row],[%s]]' % (t, h)
        k, c = (lambda h: row('CalKm', h)), (lambda h: row('CalChloramine', h))
        self.assertIn(html.escape('IF(OR(%s="",%s="",%s=""),"",IFERROR((%s/1000)/(Calibrations!n_e_fcn*Calibrations!F_const*(%s/10000)*%s)*100,""))' % (
            k('Limiting current (mA)'), k('Electrode area (cm²)'), k('Ferricyanide (mM)'), k('Limiting current (mA)'),
            k('Electrode area (cm²)'), k('Ferricyanide (mM)')), quote=False), km)
        self.assertIn(html.escape('IF(OR(%s="",%s=""),"",IFERROR(%s*(Calibrations!D_O2/%s)^Calibrations!km_exp,""))' % (
            k('k_m ferricyanide (computed, cm/s)'), k('D ferricyanide (m²/s)'), k('k_m ferricyanide (computed, cm/s)'),
            k('D ferricyanide (m²/s)')), quote=False), km)
        P, kk, pool, Pm = (c('Combined chlorine plateau (mg/L as Cl₂)'), c('Chloride turnover k (1/s)'),
                           c('Chloride pool C (mol/L)'), c('Max production P (mol/L/s)'))
        self.assertIn(html.escape(('IF(OR({P}="",{k}="",{pool}="",{Pm}=""),"",IF({P}/Calibrations!M_Cl2>={pool},'
                                   '"not invertible: plateau at or above the chloride pool",IFERROR(MAX({P}/Calibrations!M_Cl2/({k}*({pool}-{P}/Calibrations!M_Cl2)),'
                                   '{P}/Calibrations!M_Cl2/{Pm})/3600,"")))').format(P=P, k=kk, pool=pool, Pm=Pm), quote=False), ch)
        self.assertIn(html.escape('AVERAGEIFS(CalKm[k_m O₂ (computed, cm/s)],CalKm[Reactor],Reactor_sel,CalKm[Electrode],electrode_sel,'
                                  'CalKm[Include?],"y",CalKm[Stir rate (rpm)],stir_rpm_set,CalKm[Temp (°C)],">="&(temp_C-km_T_tol),'
                                  'CalKm[Temp (°C)],"<="&(temp_C+km_T_tol))', quote=False), cal)
        self.assertIn(html.escape('AVERAGEIFS(CalChloramine[Lifetime (computed, h)],CalChloramine[Reactor],Reactor_sel,'
                                  'CalChloramine[Medium],media_sel,CalChloramine[Include?],"y")', quote=False), cal)

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
        f = lambda ref: cell_formula(ch, ref)
        self.assertEqual(f('D332'), 'med_SID_rec+alk_add_M')    # recipe SID; D44 adds the nitrogen-source swap
        self.assertEqual(f('D44'), 'pH_SID_rec+IF(N_src_idx=1,0,pH_NT_rec)')
        self.assertEqual(f('D185'), 'med_I_rec+alk_add_M')
        self.assertIn('+alk_add_M*(lam_Na+lam_HCO3)/10)*kappa_fI', f('D180'))
        self.assertEqual(f('D317'), 'Summary!NaHCO3_add_gL')
        self.assertEqual(f('D318'), 'NaHCO3_add_gL/M_NaHCO3')
        tabs = re.findall(r'<sheet name="([^"]+)"', wb)          # local names are scoped by tab position
        for name, sid, ref in (('NaHCO3_add_gL', tabs.index('Summary'), 'Summary!$D$13'),
                               ('NaHCO3_add_gL', tabs.index('Chemistry'), 'Chemistry!$D$317'),
                               ('alk_add_M', tabs.index('Chemistry'), 'Chemistry!$D$318')):
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
        # With the sweep that frees CO2 from O2 duty, the pH ceiling binds and pH lands at the band ceiling
        # (carbon-trough bound switched off here; test_carbon_trough_bound covers it).
        n = self.twin(N2_sweep_set=base['N2_for_DO'], carbon_trough_min=-1e9)
        self.assertTrue(n['opt_binding'].startswith('pH CEILING ('))
        self.assertTrue(math.isclose(n['spg_int_opt'], n['spg_int_pH_opt'], rel_tol=1e-12))
        self.assertLessEqual(n['spg_int'], n['spg_int_pH'] + 1e-9)
        self.assertLess(n['spg_int_pH'] - n['spg_int'], 0.011)
        self.assertTrue(7.47 < n['pH_meas'] <= 7.5 + 1e-9, n['pH_meas'])
        # Any pulse override: the executable interval is converted back, so pH still holds the ceiling.
        for dur in (0.3, 1.0, 2.0):
            o = self.twin(N2_sweep_set=1.0, user_spg_dur=dur, carbon_trough_min=-1e9)
            self.assertTrue(7.47 < o['pH_meas'] <= 7.5 + 1e-9, (dur, o['pH_meas']))
        # Unreachable ceiling: no schedule rather than the carbon interval.
        u = self.twin(N2_sweep_set=20.0, pH_band_hi=6.0)
        self.assertTrue(u['ph_unreach'])
        self.assertTrue(math.isnan(u['spg_int_opt']))
        self.assertTrue(u['opt_binding'].startswith('pH CEILING UNREACHABLE'))
        # AM002 never reaches the ceiling: no bound, and the carbon bound stands with a sweep.
        mc = self.twin(media_sel='AM002', N2_sweep_set=1.0)
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
            if isinstance(t['spg_int_trough'], float):
                self.assertTrue(math.isclose(t['spg_int_trough'], m['spg_int_trough'], rel_tol=5e-3), (kw, t['spg_int_trough'], m['spg_int_trough']))
            self.assertTrue(math.isclose(t['spg_int'], m['spg_int_run'], rel_tol=5e-3), (kw, t['spg_int'], m['spg_int_run']))

    def test_ph_ceiling_formulas_in_workbook(self):
        with zipfile.ZipFile(BOOK) as z:
            mt = z.read('xl/worksheets/sheet6.xml').decode()
        f = lambda ref: cell_formula(mt, ref)
        self.assertEqual(f('D433'), 'IF(ISNUMBER(spg_int_pH),spg_int_pH*spg_dur_eq_opt/spg_dur_eq,"no pH bound")')
        self.assertIn('IF(OR(ph_unreach,trough_unreach),NA(),MIN(spg_int_carbon,IF(ISNUMBER(spg_int_trough_opt),spg_int_trough_opt,spg_int_carbon),IF(ISNUMBER(spg_int_DO),spg_int_DO,spg_int_max),IF(ISNUMBER(spg_int_pH_opt),spg_int_pH_opt,spg_int_carbon),IF(O2_sizing_phase=phase_name_2,IF(ISNUMBER(spg_int_H2safe_opt),spg_int_H2safe_opt,spg_int_carbon),spg_int_carbon))))', f('D91'))
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
        # Sized on Growth, the start-up uses the no-cathodic-loss bounds (ninth review), so it is never longer
        # than the Lag-sized headline; sized on Lag, it is exactly that headline.
        for kw in ({}, dict(kLa_meas=100.0), dict(N2_sweep_set=20.0, NaHCO3_add_gL=2.0), dict(vent_model_sel='Outflow only')):
            g = self.twin(**kw)
            l = self.twin(O2_phase_sel='Lag', **kw)
            if isinstance(g['spg_int_su_run'], float) and math.isnan(g['spg_int_su_run']):
                self.assertTrue(math.isnan(l['spg_int']), kw)
            else:
                self.assertLessEqual(g['spg_int_su_run'], l['spg_int'], (kw, g['su_binding'], l['opt_binding']))
                self.assertEqual(l['spg_int_su_run'], l['spg_int'], kw)
        hk = self.twin(kLa_meas=100.0)
        self.assertIn('hazard screen', hk['su_binding'])
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
        cal = html.unescape(book_sheet('Calibrations'))
        kn = html.unescape(book_sheet('Cal knallgas'))
        self.assertIn('knall_H2_basis*AVERAGEIFS(CalKnallgas[O₂ per H₂ (computed)],CalKnallgas[Organism],organism_sel,CalKnallgas[Include?],"y")', cal)
        self.assertIn('IFERROR(IF(CalKnallgas[[#This Row],[H2]]>0,CalKnallgas[[#This Row],[O2]]/CalKnallgas[[#This Row],[H2]],""),"")', kn)
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
        cal = html.unescape(book_sheet('Cal sinter'))
        bp = 'CalSinter[[#This Row],[Bubble point (kPa)]]'
        self.assertIn('"between or below the listed grades – not used"', cal)
        self.assertIn('AND((Calibrations!bp_const/%s)>=Calibrations!por_p5_lo,(Calibrations!bp_const/%s)<=Calibrations!por_p5_hi),5' % (bp, bp), cal)

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
        tab, ref = named_cell('cal_sinter')
        d89 = re.search(r'<c r="%s"[^>]*><f>([^<]*)</f>' % ref, book_sheet(tab)).group(1)
        self.assertIn('(bp_const/cal_bp)', d89)
        self.assertNotIn('AVERAGEIFS(', d89)

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

    def test_review7_fixes(self):
        # Exact periodic peak: the twin's closed form equals an independent RK4 periodic solve
        # (sensitivity model) in the reviewer's case where the quasi-steady form under-read the peak.
        t = self.twin(DO_opt=2.0, DO_toxic=2.3, user_spg_int=6.32)
        m = self.sens['model'](dict(self.sens['BASE'], DO_opt=2.0, DO_toxic=2.3))
        self.assertGreater(t['DO_peak_g'] * t['M_O2'], 2.33)
        b = self.twin()
        mb = self.sens['model'](self.sens['BASE'])
        self.assertTrue(math.isclose(b['DO_peak_g'] * b['M_O2'], mb['DO_peak_g'], rel_tol=1e-6))
        # Growth peroxide sees both sinks, and catalase returns half an O2 (findings 1-2).
        self.assertTrue(math.isclose(b['H2O2_ss'], b['r_H2O2'] / ((b['k_cat_cells'] + b['k_H2O2_anode']) * 3600), rel_tol=1e-12))
        r_tot = b['f_HOOH'] * b['O2_cathode_ORR']
        self.assertTrue(math.isclose(b['O2_H2O2_ret_g'] + 2 * b['O2_cat_ret_g'], r_tot, rel_tol=1e-12))

    def test_review8_fixes(self):
        # An accepted anodic-efficiency calibration is used, as Electrochemistry D26 does (finding 3).
        c = self.twin(cal_etaF_OER=0.8)
        self.assertEqual(c['etaF_OER'], 0.8)
        self.assertTrue(math.isclose(c['O2_net_gen'], c['I_app'] * 0.8 / (4 * c['F_const']) * 3600
                                     - c['O2_cathode_ORR'] + c['O2_cat_ret_g'], rel_tol=1e-12))
        # D66 integrates the first-order rise (finding 2): check against a direct Euler march.
        b = self.twin()
        V = b['V_charge'] / 1e6
        k = b['strip_avg'] / (V * b['O2_ceil_C'])
        C, t, h = 0.0, 0.0, 1e-5
        while C < b['O2_ceil_org']:
            C += h * (b['O2_excess'] / V - k * C); t += h
        self.assertTrue(math.isclose(b['t_O2_ceiling_strip'], t * 60, rel_tol=1e-3))
        # D80 never reports a non-crossing as a pass (finding 1).
        self.assertIn("not a pass", b['t_O2_ceiling_rem'])

    def test_review9_fixes(self):
        # The start-up schedule sizes on the no-cathodic-loss bounds (finding 1): its sources are at
        # least the lag ones, and in the reviewer's case (DO_opt 5 mg/L) the advertised start-up
        # interval clears the hazard screen on those bounds.
        for kw in ({}, {'DO_opt': 5.0}):
            t = self.twin(**kw)
            self.assertGreaterEqual(t['O2_src_su'], t['O2_src_l'])
            self.assertGreaterEqual(t['H2_src_su'], t['H2_src_l'])
            if 'hazard' in t['su_binding']:
                self.assertTrue(t['y_H2_end_su'] < t['H2_LFL'] * (1 + 1e-6)
                                or t['y_O2_end_su'] < t['O2_LOC_H2'] * t['LOC_margin'] * (1 + 1e-6))
        # Sized on Lag the start-up equals the headline schedule's lag sources.
        g = self.twin(O2_phase_sel='Lag')
        self.assertEqual(g['O2_src_su'], g['O2_src_l'])
        # The relaxation warning uses the organism ceiling (finding 3).
        r = self.twin(DO_toxic=2.0, N2_sweep_set=0.4)
        self.assertIn('2.0 mg/L inhibition ceiling', r['sched_regime'])
        # z_e_ORR is fixed, not swept (finding 2).
        self.assertNotIn('z_e_ORR', [row[0] for row in self.sens['SWEEP']])

    def test_review10_fixes(self):
        # The start-up pH grid decays the pool on the start-up gas flow (finding 1), which is the
        # lag flow when sized on Lag.
        for kw in ({}, {'N2_sweep_set': 2.0, 'NaHCO3_add_gL': 20.015}):
            t = self.twin(**kw)
            ratio = t['_Vg_e'] / (t['_V_L_CO2_e'] + t['_Vg_e']) / 3600 / t['n_hs_gas']
            self.assertTrue(math.isclose(t['_k_eff_l_e'], t['F_gap_su'] * ratio, rel_tol=1e-12))
        g = self.twin(O2_phase_sel='Lag')
        self.assertTrue(math.isclose(g['F_gap_su'], g['_F_gap_l_e'], rel_tol=1e-12))

    def test_review11_near_zero_vent_flow(self):
        # Outflow only at 25 C and 10 % power leaves a ~1e-20 mol/h residual vent flow; the helpers
        # and the exact peak must take their zero-flow limits, not collapse (twelfth review, finding 1).
        kw = dict(vent_model_sel='Outflow only', temp_C=25.0, led_intensity=10.0)
        t = self.twin(**kw)
        self.assertLess(t['hs_g']['x'], 1e-12)
        self.assertFalse(t['ph_unreach'])
        self.assertAlmostEqual(t['S_D21'], 0.57, places=9)
        self.assertGreater(t['pH_grid_C'][0], 30.0)
        m = self.sens['model'](dict(self.sens['BASE'], vent_model='Outflow only', T_C=25.0, intensity=10.0))
        self.assertTrue(math.isclose(m['spg_int_run'], 0.57, rel_tol=1e-9))
        self.assertTrue(math.isclose(t['DO_peak_g'] * t['M_O2'], m['DO_peak_g'], rel_tol=1e-6))
        # The series and the closed forms agree across the switch.
        for f, g in ((t['_phi'], lambda x: (1 - math.exp(-x)) / x), (t['_psi'], lambda x: (x - 1 + math.exp(-x)) / x ** 2)):
            xs = t['x_series']
            self.assertTrue(math.isclose(f(xs * 0.999999), g(xs * 1.000001), rel_tol=1e-6))

    def test_review13_fixes(self):
        # Every electrode the workbook lists (Electrochemistry A35:A38) runs in both companions.
        for e in ('Pt/Ti rod', 'MMO rod', 'MMO tube', 'Graphite rod'):
            t = self.twin(electrode_sel=e)
            m = self.sens['model'](dict(self.sens['BASE'], electrode=e))
            self.assertTrue(math.isclose(t['S_D21'], m['spg_int_run'], rel_tol=1e-9), e)
        # Every Summary note in column F longer than the column wraps (thirteenth review, finding 1).
        import html, zipfile
        z = zipfile.ZipFile(BOOK)
        st = z.read('xl/styles.xml').decode()
        xfs = re.findall(r'<xf [^>]*?(?:/>|>.*?</xf>)', re.search(r'<cellXfs count="\d+">(.*?)</cellXfs>', st, re.S).group(1), re.S)
        sh = z.read('xl/worksheets/sheet1.xml').decode()
        ss = [html.unescape(''.join(re.findall(r'<t[^>]*>([^<]*)</t>', si)))
              for si in re.findall(r'<si>(.*?)</si>', z.read('xl/sharedStrings.xml').decode(), re.S)]
        for m in re.finditer(r'<c r="F(\d+)"([^>]*?)(?:/>|>(.*?)</c>)', sh, re.S):
            a, body = m.group(2), m.group(3) or ''
            if 'inlineStr' in a:
                t = html.unescape(''.join(re.findall(r'<t[^>]*>([^<]*)</t>', body)))
            else:
                v = re.search(r'<v>([^<]*)</v>', body)
                if not v:
                    continue
                t = ss[int(v.group(1))] if 't="s"' in a else v.group(1)
            if len(t) > 100:
                sm = re.search(r's="(\d+)"', a)
                self.assertIn('wrapText="1"', xfs[int(sm.group(1))] if sm else '', 'Summary F' + m.group(1))
        # Long column-A labels beside an occupied column B wrap too (fourteenth review).
        occB = {int(m.group(1)) for m in re.finditer(r'<c r="B(\d+)"[^>]*?(?<!/)>(?:(?!</c>).)*?<(?:v|t)[^>]*>[^<]+', sh, re.S)}
        for m in re.finditer(r'<c r="A(\d+)"([^>]*?)>(.*?)</c>', sh, re.S):
            a, body = m.group(2), m.group(3)
            v = re.search(r'<v>([^<]*)</v>', body)
            t = (html.unescape(''.join(re.findall(r'<t[^>]*>([^<]*)</t>', body))) if 'inlineStr' in a else
                 (ss[int(v.group(1))] if 't="s"' in a else v.group(1)) if v else '')
            if int(m.group(1)) in occB and len(t) > 34:
                sm = re.search(r's="(\d+)"', a)
                self.assertIn('wrapText="1"', xfs[int(sm.group(1))] if sm else '', 'Summary A' + m.group(1))

    def test_nitrogen_source_and_media_options(self):
        base = self.twin()
        # Ammonium uptake acidifies: the end-of-run pH sits below the start; the swap is charge-neutral at the start.
        self.assertLess(base['pH_end_A'], base['pH_meas'])
        self.assertTrue(math.isclose(base['n_up_end'], 1.0 * 0.114 / 14.007, rel_tol=1e-12))
        self.assertGreater(base['pH_end_N'], base['pH_meas'])               # nitrate uptake consumes acid
        self.assertLess(abs(base['pH_end_U'] - base['pH_meas']), 1e-3)      # urea: no net acid
        for sel, key in (('Nitrate (KNO\u2083)', 'pH_end_N'), ('Urea', 'pH_end_U')):
            t = self.twin(N_source_sel=sel)
            self.assertLess(abs(t['pH_meas'] - base['pH_meas']), 2e-3, sel)  # same start pH
            self.assertTrue(math.isclose(t['pH_end'], base[key], rel_tol=1e-3), sel)   # CO2 storage shifts slightly with the start pH
            self.assertEqual(t['pH_NT'], 0.0)
        # The NaHCO3 that holds the band floor through the run lands the end-of-run pH on the floor.
        t = self.twin(NaHCO3_add_gL=base['alk_run_gL'])
        self.assertLess(abs(t['pH_end_A'] - 6.5), 0.02, t['pH_end_A'])
        # No biomass: no uptake, end equals start.
        z = self.twin(X_end_gL=0.0)
        self.assertLess(abs(z['pH_end'] - z['pH_meas']), 1e-9 + 2e-3)
        # Too much biomass for the nitrogen: uptake capped and flagged.
        big = self.twin(X_end_gL=10.0)
        self.assertEqual(big['n_up_end'], big['pH_NT_rec'])
        self.assertTrue(big['N_limit_chk'].startswith('NITROGEN RUNS OUT'))
        # An unlisted nitrogen source returns no pH, as the selectors do elsewhere.
        bad = self.twin(N_source_sel='Ammonia')
        self.assertTrue(math.isnan(bad['pH_SID']))

    def test_carbon_trough_bound(self):
        base = self.twin()
        self.assertGreater(base['spg_int_trough'], base['spg_int'])          # inert at baseline
        q = base['N2_for_DO']
        n = self.twin(N2_sweep_set=q)
        # With the N2 sweep the 2x Km trough binds before the pH ceiling, and the pool start then sits at the margin.
        self.assertTrue(n['opt_binding'].startswith('CARBON TROUGH ('), n['opt_binding'])
        self.assertTrue(math.isclose(n['spg_int_opt'], n['spg_int_trough_opt'], rel_tol=1e-12))
        m = self.sens['model'](dict(self.sens['BASE'], N2_sweep=q))
        self.assertTrue(math.isclose(n['spg_int'], m['spg_int_run'], rel_tol=5e-3), (n['spg_int'], m['spg_int_run']))
        self.assertTrue(m['opt_binding'].startswith('CARBON TROUGH ('))
        # An impossible margin returns no schedule rather than a starving one.
        u = self.twin(carbon_trough_min=1e6)
        self.assertTrue(u['trough_unreach'])
        self.assertTrue(math.isnan(u['spg_int_opt']))

    def test_pulse_rule_and_startup_current(self):
        base = self.twin()
        s = self.twin(pulse_rule_sel='Shortest reliable pulse')
        self.assertEqual(s['spg_dur_opt'], s['pulse_floor'])
        self.assertLess(s['spg_dur_opt'], base['spg_dur_opt'])
        self.assertTrue(math.isnan(self.twin(pulse_rule_sel='Longest')['spg_dur_opt']))
        # Start-up current: below the set current while the lag DO target is unreachable, and the net lag O2
        # at that current is what the surface kLa in use holds at the target.
        self.assertLess(base['kLa_margin_l'], 1)
        self.assertLess(base['I_su'], base['I_app'])
        net = base['rO2_per_A'] * base['I_su'] - base['O2_ORR_lag'] + base['O2_H2O2_lag_adj']
        self.assertTrue(math.isclose(net, base['kLa_margin_l'] * base['O2_net_lag'], rel_tol=1e-12))
        self.assertTrue(base['power_su_basis'].startswith('EXTRAPOLATED') and 'DATA GAP' in base['power_su_basis'])
        hi = self.twin(temp_C=20.0, led_intensity=3.0)
        if hi['kLa_margin_l'] >= 1:
            self.assertTrue(hi['power_su_basis'].startswith('not needed'))

    def test_summary_layout_and_formats(self):
        """Every Summary value row has a name, every check sits under Checks, and only the Key's formats are used."""
        import html
        with zipfile.ZipFile(BOOK) as z:
            wb = z.read('xl/workbook.xml').decode()
            sh = z.read('xl/worksheets/sheet1.xml').decode()
            st = z.read('xl/styles.xml').decode()
            parts = [z.read(n).decode() for n in z.namelist() if n.startswith('xl/worksheets/sheet')]
        summary_id = re.findall(r'<sheet name="([^"]+)"', wb).index('Summary')    # local names are scoped by tab position
        names = {m.group(1): int(m.group(2)) for m in
                 re.finditer(r'<definedName name="([^"]+)" localSheetId="%d">Summary!\$D\$(\d+)</definedName>' % summary_id, wb)}
        checks_row = min(r for n, r in names.items() if n.startswith('chk_'))
        self.assertTrue(all(r >= checks_row for n, r in names.items() if n.startswith('chk_')))
        self.assertTrue(all(r < checks_row for n, r in names.items() if n.startswith('res_')))
        # no colour scales, data bars or decorative outlines; traffic lights use only the Key's three dxfs and DATA GAP
        for x in parts:
            self.assertNotIn('colorScale', x)
            self.assertNotIn('dataBar', x)
        borders = re.findall(r'<border\b.*?</border>|<border/>', re.search(r'<borders.*?</borders>', st, re.S).group(0), re.S)
        xfs = re.findall(r'<xf [^>]*?(?:/>|>.*?</xf>)', re.search(r'<cellXfs count="\d+">(.*?)</cellXfs>', st, re.S).group(1), re.S)
        used = {int(m.group(1)) for x in parts for m in re.finditer(r'<c r="[A-Z]+\d+"[^>]*\ss="(\d+)"', x)}
        for i in used:
            b = int(re.search(r'borderId="(\d+)"', xfs[i]).group(1))
            self.assertNotIn('style="medium"', borders[b], i)
        dxfs = re.findall(r'<dxf>.*?</dxf>', st, re.S)
        for x in parts:
            for d in re.findall(r'dxfId="(\d+)"', x):
                self.assertTrue(re.search(r'FF006100|FF9C5700|FF9C0006|theme="0"', dxfs[int(d)]), dxfs[int(d)])

    def test_measured_hydrogen_utilisation_changes_consumption_and_residual_gas(self):
        baseline = self.twin()
        half = self.twin(H2_util_meas=0.5)
        for key in ('H2_cons', 'O2_cons', 'CO2_cons'):
            self.assertAlmostEqual(half[key], baseline[key] / 2)
        self.assertGreater(half['O2_excess'], baseline['O2_excess'])
        self.assertGreater(half['H2_src_g'], baseline['H2_src_g'])
        reduced = self.sens['model'](dict(self.sens['BASE'], H2_util=0.5))
        for key in ('spg_int_opt', 'DO_ss', 'pH_meas'):
            self.assertTrue(math.isclose(reduced[key], half[key], rel_tol=5e-5), key)
        with zipfile.ZipFile(BOOK) as z:
            sh = z.read('xl/worksheets/sheet5.xml').decode()
        self.assertEqual(cell_formula(sh, 'D13'), 'MAX(0,rH2_gen-H2_HOR_b)*H2_util')
        self.assertIn('ISBLANK(H2_util_meas)', cell_formula(sh, 'D130'))

    def test_infeasible_candidate_is_not_presented_as_an_optimum(self):
        n = self.twin()
        self.assertLess(n['pH_end'], n['pH_band_lo'])
        self.assertEqual(n['res_qualification'],
                         'NOT FEASIBLE for the stated pH/DO targets; candidate only')

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
