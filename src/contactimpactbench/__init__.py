"""ContactImpactBench: verification tools for reduced compliant impact.

Numerical verification examples, NOT experimental validation of an inflatable shell.
"""
from .reduced import ReducedCase, run_impact, result_summary
from .normal import normal_reference, compare_normal
from .friction import distributed_friction, friction_ellipsoid, drilling_arm, weak_spin_slope
__version__ = '0.1.4'
__all__ = ['ReducedCase','run_impact','result_summary','normal_reference',
           'compare_normal','distributed_friction','friction_ellipsoid',
           'drilling_arm','weak_spin_slope']
