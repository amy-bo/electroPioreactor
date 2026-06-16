#!/usr/bin/env python3
"""One-at-a-time (OAT) sensitivity analysis for electroPioreactorGasModel.xlsx.

Re-implements the model's formula chain in plain Python so the analysis is
reviewable and reproducible without Excel. Active build = AEP0.1.1 (20 mL).
For each UNCERTAIN input (a thing you'd measure), it recomputes the model at a
plausible low and high and reports the span induced in the decision outputs.
Largest span = highest-value measurement to pin down. Knobs (settings you choose,
not measure) are reported separately as control authority.
"""
import math
PI=math.pi

BASE=dict(
  vial_OD=27.48, vial_wall=1.1, D_int=55, V_max=16, V_vial_total=24,
  rod_d=6, rod_n=2, elec_clear=22, spg_OD=3.175, spg_ID=1.5875,
  eff_OD=3.175, eff_ID=1.5875,
  intensity=3, gerrit_slope=1.03, gerrit_int=2.6, F=96485.33212,
  z_e_H2=2, z_e_O2=4, etaF=1.0, etaF_OER=1.0, z_e_ORR=4,
  bio_H2=6, bio_O2=2, bio_CO2=1,
  T_C=30, P_atm=101325, Pa_per_atm=101325,
  H_O2ref=1.3e-5, H_O2T=1500, T_ref=298.15, O2_ceil_atm=0.3,
  Q_CO2=10, spg_dur=1, spg_int=1, R=8.314462618, M_CO2=44.0095,
  sigma=0.0712, rho_L=995.65, g=9.80665, D_O2=2.4e-9,
  d_orifice=0.000205, mend_a=2.14, mend_b=0.505,
)

def model(p):
    vial_ID=p['vial_OD']-2*p['vial_wall']
    A_x=PI/4*vial_ID**2
    h_datum=p['V_max']*1000/A_x
    elec_ins=p['D_int']-p['elec_clear']; spg_tip_h=p['elec_clear']
    elec_sub=max(0,h_datum-p['elec_clear'])
    disp=(p['rod_n']*(PI/4*p['rod_d']**2)*elec_sub
          +(PI/4*p['spg_OD']**2)*max(0,h_datum-spg_tip_h)
          +(PI/4*(p['eff_OD']**2-p['eff_ID']**2))*((p['eff_OD']+p['eff_ID'])/2))/1000
    V_charge=round(p['V_max']-disp,0)
    I_app=(p['gerrit_slope']*p['intensity']+p['gerrit_int'])/1000
    rH2=I_app*p['etaF']/(p['z_e_H2']*p['F'])*3600
    rO2_gross=I_app*p['etaF_OER']/(p['z_e_O2']*p['F'])*3600
    O2_cath=I_app*(1-p['etaF'])/(p['z_e_ORR']*p['F'])*3600
    O2_net=rO2_gross-O2_cath
    O2_cons=rH2*p['bio_O2']/p['bio_H2']; CO2_cons=rH2*p['bio_CO2']/p['bio_H2']
    O2_excess=O2_net-O2_cons
    T_K=p['T_C']+273.15
    H_O2_T=p['H_O2ref']*math.exp(p['H_O2T']*(1/T_K-1/p['T_ref']))
    O2_ceil_C=H_O2_T*p['O2_ceil_atm']*p['Pa_per_atm']
    nCO2=p['P_atm']*(p['Q_CO2']/1e6/60)/(p['R']*T_K)
    CO2_supply=nCO2*p['spg_dur']*(60/p['spg_int'])
    CO2_sd=CO2_supply/CO2_cons if CO2_cons>0 else float('nan')
    duty=p['spg_dur']/(p['spg_int']*60)
    d_b=(6*p['d_orifice']*p['sigma']/(p['rho_L']*p['g']))**(1/3)
    u_rise=math.sqrt(p['mend_a']*p['sigma']/(p['rho_L']*d_b)+p['mend_b']*p['g']*d_b)
    u_sg=(p['Q_CO2']/1e6/60)/(A_x/1e6)
    holdup=u_sg/u_rise; a_int=6*holdup/d_b; t_c=d_b/u_rise
    kL=2*math.sqrt(p['D_O2']/(PI*t_c)); kLa=kL*a_int
    strip_sparge=kLa*(V_charge/1e6)*O2_ceil_C*3600
    strip_ratio=(strip_sparge*duty)/O2_excess if O2_excess>0 else float('nan')
    return dict(rH2_mol_h=rH2, O2_excess=O2_excess, strip_ratio=strip_ratio,
                CO2_sd=CO2_sd, d_bubble_mm=d_b*1000)

def run(name,val):
    p=dict(BASE); p[name]=val; return model(p)

# UNCERTAIN INPUTS (measurements): (low, high, rationale)
MEAS={
 'etaF':       (0.5, 1.0,  'cathodic H2 faradaic efficiency; 1.0 optimistic, true value unmeasured'),
 'bio_O2':     (1.5, 2.5,  'O2:H2 consumption ratio (base 2 of 6:2:1)'),
 'bio_CO2':    (0.7, 1.3,  'CO2:H2 consumption ratio (base 1 of 6:2:1)'),
 'D_O2':       (1.8e-9,3.0e-9,'O2 diffusivity literature spread'),
 'O2_ceil_atm':(0.2, 0.4,  'O2 growth-inhibition ceiling'),
 'd_orifice':  (160e-6,250e-6,'sinter P0 pore size range 160-250 um'),
 'vial_wall':  (0.8, 1.4,  'estimated borosilicate wall thickness'),
}
KNOBS={
 'intensity':(3,25,'LED setpoint, validated range'),
 'Q_CO2':    (5,20,'needle-valve flow'),
 'spg_int':  (0.5,2,'sparge interval (duty)'),
}
KEYS=['rH2_mol_h','O2_excess','strip_ratio','CO2_sd']

b=model(BASE)
print("BASELINE (AEP0.1.1):")
for k in KEYS: print(f"  {k:12} = {b[k]:.4g}")
print(f"  verdicts: strip_ratio {b['strip_ratio']:.3f} (<1 => stripping insufficient); CO2_sd {b['CO2_sd']:.1f} (>1 => carbon ok)")

def report(title, D):
    print(f"\n=== {title} — span of each output across the input's range ===")
    print(f"  {'input':12} {'O2_excess span%':>16} {'strip_ratio span%':>18} {'rH2 span%':>11} {'CO2_sd span%':>13}")
    rows=[]
    for nm,(lo,hi,_) in D.items():
        rl,rh=run(nm,lo),run(nm,hi)
        def span(k):
            a,bv=rl[k],rh[k]
            if any(map(lambda x:isinstance(x,float) and math.isnan(x),(a,bv))): return float('nan')
            base=b[k]
            return abs(bv-a)/abs(base)*100 if base else float('nan')
        rows.append((nm,span('O2_excess'),span('strip_ratio'),span('rH2_mol_h'),span('CO2_sd')))
    rows.sort(key=lambda r:(-(r[1] if not math.isnan(r[1]) else -1)))
    for nm,oe,sr,rh,cs in rows:
        print(f"  {nm:12} {oe:>15.1f}% {sr:>17.1f}% {rh:>10.1f}% {cs:>12.1f}%")

report("UNCERTAIN MEASUREMENTS", MEAS)
report("KNOBS (control authority, not measurements)", KNOBS)
