# Linux v0.1.1 check — 10 November 2026

- Test platform: Linux, Python 3.13.5, x86_64.
- Package wheel: `contactimpactbench-0.1.1-py3-none-any.whl`.
- Legacy kernel SHA-256: **unchanged** from v0.1 (N3.3 and N3.6).
- `pytest`: **21/21** PASS in package source and 21/21 with the wheel installed.
- `python -m contactimpactbench verify --full`: **PASS**, counts N3.3=36,
  N3.4=24, N3.6=4; failures=[] (console output recorded during this run).
- `python -m contactimpactbench env`: v0.1.1, NumPy 2.3.5,
  SciPy 1.17.0.

## Limitation of the environment

The Linux venv did not independently download or install NumPy/SciPy.
Those existing dependencies were made visible from
`/opt/pyvenv/lib/python3.13/site-packages` using `PYTHONPATH`.
Therefore **Linux wheel runtime passed**, but the criterion of a new
fully independent dependency environment is **NOT MET**.

The version-record script (`reports/linux_v011_fast_verification.json`)
returned `all_steps_passed=false` solely because `pip check` found an
unrelated inherited-environment conflict:

`moviepy 2.2.1 has requirement pillow<12.0,>=9.2.0, but you have pillow 12.3.0.`

The package CLI actions `env`, `impact`, `normal`, `friction`, and the fast
archived regression **each returned exit code 0**. Do not interpret this as
a successful whole-environment dependency check.

The v0.1.0 Windows user run was clean in its separate Python 3.14 venv,
but it cannot be substituted for v0.1.1 Windows verification.

Neither test constitutes physical validation of inflated-shell impact.
