# Changelog

## 0.1.3 — 2026-11-10 (source release candidate)

- Corrected public release status following the successful 0.1.2 TestPyPI
  upload and clean Windows regression (36 + 24 + 4 = 64 cases).
- Added GitHub homepage/repository/issues/documentation metadata and the
  planned repository URL to the citation file.
- Updated README, release and Windows publishing guidance to remove stale
  unpublished/private-license claims.
- **No changes to numerical kernels, equations, calibration or archived CSV
  reference data.** Version/metadata-only change in Python package code.

## 0.1.2 — 2026-11-10 (public TestPyPI release)

- Published wheel and source distribution at
  https://test.pypi.org/project/contactimpactbench/0.1.2/.
- Verified in independent Windows venv (Python 3.14.3; NumPy 2.5.4;
  SciPy 1.18.1): dependency check and 64/64 regression pass.
- Added the MIT license, contributor attribution, `CITATION.cff`, build
  metadata, Windows instructions, and CI workflow source.

## 0.1.1 — private research release

- Reproducibility tools, environment report and archived regression suite.
