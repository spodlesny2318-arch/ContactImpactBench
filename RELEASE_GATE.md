# ContactImpactBench 0.1.3 — publication gate

## Evidence already obtained for **0.1.2**

- Both wheel and source distribution were accepted on public TestPyPI:
  https://test.pypi.org/project/contactimpactbench/0.1.2/.
- User-reported Windows AMD64 / Python 3.14.3 / NumPy 2.5.4 / SciPy 1.18.1:
  `pip check` clean and full regression **64/64** (36 + 24 + 4).
- `twine check` passed for both 0.1.2 distribution files.
- This is numerical regression, not experimental physical validation.

## Requirements before 0.1.3 main-PyPI upload

- [ ] Public GitHub source successfully pushed; check README, License,
  metadata and provenance files in the browser.
- [ ] GitHub Actions tests passed on configured platforms, or disclose any
  unavailable CI configuration with corresponding local verification.
- [ ] Install **0.1.3** in a clean environment and pass both pytest and
  64-case full regression.
- [ ] Build wheel and source distribution from **this source tree**;
  run `twine check dist/*` for 0.1.3 and inspect the metadata.
- [ ] Verify author/license attribution and ensure no secret tokens, passwords,
  private folders or test logs with personally identifying paths are committed.
- [ ] Confirm registry package-name availability and project ownership on
  the **main** PyPI (TestPyPI is a separate service).
- [ ] Upload to main PyPI once; distributions cannot be overwritten with the
  same names. Verify fresh-index installation, `pip check` and regression.
- [ ] Tag Git commit and publish a release; prepare archival DOI and precise
  citation metadata if pursuing a SoftwareX submission.

Do not claim that repository publication or PyPI distribution implies an
accepted paper or experimental validation of inflated-shell impact.
