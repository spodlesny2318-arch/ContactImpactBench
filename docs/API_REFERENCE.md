# Python API reference — ContactImpactBench v0.1.1

The package exposes *numerical verification examples*, not experimentally
validated predictions for an inflated hyperelastic shell.

## N3.3 — Reduced impact (`contactimpactbench.reduced`)

```python
from contactimpactbench import ReducedCase, run_impact, result_summary
case = ReducedCase(spin_rad_s=20.0, pressure_pa=55160.0,
                   time_step_s=2e-6, normal_law='A',
                   tangential_damping_ratio=0.25)
result = result_summary(run_impact(case))
print(result['peakN'], result['positive_sum'])
```

`ReducedCase` (frozen dataclass):

| Parameter | Default | Unit / meaning |
|---|---:|---|
| `spin_rad_s` | 20 | Initial drilling rotation (rad/s) |
| `velocity_m_s` | `(4, 0, -4)` | Initial center velocity, x/y/z in m/s |
| `pressure_pa` | kernel baseline | Prescribed *gauge* pressure, Pa |
| `time_step_s` | `2e-6` | Time step, s |
| `maximum_time_s` | `0.04` | Limit of integration, s |
| `normal_law` | `A` | A: small-indentation pressure-proportional; B: geometric proxy |
| `tangential_damping_ratio` | `0.25` | Dimensionless reduced damping parameter |

`run_impact(case, record=False)` returns the **frozen original N3.3 result object**, with fields such as `peakN`, `peakFt`, `peakM`, `dE`, `positive_sum`, `residual_max`, `max_phi`, `tc`, and rebound velocities. Use `result_summary()` for a JSON-friendly dictionary; `tc` is exposed as `contact_time_ms`.

Important: `positive_sum` and `residual_max` check the stated *discrete* accounting. An energy residual near roundoff is not experimental validation. Contact memory is not a derived field of the hyperelastic shell.

## N3.4 — Independent *normal-only* comparator (`contactimpactbench.normal`)

```python
from contactimpactbench import normal_reference, compare_normal
reference = normal_reference(pressure_pa=8 * 6894.757293168, law='A')
comparison = compare_normal(pressure_pa=8 * 6894.757293168,
                            law='A', dt=2e-6)
print(comparison['difference'])
```

- `normal_reference(pressure_pa=..., law='A', inbound_speed_m_s=4.0)` uses `scipy.integrate.solve_ivp(method='DOP853')` and a localized lift-off event.
- `compare_normal(..., dt=..., inbound_speed_m_s=...)` compares the DOP853 reference to the frozen N3.3 time-stepping scheme using the *same normal force law*.

Neither function independently solves the full tangential/spinning dynamics.

## N3.6 — Prescribed pressure patch (`contactimpactbench.friction`)

```python
from contactimpactbench import distributed_friction, friction_ellipsoid
from contactimpactbench import drilling_arm, weak_spin_slope
q = 1.0
p = distributed_friction(q, alpha=0.0, nr=128, nt=384)
e = friction_ellipsoid(q, alpha=0.0)
print(p['M_over_muNa'], e['M_over_muNa'])
```

`q = |omega_3| a / |s|` is a nonnegative nondimensional spin/sliding ratio; `alpha >= 0` controls a **prescribed**, normalized radial pressure profile. `nr`, `nt` control quadrature. `drilling_arm(alpha)` and `weak_spin_slope(alpha)` return the archived analytical limits.

The output contains normalized force, moment and frictional dissipation. Do not interpret the pressure profile as being derived from the shell.

## Archived data and checks

```python
from contactimpactbench.reference import datasets, load_reference
from contactimpactbench.checks import verify_archive
print(datasets())
print(len(load_reference('n33')))
print(verify_archive(full=False)['passed'])
```

- `load_reference('n33')`: 36 archived N3.3 trajectories.
- `load_reference('n34')`: 24 N3.4 cases; not 48.
- `load_reference('n36_geometry')`: 4 analytical limit fixtures.
- `load_reference('n31_negative')`: known defective legacy N3.1 energy results for a negative test; **never** use as a physical reference.
- `verify_archive(full=True)` executes a **regression** check, not physical validation.

## CLI and environment record

```bash
python -m contactimpactbench env
python -m contactimpactbench verify --full
python tools/verification_record.py --output verification_record.json --full
```

The report records the Python, NumPy and SciPy versions, summary of commands, output and exit status. This is not an external experimental benchmark. The report intentionally omits usernames and local installation paths; console output may nonetheless contain user-provided paths when a command fails, so inspect before sharing publicly.

## Error handling

The CLI converts invalid user parameters and output-path errors into explanatory usage messages rather than Python tracebacks. Importing the package does not trigger an impact simulation. API errors use `ValueError` for invalid numerical inputs.

## Provenance and license

The original N3.3 and N3.6 computational kernels in `_legacy/` remain byte-identical to v0.1. Review `provenance/SOURCES_SHA256.csv` and `RELEASE_GATE.md`. This source tree is distributed under the **MIT License** (see `LICENSE`). It provides numerical verification fixtures, not experimental physical validation.
