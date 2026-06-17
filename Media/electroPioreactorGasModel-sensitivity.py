#!/usr/bin/env python3
"""Comprehensive one-at-a-time (OAT) sensitivity analysis for electroPioreactorGasModel.xlsx.

Re-implements the full model (geometry → electrolysis → biology → O2 ceiling → CO2 dosing
→ bubble/strip → surface/headspace → dissolved CO2 → H2 availability → §14 optimiser) in
plain Python so the analysis is reviewable without Excel. Runs in OPTIMAL schedule mode
(spg_dur/spg_int computed by the optimiser), so the sweep shows what actually moves the
RECOMMENDED schedule and the feasibility of reaching growth.

Covers every NON-ABSOLUTE input. Excluded (absolute / defined): F_const, R_gas, g_const,
Pa_per_atm, z_e_H2, z_e_O2, M_CO2, T_ref.

Each input carries an IGNORANCE tier — DATA-GAP (unmeasured), ESTIMATE, LITERATURE
(well-known), KNOB (you set it). Urgency = leverage on the critical outputs × how poorly
we know the value. KNOBs are control authority, reported separately (not "attention").
"""
import math
PI=math.pi

BASE=dict(
  # --- geometry (measured / estimated for the build) ---
  vial_OD=27.48, vial_wall=1.1, D_int=55, V_max=16, V_vial_total=20,
  rod_d=6, rod_n=2, elec_clear=22, spg_OD=3.175, spg_ID=1.5875,
  eff_OD=3.175, eff_ID=1.5875, xtube_n=3, xtube_pro=5,
  # --- electrolysis ---
  intensity=3, gerrit_slope=1.03, gerrit_int=2.6, F=96485.33212,
  z_e_H2=2, z_e_O2=4, etaF=1.0, etaF_OER=1.0, z_e_ORR=4,
  # --- biology ---
  bio_H2=6, bio_O2=2, bio_CO2=1,
  # --- O2 ceiling / Henry ---
  T_C=30, P_atm=101325, H_O2ref=1.3e-5, H_O2T=1500, T_ref=298.15, O2_ceil_atm=0.3,
  # --- CO2 dosing ---
  Q_CO2=10, pulse_floor=0.5, R=8.314462618, M_CO2=44.0095,
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
    T_K=p['T_C']+273.15
    # geometry
    vial_ID=p['vial_OD']-2*p['vial_wall']; A_x=PI/4*vial_ID**2
    h_datum=p['V_max']*1000/A_x; elec_ins=p['D_int']-p['elec_clear']; spg_tip_h=p['elec_clear']
    disp=(p['rod_n']*(PI/4*p['rod_d']**2)*max(0,h_datum-p['elec_clear'])
          +(PI/4*p['spg_OD']**2)*max(0,h_datum-spg_tip_h)
          +(PI/4*(p['eff_OD']**2-p['eff_ID']**2))*((p['eff_OD']+p['eff_ID'])/2))/1000
    V_charge=round(p['V_max']-disp,0); h_actual=(V_charge+disp)*1000/A_x
    interface_A=A_x-(p['rod_n']*(PI/4*p['rod_d']**2)+(PI/4*p['spg_OD']**2)+(PI/4*p['eff_OD']**2))
    # electrolysis
    I_app=(p['gerrit_slope']*p['intensity']+p['gerrit_int'])/1000
    rH2=I_app*p['etaF']/(p['z_e_H2']*p['F'])*3600
    rO2=I_app*p['etaF_OER']/(p['z_e_O2']*p['F'])*3600
    O2_cath=I_app*(1-p['etaF'])/(p['z_e_ORR']*p['F'])*3600
    O2_net=rO2-O2_cath
    O2_cons=rH2*p['bio_O2']/p['bio_H2']; CO2_cons=rH2*p['bio_CO2']/p['bio_H2']
    O2_excess=O2_net-O2_cons
    # O2 ceiling
    H_O2_T=p['H_O2ref']*math.exp(p['H_O2T']*(1/T_K-1/p['T_ref'])); O2_ceil_C=H_O2_T*p['O2_ceil_atm']*p['P_atm']
    nCO2=p['P_atm']*(p['Q_CO2']/1e6/60)/(p['R']*T_K)
    t_lag=O2_ceil_C*(V_charge/1e6)/O2_net*60
    # --- §14 optimiser (Optimal mode) ---
    duty_carbon=p['carbon_margin_min']*CO2_cons/(nCO2*3600)
    duty_O2vent=O2_net/(p['target_DO_frac']*p['O2_ceil_atm'])/(nCO2*3600)
    duty_opt=max(duty_carbon,duty_O2vent)
    spg_int_max=p['target_DO_frac']*t_lag
    spg_dur=p['pulse_floor']
    spg_int=min(spg_dur/(60*duty_opt), spg_int_max)   # minutes
    duty=spg_dur/(spg_int*60)
    CO2_supply=nCO2*spg_dur*(60/spg_int); CO2_sd=CO2_supply/CO2_cons if CO2_cons>0 else float('nan')
    # bubble / strip (tube); Mendelson NA-guard < 1 mm
    d_or=p['spg_ID']/1000; d_b=(6*d_or*p['sigma']/(p['rho_L']*p['g']))**(1/3)
    if d_b<0.001:
        strip_avg=float('nan'); strip_ratio=float('nan')
    else:
        u_rise=math.sqrt(p['mend_a']*p['sigma']/(p['rho_L']*d_b)+p['mend_b']*p['g']*d_b)
        u_sg=(p['Q_CO2']/1e6/60)/(A_x/1e6); holdup=u_sg/u_rise; a_int=6*holdup/d_b; t_c=d_b/u_rise
        kL=2*math.sqrt(p['D_O2']/(PI*t_c)); kLa=kL*a_int
        strip_sparge=kLa*(V_charge/1e6)*O2_ceil_C*3600; strip_avg=strip_sparge*duty
        strip_ratio=strip_avg/O2_excess if O2_excess>0 else float('nan')
    # surface
    tip=PI*(p['stir_len']/1000)*p['stir_rpm']/60; s_ren=tip/(vial_ID/1000)
    kL_surf=2*math.sqrt(p['D_O2']*s_ren/PI)*p['kL_surf_factor']
    a_surf=interface_A/V_charge; kLa_surf=kL_surf*a_surf
    surf_strip=kLa_surf*(V_charge/1e6)*O2_ceil_C*3600; surf_ratio=surf_strip/O2_excess if O2_excess>0 else float('nan')
    sa=0 if math.isnan(strip_avg) else strip_avg
    removal_ratio=(sa+surf_strip+O2_cath)/O2_excess if O2_excess>0 else float('nan')
    # dissolved CO2 / H2
    H_CO2_T=p['H_CO2ref']*math.exp(p['H_CO2T']*(1/T_K-1/p['T_ref'])); CO2_diss=H_CO2_T*p['P_atm']
    carbon_margin=CO2_diss*1000/p['Km_CO2']
    H_H2_T=p['H_H2ref']*math.exp(p['H_H2T']*(1/T_K-1/p['T_ref'])); C_H2=H_H2_T*p['P_atm']
    t_H2_sat=C_H2*(V_charge/1e6)/rH2*60
    return dict(spg_int_opt=spg_int, spg_int_opt_s=spg_int*60, duty_opt=duty, CO2_sd=CO2_sd,
                t_O2_ceiling_lag=t_lag, O2_removal_ratio=removal_ratio, surf_ratio=surf_ratio,
                O2_excess=O2_excess, rH2=rH2, carbon_margin=carbon_margin, t_H2_sat=t_H2_sat,
                strip_ratio=strip_ratio)

# (input, low, high, tier).  tiers: DATA-GAP, ESTIMATE, LITERATURE, KNOB
SWEEP=[
 # ---- DATA-GAP (unmeasured) ----
 ('etaF',0.5,1.0,'DATA-GAP'),
 ('kL_surf_factor',0.25,4.0,'DATA-GAP'),     # surface kLa is a coarse proxy: order-of-magnitude
 ('bio_O2',1.6,2.4,'DATA-GAP'),
 ('bio_CO2',0.8,1.3,'DATA-GAP'),
 ('pulse_floor',0.3,1.0,'DATA-GAP'),
 # ---- ESTIMATE ----
 ('O2_ceil_atm',0.25,0.35,'ESTIMATE'),
 ('z_e_ORR',2,4,'ESTIMATE'),
 ('etaF_OER',0.9,1.0,'ESTIMATE'),
 ('vial_wall',0.9,1.3,'ESTIMATE'),
 ('Km_CO2',20,80,'ESTIMATE'),
 ('gerrit_slope',0.95,1.11,'ESTIMATE'),      # empirical rig fit ±8%
 ('gerrit_int',2.2,3.0,'ESTIMATE'),
 ('u_g_max',0.03,0.10,'ESTIMATE'),
 ('V_max',14,18,'ESTIMATE'),
 # ---- LITERATURE (well-known) ----
 ('D_O2',2.07e-9,2.43e-9,'LITERATURE'),
 ('sigma',0.0698,0.0726,'LITERATURE'),
 ('rho_L',990.6,1000.7,'LITERATURE'),
 ('H_O2ref',1.20e-5,1.40e-5,'LITERATURE'),
 ('H_O2T',1275,1725,'LITERATURE'),
 ('H_CO2ref',3.05e-4,3.55e-4,'LITERATURE'),
 ('H_H2ref',7.2e-6,8.4e-6,'LITERATURE'),
 ('mend_a',2.03,2.25,'LITERATURE'),
 ('mend_b',0.48,0.53,'LITERATURE'),
 # ---- KNOB (you set it) ----
 ('intensity',3,25,'KNOB'),
 ('Q_CO2',5,20,'KNOB'),
 ('target_DO_frac',0.3,0.9,'KNOB'),
 ('carbon_margin_min',1.5,3.0,'KNOB'),
 ('stir_rpm',250,900,'KNOB'),
 ('T_C',28,34,'KNOB'),
]
# outputs that decide whether we reach growth / what schedule to run
CRITICAL=['spg_int_opt','t_O2_ceiling_lag','O2_removal_ratio','surf_ratio','t_H2_sat']
WEIGHT={'DATA-GAP':1.0,'ESTIMATE':0.6,'LITERATURE':0.15,'KNOB':0.0}

def run(name,val):
    p=dict(BASE); p[name]=val; return model(p)

b=model(BASE)
print("="*88)
print("BASELINE (Optimal mode, tube, AEP0.1.1):")
for k in ['spg_int_opt_s','duty_opt','t_O2_ceiling_lag','O2_removal_ratio','surf_ratio','t_H2_sat','carbon_margin','rH2','CO2_sd']:
    print(f"   {k:18}= {b[k]:.4g}")
print(f"   => recommended schedule: {b['spg_int_opt']*0+BASE['pulse_floor']}s pulse every {b['spg_int_opt_s']:.0f}s")

def span(name,lo,hi,k):
    rl,rh=run(name,lo),run(name,hi)
    a,c=rl[k],rh[k]
    if any(isinstance(x,float) and math.isnan(x) for x in (a,c)): return float('nan')
    base=b[k]
    return abs(c-a)/abs(base)*100 if base else float('nan')

print("\n"+"="*88)
print("LEVERAGE — % change in each critical output across the input's plausible range")
print(f"{'input':16}{'tier':10}{'sched%':>8}{'tO2lag%':>9}{'remRatio%':>10}{'surfR%':>8}{'tH2%':>7}")
rows=[]
for name,lo,hi,tier in SWEEP:
    sp={k:span(name,lo,hi,k) for k in CRITICAL}
    crit=max([v for v in sp.values() if not math.isnan(v)] or [0])
    rows.append((name,tier,sp,crit))
for name,tier,sp,crit in rows:
    def f(k): v=sp[k]; return f"{v:>7.0f}" if not math.isnan(v) else "    n/a"
    print(f"{name:16}{tier:10}{f('spg_int_opt'):>8}{f('t_O2_ceiling_lag'):>9}{f('O2_removal_ratio'):>10}{f('surf_ratio'):>8}{f('t_H2_sat'):>7}")

print("\n"+"="*88)
print("URGENT ATTENTION ranking = leverage × ignorance  (KNOBs excluded — those are control levers)")
scored=[(name,tier,crit,crit*WEIGHT[tier]) for name,tier,sp,crit in rows if tier!='KNOB']
scored.sort(key=lambda r:-r[3])
print(f"{'rank':5}{'input':16}{'tier':10}{'max critical span%':>20}{'urgency score':>15}")
for i,(name,tier,crit,score) in enumerate(scored,1):
    print(f"{i:<5}{name:16}{tier:10}{crit:>18.0f}%{score:>15.1f}")

print("\nKNOBS (control authority — biggest levers you turn deliberately):")
knobs=[(name,crit) for name,tier,sp,crit in rows if tier=='KNOB']
knobs.sort(key=lambda r:-r[1])
for name,crit in knobs: print(f"   {name:18} max critical span {crit:.0f}%")
