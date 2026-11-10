"""N3.6: controlled radial-pressure distributed gross-slip circular-patch study.
Radial pressure p_c(r)=N(alpha+1)/(pi*a^2)*(1-(r/a)^2)^alpha, alpha>=0.
This is a prescribed profile, NOT an inflated-shell solution or full grip-slip dynamics.
Dependencies numpy scipy matplotlib. Run: python JoMMS_N36_patch.py
"""
from pathlib import Path
import csv
import numpy as np
from scipy.special import beta
from numpy.polynomial.legendre import leggauss
from math import pi,sqrt
OUT=Path(__file__).resolve().parent
MU=.55

def chi_analytic(alpha):
    return (alpha+1)*beta(1.5,alpha+1) # chi/a, pure drilling

def low_spin_slope(alpha):
    return 1/(2*(alpha+2)) # - M/(mu*N*a*q) as q->0

def distributed(q,alpha,nr=128,nt=384):
    """F/(mu N), M/(mu N a), D/(mu N |s|), s=(1,0), omega*a=q.
       Radial variable t=(r/a)^2, exact area weighting.
    """
    rnodes, rw=leggauss(nr);t=(rnodes+1)/2;wt=rw/2
    radius=np.sqrt(t)
    wt=wt*(alpha+1)*np.power(1-t,alpha)
    wt=wt/np.sum(wt) # exact total-load normalization of the discrete profile
    theta=2*pi*(np.arange(nt)+.5)/nt
    X=radius[:,None]*np.cos(theta)[None,:]
    Y=radius[:,None]*np.sin(theta)[None,:]
    ux=1-q*Y;uy=q*X
    mod=np.hypot(ux,uy)
    fx=-ux/mod;fy=-uy/mod
    mm=X*fy-Y*fx
    w=wt[:,None]/nt
    F1=float(np.sum(w*fx));F2=float(np.sum(w*fy));M=float(np.sum(w*mm))
    return F1,F2,M,-F1-q*M

def ellipsoid(q,alpha):
    c=chi_analytic(alpha);norm=sqrt(1+(c*q)**2)
    return -1/norm,0.,-(c*c*q)/norm,norm

def write_csv(name,rows):
    with open(OUT/name,'w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)

if __name__=='__main__':
    alphas=[0.,.5,1.,2.]
    qs=[0.,.05,.1,.25,.5,1.,2.,4.,10.,30.]
    geom=[];rows=[];convergence=[]
    for alpha in alphas:
        c=chi_analytic(alpha);slope=low_spin_slope(alpha)
        geom.append(dict(alpha=alpha,chi_over_a=c,low_q_M_slope_distributed=slope,
                         low_q_M_slope_ellipsoid=c*c,ratio_ellipsoid_to_distributed_slope=c*c/slope,
                         peak_pressure_over_mean=alpha+1))
        for q in qs:
            F1,F2,M,D=distributed(q,alpha)
            L1,L2,LM,LD=ellipsoid(q,alpha)
            phi=F1**2+(M/c)**2
            rows.append(dict(alpha=alpha,q=q,Fx_distributed_over_muN=F1,
                             M_distributed_over_muNa=M,D_distributed_over_muN_s=D,
                             Fx_ellipsoid_over_muN=L1,M_ellipsoid_over_muNa=LM,
                             D_ellipsoid_over_muN_s=LD,
                             abs_F_error_over_muN=abs(F1-L1),abs_M_error_over_muNa=abs(M-LM),
                             distributed_phi_under_chi_ellipsoid=phi,
                             distributed_power_nonnegative=D>=-1e-12))
        for q in [0.1,1.,4.,10.]:
            ref=np.array(distributed(q,alpha,256,768))
            for nr,nt in [(32,96),(64,192),(128,384)]:
                z=np.array(distributed(q,alpha,nr,nt))
                convergence.append(dict(alpha=alpha,q=q,nr=nr,nt=nt,
                                        max_abs_FM_D_error_vs_highres=float(max(abs(z[[0,2,3]]-ref[[0,2,3]])))))
    write_csv('N36_geometry.csv',geom)
    write_csv('N36_patch.csv',rows)
    write_csv('N36_convergence.csv',convergence)
    # Pressure normalization and limiting formula tests (analytic and numerics).
    assert abs(chi_analytic(0)-2/3)<1e-14
    for alpha in alphas:
        for q in [0,.1,.5,1,2,4,10]:
            f,fy,m,d=distributed(q,alpha)
            assert abs(fy)<1e-11
            assert d>=-1e-11
            assert abs(d+f+q*m)<1e-12
            assert abs(f)<=1+1e-10
            assert abs(m)<=chi_analytic(alpha)+1e-10
        # finite small spin check; local singularity doesn't occur for q<1
        slope=-distributed(1e-4,alpha)[2]/1e-4
        assert abs(slope-low_spin_slope(alpha))<1e-6,(alpha,slope)
        # large-q tends to analytic pure spin
        large=distributed(10000,alpha,128,384)
        assert abs(-large[2]-chi_analytic(alpha))<2e-4,(alpha,large)
    # Uniform alpha=0 cross-check with previous N3.5 implementation
    import JoMMS_N35_patch as old
    for q in [0,.1,.5,1.,2.,4.,10.]:
        diff=np.array(distributed(q,0,128,384))-np.array(old.distributed(q,128,384))
        assert np.max(np.abs(diff))<1e-4,(q,diff) # distinct quadratures near slip-velocity zeros
    assert max(z['max_abs_FM_D_error_vs_highres'] for z in convergence if z['nr']==128)<0.001
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    x=np.geomspace(.03,30,110)
    fig,axs=plt.subplots(2,1,figsize=(8,7.5),sharex=True)
    for alpha in alphas:
        vals=np.array([distributed(q,alpha,64,192) for q in x])
        axs[0].semilogx(x,-vals[:,0],label=f'alpha={alpha:g}')
        axs[1].semilogx(x,-vals[:,2],label=f'alpha={alpha:g}')
    axs[0].set_ylabel(r'$|F_t|/(\mu N)$')
    axs[1].set_ylabel(r'$|M_3|/(\mu N a)$')
    axs[1].set_xlabel(r'$q=|\omega_3|a/|s|$')
    for ax in axs:ax.grid(True,alpha=.3);ax.legend()
    fig.tight_layout();fig.savefig(OUT/'N36_pressure_profiles.png',dpi=175);plt.close(fig)
    print('Geometry:')
    for r in geom:print(r)
    print('At q=1:')
    for r in rows:
        if r['q']==1:print(r['alpha'],r['Fx_distributed_over_muN'],r['M_distributed_over_muNa'],r['abs_F_error_over_muN'],r['abs_M_error_over_muNa'],r['distributed_phi_under_chi_ellipsoid'])
    print('Maximum convergence error @128x384:',max(z['max_abs_FM_D_error_vs_highres'] for z in convergence if z['nr']==128))
    print('Checks PASS')
