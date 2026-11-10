"""Interfaces to exact archived N3.6 radial gross-slip patch quadrature.

Prescribed radial pressure is not calculated from an inflatable shell.
"""
from math import isfinite
from ._legacy import JoMMS_N36_patch as n36

def _check(alpha,q=None):
    if alpha<0 or not isfinite(alpha):
        raise ValueError('alpha must be finite and nonnegative')
    if q is not None and (q<0 or not isfinite(q)):
        raise ValueError('q must be finite and nonnegative')

def drilling_arm(alpha=0.):
    """Pure-drilling effective arm chi/a."""
    _check(alpha)
    return float(n36.chi_analytic(alpha))

def weak_spin_slope(alpha=0.):
    """Leading coefficient -M/(mu*N*a*q), q -> 0+."""
    _check(alpha)
    return float(n36.low_spin_slope(alpha))

def distributed_friction(q,alpha=0.,*,nr=128,nt=384):
    """Gross-slip patch F/(mu N), M/(mu N a), dissipation/(mu N |s|)."""
    _check(alpha,q)
    if not isinstance(nr,int) or not isinstance(nt,int) or nr<2 or nt<8:
        raise ValueError('nr>=2, nt>=8 required')
    fx,fy,m,d=n36.distributed(q,alpha,nr,nt)
    return {'Fx_over_muN':fx,'Fy_over_muN':fy,'M_over_muNa':m,
            'dissipation_over_muNs':d,'q':q,'alpha':alpha,
            'quadrature':{'nr':nr,'nt':nt}}

def friction_ellipsoid(q,alpha=0.):
    _check(alpha,q)
    fx,fy,m,d=n36.ellipsoid(q,alpha)
    return {'Fx_over_muN':fx,'Fy_over_muN':fy,'M_over_muNa':m,
            'dissipation_over_muNs':d,'q':q,'alpha':alpha}
