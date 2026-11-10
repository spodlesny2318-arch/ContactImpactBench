"""Documented CLI for numerical verification, not experimental validation."""
import argparse
import json
from pathlib import Path
from .reduced import ReducedCase, run_impact, result_summary
from .normal import compare_normal, PSI_PA
from .friction import distributed_friction, friction_ellipsoid, drilling_arm, weak_spin_slope

def _save(d, path):
    text = json.dumps(d, indent=2, ensure_ascii=False, allow_nan=False)
    if path:
        target = Path(path)
        if not target.parent.is_dir():
            raise ValueError(f'Output directory does not exist: {target.parent}')
        target.write_text(text + '\n', encoding='utf-8')
    else:
        print(text)

def main(argv=None):
    parser = argparse.ArgumentParser(
        prog='contactimpactbench',
        description='Research verification benchmarks (not experimental validation)')
    sub = parser.add_subparsers(dest='cmd', required=True)
    run = sub.add_parser('impact', help='One archived N3.3 reduced-impact trajectory')
    run.add_argument('--spin', type=float, default=20.0)
    run.add_argument('--pressure-psi', type=float, default=55.16e3 / PSI_PA)
    run.add_argument('--dt-us', type=float, default=2.0)
    run.add_argument('--law', choices=['A', 'B'], default='A')
    run.add_argument('--zeta', type=float, default=.25)
    run.add_argument('--output')
    normal = sub.add_parser('normal', help='N3.3 vs independent normal-only N3.4 DOP853')
    normal.add_argument('--pressure-psi', type=float, default=8.)
    normal.add_argument('--dt-us', type=float, default=2.)
    normal.add_argument('--law', choices=['A', 'B'], default='A')
    normal.add_argument('--output')
    patch = sub.add_parser('friction', help='N3.6 prescribed patch vs ellipsoid')
    patch.add_argument('--q', type=float, default=1.)
    patch.add_argument('--alpha', type=float, default=0.)
    patch.add_argument('--nr', type=int, default=128)
    patch.add_argument('--nt', type=int, default=384)
    patch.add_argument('--output')
    verify = sub.add_parser('verify', help='Curated archived regression checks')
    verify.add_argument('--full', action='store_true', help='N3.3 36-case grid and N3.4 24 comparisons')
    verify.add_argument('--output')
    env = sub.add_parser('env', help='Print privacy-conscious environment/version metadata')
    env.add_argument('--output')
    args = parser.parse_args(argv)
    try:
        if args.cmd == 'impact':
            case = ReducedCase(spin_rad_s=args.spin,
                pressure_pa=args.pressure_psi * PSI_PA, time_step_s=args.dt_us * 1e-6,
                normal_law=args.law, tangential_damping_ratio=args.zeta)
            result = {'model': 'N3.3', 'parameters': vars(args),
                      'results': result_summary(run_impact(case)), 'physical_validation': False}
        elif args.cmd == 'normal':
            result = compare_normal(pressure_pa=args.pressure_psi * PSI_PA,
                law=args.law, dt=args.dt_us * 1e-6)
        elif args.cmd == 'friction':
            result = {'distributed': distributed_friction(args.q, args.alpha, nr=args.nr, nt=args.nt),
                      'ellipsoid': friction_ellipsoid(args.q, args.alpha),
                      'chi_over_a': drilling_arm(args.alpha),
                      'weak_spin_slope': weak_spin_slope(args.alpha),
                      'pressure_model': 'prescribed, not derived from a shell'}
        elif args.cmd == 'verify':
            from .checks import verify_archive
            result = verify_archive(full=args.full)
        else:
            from .environment import environment_info
            result = environment_info()
        _save(result, args.output)
        return 1 if args.cmd == 'verify' and not result['passed'] else 0
    except (OSError, ValueError, TypeError) as err:
        parser.error(str(err))

if __name__ == '__main__':
    raise SystemExit(main())
