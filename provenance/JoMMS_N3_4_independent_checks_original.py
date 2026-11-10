"""JoMMS N3.4: independently integrated normal contact + patch-radius and timestep sensitivity.
Original N3.3 untouched; its chi mapping is temporarily replaced for parameter tests only.
"""
import csv, sys, math
from pathlib import Path
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0,str(Path(__file__).resolve().parent))
import JoMMS_N3_3_kelvin_consistent as N
OUT=Path('/mnt/data')
PSI=6894.757293168

def independent_normal(p,law, speed=4.0):
    kn=2*np.pi*N.R*p
    def slope(d):return kn*d if law=='A' else np.pi*p*(2*N.R*d-d*d)
    def rhs(t,y):
        delta,v=y
        force=max(0.,slope(max(0.,delta))+N.c_hc*max(0.,delta)*(-v))
        return [-v,force/N.m]
    def lift(t,y):return y[0]
    lift.direction=-1;lift.terminal=True
    # Begin at small positive delta, to avoid root at t=0.
    tiny=1e-10
    init=[tiny,-speed]
    sol=solve_ivp(rhs,(0,.04),init,method='DOP853',rtol=2e-11,atol=2e-13,max_step=1.5e-5,events=lift,dense_output=True)
    if len(sol.t_events[0])==0: raise RuntimeError('no liftoff')
    T=float(sol.t_events[0][0]); samples=np.linspace(0,T,10001); y=sol.sol(samples)
    F=np.maximum(0.,np.array([slope(max(0,d)) for d in y[0]])+N.c_hc*np.maximum(0,y[0])*(-y[1]))
    return T,float(np.max(F)),float(sol.y_events[0][0][1])

rows=[]
for psi in [4.,8.,12.]:
 for law in ['A','B']:
    p=psi*PSI
    tref,fref,vref=independent_normal(p,law)
    for h in [4e-6,2e-6,1e-6,0.5e-6]:
       r=N.simulate(0.,v0=(0.,0.,-4.),p=p,normal=law,dt=h,zeta_t=0)
       # tangential internal state must stay zero: exact independent normal test.
       rows.append(dict(pressure_psi=psi,normal_law=law,dt_us=h*1e6,tc_ms=r.tc*1e3,tc_ref_ms=tref*1e3,tc_error_ms=(r.tc-tref)*1e3,Nmax_N=r.peakN,Nmax_ref_N=fref,Nmax_error_N=r.peakN-fref,vz_out=r.vz,vz_ref=vref,vz_error=r.vz-vref,positive_sum_J=r.positive_sum,max_phi=r.max_phi))
with open(OUT/'JoMMS_N3_4_normal_independent.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)

patch=[]; original=N.chi
for factor in [.7,1.,1.3]:
 N.chi=lambda d,scale=factor:scale*original(d)
 for spin in [20.,100.,300.]:
  for dt in [2e-6,1e-6]:
   r=N.simulate(spin,p=8*PSI,normal='B',dt=dt,zeta_t=.25)
   patch.append(dict(chi_factor=factor,spin_rad_s=spin,dt_us=dt*1e6,vx_out=r.vx,vy_out=r.vy,omega3_out=r.w3,dE_J=r.dE,peakN=r.peakN,peakFt=r.peakFt,peakM=r.peakM,grip_steps=r.grip_steps,slip_steps=r.slip_steps,reversals=r.reversal_count,max_phi=r.max_phi,positive_sum=r.positive_sum,residual_max=r.residual_max))
N.chi=original
with open(OUT/'JoMMS_N3_4_patch_sensitivity.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=patch[0]);w.writeheader();w.writerows(patch)
print('normal comparisons:',len(rows),'patch tests:',len(patch))
for law in ['A','B']:
 sel=[r for r in rows if r['normal_law']==law and r['pressure_psi']==8]
 print(law,[(r['dt_us'],round(r['tc_error_ms'],6),round(r['Nmax_error_N'],5)) for r in sel])
for spin in [20.,100.,300.]:
 print('patch spin',spin,[(r['chi_factor'],round(r['vy_out'],5),round(r['omega3_out'],5)) for r in patch if r['spin_rad_s']==spin and r['dt_us']==1])
print('max patch pos energy',max(r['positive_sum'] for r in patch),'max phi',max(r['max_phi'] for r in patch))
