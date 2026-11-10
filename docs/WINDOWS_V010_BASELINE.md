# Archived Windows validation evidence for v0.1.0 — NOT v0.1.1

Reported by the research user on 10 November 2026. Tests executed from an
isolated Windows virtual environment using Python 3.14, NumPy 2.5.4 and
SciPy 1.18.1.

- `pip install` completed successfully.
- `pip check`: `No broken requirements found.`
- `python -m contactimpactbench verify`: `passed: true`, counts: N3.3=4,
  N3.4=1, N3.6=4.
- Three CLI examples ran: impact (spin=20), normal (8 psi), friction (q=1,
  alpha=0).
- `python -m contactimpactbench verify --full`: `passed: true`, counts:
  N3.3=36, N3.4=24, N3.6=4.

The full terminal transcript is present in the conversation, not embedded as a
falsely independently generated machine file. This note is a faithful summary
of that user-provided record, not a fresh v0.1.1 test. A machine-readable
report for v0.1.1 must be generated with `tools/verification_record.py`.
