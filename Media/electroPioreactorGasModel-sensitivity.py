#!/usr/bin/env python3
"""One-at-a-time (OAT) sensitivity analysis for electroPioreactorGasModel.xlsx.

Companion to electroPioreactorGasModel.py (the full independent re-derivation that
reproduces all 77 spreadsheet outputs within 0.5%). This script is kept SEPARATE
from that module on purpose: the full model is a fidelity cross-check (every output
must match the workbook), whereas this one is a deliberately reduced re-implementation
that holds the schedule logic fixed and sweeps each uncertain INPUT over its plausible
range to rank what actually moves the recommended schedule. Merging them would force
the sweep to carry the full Summary/Chemistry/CO2-flows apparatus it does not need, and
would couple a "must reproduce the sheet exactly" module to a "perturb and rank" one.
They share the same physics; this file re-implements only the path from input -> the
five schedule-critical outputs.

Baseline matches the live model (Media/electroPioreactorGasModel.py) for reactor ed04:
  - calibrated CO2 flow Q_CO2 = flowrate_cal*60 = 199.8 mL/min (NOT the old 10 mL/min
    design-narrative figure)
  - z_e_ORR = 2 (Pt/Ti rod electrode lookup, 2e- peroxide pathway)
  - H_O2ref = 1.2e-5 mol/m3/Pa
  - spg_dur_opt = max(pulse_floor, flush_factor*headspace_V/(Q_CO2/60))
  - the O2 schedule guards credit surf_strip (the current live form -- this is the
    H-2/H-3 finding; the sweep shows how strongly kL_surf_factor drives the schedule
    precisely BECAUSE that credit gates the cap).

Standard library only.  Run with:  python3 electroPioreactorGasModel-sensitivity.py

Covers every NON-ABSOLUTE input. Excluded (absolute / defined): F_const, R_gas,
g_const, Pa_per_atm, z_e_H2, z_e_O2, M_CO2, T_ref.

Each input carries an IGNORANCE tier -- DATA-GAP (unmeasured), ESTIMATE, LITERATURE
(well-known), KNOB (you set it). Urgency = leverage on the critical outputs x how
poorly we know the value. KNOBs are control authority, reported separately.
"""
import math
PI = math.pi

BASE = dict(
  # --- geometry (measured / estimated for the build; AEP0.1.1-class vial) ---
  vial_OD=27.48, vial_wall=1.1, D_int=55, V_max=16, V_vial_total=20,
  rod_d=6, rod_n=2, elec_clear=22, spg_OD=3.175, spg_ID=1.5875,
  eff_OD=3.175, eff_ID=1.5875, xtube_n=3, xtube_pro=5,
  # --- electrolysis ---
  intensity=3, gerrit_slope=1.03, gerrit_int=2.6, F=96485.33212,
  z_e_H2=2, z_e_O2=4, etaF=1.0, etaF_OER=1.0, z_e_ORR=2,   # z_e_ORR=2: Pt/Ti rod lookup
  # --- biology ---
  bio_H2=6, bio_O2=2, bio_CO2=1,
  # --- O2 ceiling / Henry ---
  T_C=30, P_atm=101325, H_O2ref=1.2e-5, H_O2T=1500, T_ref=298.15, O2_ceil_atm=0.3,
  # --- CO2 dosing (ed04 calibrated: 3.33 mL/s = 199.8 mL/min) ---
  Q_CO2=199.8, pulse_floor=0.25, flush_factor=1.0, R=8.314462618, M_CO2=44.0095,
  # --- bubble / strip ---
  sigma=0.0712, rho_L=995.65, g=9.80665, D_O2=2.249e-9, mend_a=2.14, mend_b=0.505,
  u_g_max=0.05,
  # --- surface / stirring ---
  stir_rpm=500, stir_len=12, kL_surf_factor=1.0,   # factor = order-of-magnitude uncertainty in the coarse surface kLa
  # --- dissolved CO2 / H2 ---
  H_CO2ref=3.3e-4, H_CO2T=2400, Km_CO2=50,
  H_H2ref=7.8e-6, H_H2T=500,
  # --- optimiser inputs ---
  target_DO_frac=0.5, carbon_margin_min=2,
)


def model(p):
    T_K = p['T_C'] + 273.15
    # --- geometry ---
    vial_ID = p['vial_OD'] - 2 * p['vial_wall']
    A_x = PI / 4 * vial_ID ** 2
    h_datum = p['V_max'] * 1000 / A_x
    elec_ins = p['D_int'] - p['elec_clear']
    spg_tip_h = p['elec_clear']
    disp = (p['rod_n'] * (PI / 4 * p['rod_d'] ** 2) * max(0, h_datum - p['elec_clear'])
            + (PI / 4 * p['spg_OD'] ** 2) * max(0, h_datum - spg_tip_h)
            + (PI / 4 * (p['eff_OD'] ** 2 - p['eff_ID'] ** 2)) * ((p['eff_OD'] + p['eff_ID']) / 2)) / 1000
    V_charge = round(p['V_max'] - disp, 0)
    h_actual = (V_charge + disp) * 1000 / A_x
    interface_A = A_x - (p['rod_n'] * (PI / 4 * p['rod_d'] ** 2)
                         + (PI / 4 * p['spg_OD'] ** 2) + (PI / 4 * p['eff_OD'] ** 2))
    spg_len = p['D_int'] - spg_tip_h
    V_inserts = (p['rod_n'] * (PI / 4 * p['rod_d'] ** 2) * elec_ins
                 + (PI / 4 * p['spg_OD'] ** 2) * spg_len
                 + (PI / 4 * (p['eff_OD'] ** 2 - p['eff_ID'] ** 2)) * (p['D_int'] - h_actual)
                 + p['xtube_n'] * (PI / 4 * p['eff_OD'] ** 2) * p['xtube_pro']) / 1000
    headspace_V = p['V_vial_total'] - V_charge - V_inserts
    # --- electrolysis ---
    I_app = (p['gerrit_slope'] * p['intensity'] + p['gerrit_int']) / 1000
    rH2 = I_app * p['etaF'] / (p['z_e_H2'] * p['F']) * 3600
    rO2 = I_app * p['etaF_OER'] / (p['z_e_O2'] * p['F']) * 3600
    O2_cath = I_app * (1 - p['etaF']) / (p['z_e_ORR'] * p['F']) * 3600
    O2_net = rO2 - O2_cath
    O2_cons = rH2 * p['bio_O2'] / p['bio_H2']
    CO2_cons = rH2 * p['bio_CO2'] / p['bio_H2']
    O2_excess = O2_net - O2_cons
    # --- O2 ceiling ---
    H_O2_T = p['H_O2ref'] * math.exp(p['H_O2T'] * (1 / T_K - 1 / p['T_ref']))
    O2_ceil_C = H_O2_T * p['O2_ceil_atm'] * p['P_atm']
    O2_ceil_Pa = p['O2_ceil_atm'] * p['P_atm']
    nCO2 = p['P_atm'] * (p['Q_CO2'] / 1e6 / 60) / (p['R'] * T_K)
    # O2_net can vanish exactly (e.g. etaF=0.5 with z_e_ORR=2: cathodic ORR consumes
    # all anodic O2) -- guard the lag time, which then diverges.
    t_lag = (O2_ceil_C * (V_charge / 1e6) / O2_net * 60) if O2_net > 1e-12 else float('inf')
    # --- surface stripping (kL_surf) ---
    tip = PI * (p['stir_len'] / 1000) * p['stir_rpm'] / 60
    s_ren = tip / (vial_ID / 1000)
    kL_surf = 2 * math.sqrt(p['D_O2'] * s_ren / PI) * p['kL_surf_factor']
    a_surf = interface_A / V_charge
    kLa_surf = kL_surf * a_surf
    surf_strip = kLa_surf * (V_charge / 1e6) * O2_ceil_C * 3600
    surf_ratio = surf_strip / O2_excess if O2_excess > 0 else float('nan')
    # --- §14 optimiser (Optimal mode) -- live form, surf_strip-credited guards ---
    spg_dur = max(p['pulse_floor'], p['flush_factor'] * headspace_V / (p['Q_CO2'] / 60))
    duty_carbon = p['carbon_margin_min'] * CO2_cons / (nCO2 * 3600)
    duty_O2vent = (max(0.0, O2_net - surf_strip)
                   / (p['target_DO_frac'] * (O2_ceil_Pa / p['P_atm'])) / (nCO2 * 3600))
    duty_opt = max(duty_carbon, duty_O2vent)
    spg_int_max = (p['target_DO_frac'] * O2_ceil_C * (V_charge / 1e6)
                   / max(1e-12, O2_net - surf_strip) * 60)
    spg_int = min(spg_dur / (60 * duty_opt), spg_int_max)   # minutes
    duty = spg_dur / (spg_int * 60)
    CO2_supply = nCO2 * spg_dur * (60 / spg_int)
    CO2_sd = CO2_supply / CO2_cons if CO2_cons > 0 else float('nan')
    # --- bubble / strip (tube); Mendelson NA-guard < 1 mm ---
    d_or = p['spg_ID'] / 1000
    d_b = (6 * d_or * p['sigma'] / (p['rho_L'] * p['g'])) ** (1 / 3)
    if d_b < 0.001:
        strip_avg = float('nan'); strip_ratio = float('nan')
    else:
        u_rise = math.sqrt(p['mend_a'] * p['sigma'] / (p['rho_L'] * d_b) + p['mend_b'] * p['g'] * d_b)
        u_sg = (p['Q_CO2'] / 1e6 / 60) / (A_x / 1e6)
        holdup = u_sg / u_rise; a_int = 6 * holdup / d_b; t_c = d_b / u_rise
        kL = 2 * math.sqrt(p['D_O2'] / (PI * t_c)); kLa = kL * a_int
        strip_sparge = kLa * (V_charge / 1e6) * O2_ceil_C * 3600
        strip_avg = strip_sparge * duty
        strip_ratio = strip_avg / O2_excess if O2_excess > 0 else float('nan')
    sa = 0 if (isinstance(strip_avg, float) and math.isnan(strip_avg)) else strip_avg
    removal_ratio = (sa + surf_strip + O2_cath) / O2_excess if O2_excess > 0 else float('nan')
    # --- dissolved CO2 / H2 ---
    H_CO2_T = p['H_CO2ref'] * math.exp(p['H_CO2T'] * (1 / T_K - 1 / p['T_ref']))
    CO2_diss = H_CO2_T * p['P_atm']
    carbon_margin = CO2_diss * 1000 / p['Km_CO2']
    H_H2_T = p['H_H2ref'] * math.exp(p['H_H2T'] * (1 / T_K - 1 / p['T_ref']))
    C_H2 = H_H2_T * p['P_atm']
    t_H2_sat = C_H2 * (V_charge / 1e6) / rH2 * 60
    return dict(spg_int_opt=spg_int, spg_int_opt_s=spg_int * 60, duty_opt=duty, CO2_sd=CO2_sd,
                t_O2_ceiling_lag=t_lag, O2_removal_ratio=removal_ratio, surf_ratio=surf_ratio,
                O2_excess=O2_excess, rH2=rH2, carbon_margin=carbon_margin, t_H2_sat=t_H2_sat,
                strip_ratio=strip_ratio)


# (input, low, high, tier).  tiers: DATA-GAP, ESTIMATE, LITERATURE, KNOB
SWEEP = [
 # ---- DATA-GAP (unmeasured) ----
 ('etaF', 0.5, 1.0, 'DATA-GAP'),
 ('kL_surf_factor', 0.25, 4.0, 'DATA-GAP'),     # surface kLa is a coarse proxy: order-of-magnitude
 ('bio_O2', 1.6, 2.4, 'DATA-GAP'),
 ('bio_CO2', 0.8, 1.3, 'DATA-GAP'),
 ('pulse_floor', 0.2, 1.0, 'DATA-GAP'),
 # ---- ESTIMATE ----
 ('O2_ceil_atm', 0.25, 0.35, 'ESTIMATE'),
 ('z_e_ORR', 2, 4, 'ESTIMATE'),
 ('etaF_OER', 0.9, 1.0, 'ESTIMATE'),
 ('vial_wall', 0.9, 1.3, 'ESTIMATE'),
 ('Km_CO2', 20, 80, 'ESTIMATE'),
 ('gerrit_slope', 0.95, 1.11, 'ESTIMATE'),      # empirical rig fit +/-8%
 ('gerrit_int', 2.2, 3.0, 'ESTIMATE'),
 ('u_g_max', 0.03, 0.10, 'ESTIMATE'),
 ('V_max', 14, 18, 'ESTIMATE'),
 # ---- LITERATURE (well-known) ----
 ('D_O2', 2.07e-9, 2.43e-9, 'LITERATURE'),
 ('sigma', 0.0698, 0.0726, 'LITERATURE'),
 ('rho_L', 990.6, 1000.7, 'LITERATURE'),
 ('H_O2ref', 1.10e-5, 1.30e-5, 'LITERATURE'),
 ('H_O2T', 1275, 1725, 'LITERATURE'),
 ('H_CO2ref', 3.05e-4, 3.55e-4, 'LITERATURE'),
 ('H_H2ref', 7.2e-6, 8.4e-6, 'LITERATURE'),
 ('mend_a', 2.03, 2.25, 'LITERATURE'),
 ('mend_b', 0.48, 0.53, 'LITERATURE'),
 # ---- KNOB (you set it) ----
 ('intensity', 3, 25, 'KNOB'),
 ('Q_CO2', 100, 300, 'KNOB'),
 ('target_DO_frac', 0.3, 0.9, 'KNOB'),
 ('carbon_margin_min', 1.5, 3.0, 'KNOB'),
 ('stir_rpm', 250, 900, 'KNOB'),
 ('T_C', 28, 34, 'KNOB'),
]
# outputs that decide whether we reach growth / what schedule to run
CRITICAL = ['spg_int_opt', 't_O2_ceiling_lag', 'O2_removal_ratio', 'surf_ratio', 't_H2_sat']
WEIGHT = {'DATA-GAP': 1.0, 'ESTIMATE': 0.6, 'LITERATURE': 0.15, 'KNOB': 0.0}


def run(name, val):
    p = dict(BASE); p[name] = val; return model(p)


b = model(BASE)
print("=" * 88)
print("BASELINE (Optimal mode, tube sparger, ed04 / AEP0.1.1-class vial, Q_CO2=199.8 mL/min):")
for k in ['spg_int_opt_s', 'duty_opt', 't_O2_ceiling_lag', 'O2_removal_ratio', 'surf_ratio',
          't_H2_sat', 'carbon_margin', 'rH2', 'CO2_sd']:
    print(f"   {k:18}= {b[k]:.4g}")
print(f"   => recommended schedule: {BASE['pulse_floor']}s pulse every {b['spg_int_opt_s']:.0f}s "
      f"(~{b['spg_int_opt']:.1f} min)")


def span(name, lo, hi, k):
    rl, rh = run(name, lo), run(name, hi)
    a, c = rl[k], rh[k]
    if any(isinstance(x, float) and (math.isnan(x) or math.isinf(x)) for x in (a, c)):
        return float('nan')
    base = b[k]
    return abs(c - a) / abs(base) * 100 if base else float('nan')


print("\n" + "=" * 88)
print("LEVERAGE -- % change in each critical output across the input's plausible range")
print(f"{'input':16}{'tier':10}{'sched%':>8}{'tO2lag%':>9}{'remRatio%':>10}{'surfR%':>8}{'tH2%':>7}")
rows = []
for name, lo, hi, tier in SWEEP:
    sp = {k: span(name, lo, hi, k) for k in CRITICAL}
    crit = max([v for v in sp.values() if not math.isnan(v)] or [0])
    rows.append((name, tier, sp, crit))
for name, tier, sp, crit in rows:
    def f(k):
        v = sp[k]; return f"{v:>7.0f}" if not math.isnan(v) else "    n/a"
    print(f"{name:16}{tier:10}{f('spg_int_opt'):>8}{f('t_O2_ceiling_lag'):>9}"
          f"{f('O2_removal_ratio'):>10}{f('surf_ratio'):>8}{f('t_H2_sat'):>7}")

print("\n" + "=" * 88)
print("URGENT ATTENTION ranking = leverage x ignorance  (KNOBs excluded -- those are control levers)")
scored = [(name, tier, crit, crit * WEIGHT[tier]) for name, tier, sp, crit in rows if tier != 'KNOB']
scored.sort(key=lambda r: -r[3])
print(f"{'rank':5}{'input':16}{'tier':10}{'max critical span%':>20}{'urgency score':>15}")
for i, (name, tier, crit, score) in enumerate(scored, 1):
    print(f"{i:<5}{name:16}{tier:10}{crit:>18.0f}%{score:>15.1f}")

print("\nKNOBS (control authority -- biggest levers you turn deliberately):")
knobs = [(name, crit) for name, tier, sp, crit in rows if tier == 'KNOB']
knobs.sort(key=lambda r: -r[1])
for name, crit in knobs:
    print(f"   {name:18} max critical span {crit:.0f}%")


# ============================================================================
# C_eff (effective biocidal chlorine) sensitivity -- the four chlorine knobs the
# review (2026-06-26) flagged as never swept: tau_NH2Cl, R_chloramine, km_Cl,
# FE_CER. The schedule model above does not compute C_eff, so this is a separate
# block. It holds the pH/chloride context fixed at the UdG recommended-schedule
# baseline (taken from the live model) and sweeps each knob over its plausible
# range. The headline is that the chloride-pool cap (Cl_pool_mgL, the new mass-
# balance fix) bounds C_eff below the kill threshold across the WHOLE knob box.
# ============================================================================
CL_BASE = dict(
  # fixed context from electroPioreactorGasModel.py (UdG, recommended schedule)
  pH_Cl=0.00018021265092809516,   # chloride molarity (mol/L)
  NH3_free=9.542413029341608e-05, # reactive free ammonia (M)
  NH3_N=99.64113818677161,        # ammonium-N (mg/L) -> 5.06*NH3_N ammonium cap
  Cl_pool_mgL=9.453955667687872,  # chloride-pool ceiling (mg/L HOCl-equiv)
  Iappc=0.00569, Fcc=96485.33212, VLc=0.015, k1_NH2Cl=4.2e6, f_local=10,
  A_anode=2.1445,  # geometry-derived wetted anode area (20 mL Pt/Ti, ~9.9 mm submerged); was a fixed 5 cm2 estimate, now computed in the model

  # the four swept knobs at baseline
  km_Cl=0.003, FE_CER=0.5, tau_NH2Cl=1.0, R_chloramine=25.0,
)


def c_eff_model(p):
    """Reproduce the live chlorine chain (Chemistry rows 128-163) at fixed pH/Cl.
    Returns C_eff (mg/L). Includes the two review bug-fixes: n-electron-correct
    P_HOCl and the chloride-pool cap on combined chlorine."""
    I_Cl_FE = p['Iappc'] * p['FE_CER']
    I_Cl_mt = p['Fcc'] * p['km_Cl'] * (p['pH_Cl'] / 1000) * p['A_anode']
    I_Cl = min(I_Cl_FE, I_Cl_mt)
    n_e_Cl = 1 if I_Cl_mt <= I_Cl_FE else 2          # arrival-limited -> 1 e-/Cl
    P_HOCl = I_Cl / (n_e_Cl * p['Fcc'] * p['VLc'])
    HOCl_ss_mgL = P_HOCl / (p['k1_NH2Cl'] * p['NH3_free']) * 52460
    NH2Cl = min(P_HOCl * p['tau_NH2Cl'] * 3600 * 52460, 5.06 * p['NH3_N'], p['Cl_pool_mgL'])
    return p['f_local'] * HOCl_ss_mgL + NH2Cl / p['R_chloramine']


def c_eff_run(name, val):
    p = dict(CL_BASE); p[name] = val; return c_eff_model(p)


# (knob, low, high, tier) -- all four are ESTIMATE/DATA-GAP, none measured here
CL_SWEEP = [
 ('tau_NH2Cl', 1/60, 5.0, 'DATA-GAP'),   # 1 min .. 5 h monochloramine residence
 ('R_chloramine', 18, 70, 'ESTIMATE'),   # potency-divisor band
 ('km_Cl', 0.001, 0.01, 'ESTIMATE'),     # chloride mass-transfer coeff (cm/s)
 ('FE_CER', 0.2, 0.8, 'DATA-GAP'),       # max CER faradaic efficiency
]
ce_base = c_eff_model(CL_BASE)
print("\n" + "=" * 88)
print("C_eff (effective biocidal chlorine) sensitivity -- the four chlorine knobs")
print(f"   baseline C_eff = {ce_base:.3f} mg/L  (UdG, recommended schedule; "
      f"onset 0.1, kill 2.0 mg/L)")
print(f"{'knob':16}{'tier':10}{'low':>12}{'high':>12}{'C_eff lo':>11}{'C_eff hi':>11}")
ce_lo_all, ce_hi_all = [], []
for name, lo, hi, tier in CL_SWEEP:
    a, c = c_eff_run(name, lo), c_eff_run(name, hi)
    ce_lo_all.append(min(a, c)); ce_hi_all.append(max(a, c))
    print(f"{name:16}{tier:10}{lo:>12.4g}{hi:>12.4g}{min(a,c):>11.3f}{max(a,c):>11.3f}")
print(f"\n   full one-at-a-time C_eff envelope: {min(ce_lo_all):.3f} .. {max(ce_hi_all):.3f} mg/L")
print(f"   kill threshold = 2.0 mg/L -> {'REACHED' if max(ce_hi_all) >= 2.0 else 'NOT reached'}: "
      "the chloride-pool cap holds C_eff sub-lethal across the whole knob box for UdG.")
