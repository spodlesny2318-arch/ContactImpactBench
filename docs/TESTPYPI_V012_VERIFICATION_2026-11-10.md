# Public TestPyPI v0.1.2 — Windows verification record

**Source of evidence:** user-provided PowerShell logs on 2026-11-10,
not independent experimental measurements.

- TestPyPI URL: https://test.pypi.org/project/contactimpactbench/0.1.2/
- Published: `.whl` and `.tar.gz`; both accepted by TestPyPI.
- Windows AMD64, Python 3.14.3, NumPy 2.5.4, SciPy 1.18.1.
- Clean separate environment: `pip check`: `No broken requirements found.`
- `python -m contactimpactbench verify --full` output:

```json
{"passed":true,"counts":{"n33":36,"n34":24,"n36":4},"failures":[],"scope":"Full historical N3.3 grid and N3.4 reference","is_physical_validation":false}
```

The record demonstrates package installation and *archived-regression*
consistency; it does **not** validate physical contact forces, inflated-shell
behavior or contact patch pressure against independent observations.
