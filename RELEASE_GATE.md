# ContactImpactBench v0.1.4 — author metadata correction release gate

## Scope

This is a metadata-only correction to the already verified 0.1.3 numerical
software. No computational source kernels or archived CSV benchmarks have
changed. Earlier published v0.1.3 files must remain immutable.

## Required prior to release

- [ ] Confirm `CITATION.cff`, PyPI `pyproject.toml`, `AUTHORS.md`, and Zenodo
  creators all use: Serhii Podliesnyi; Oksana Chmykhova; Bohdan Vorobiov.
- [ ] Confirm corresponding author Serhii Podliesnyi and ORCIDs.
- [ ] Ensure code/source/CSV frozen SHA-256 checks are identical to v0.1.3.
- [ ] Confirm local 23 pytest checks plus complete archived 64-case regression.
- [ ] Push changes to main and confirm 4/4 jobs in GitHub Actions.
- [ ] Build wheel and sdist for **0.1.4**, check with Twine, and test wheel
  from a new virtual environment (never overwrite any 0.1.3 files).
- [ ] Create Git tag and Release `v0.1.4` only after these gates pass.
- [ ] Publish to main PyPI and verify clean index installation.
- [ ] Upload **v0.1.4** source snapshot, not v0.1.3, into the unpublished
  Zenodo draft. Verify creators and type `Software`; only then publish DOI.

Numerical regression does not constitute experimental validation.
