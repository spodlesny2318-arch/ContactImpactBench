# ContactImpactBench 0.1.3

**Reproducible numerical-verification benchmarks for reduced compliant-impact and frictional-contact models.**

[Source code](https://github.com/spodlesny2318-arch/ContactImpactBench) ·
[TestPyPI 0.1.2](https://test.pypi.org/project/contactimpactbench/0.1.2/) ·
[MIT License](LICENSE) · [CITATION.cff](CITATION.cff)

ContactImpactBench is a small Python research-software toolkit derived from
archived N3.3, N3.4 and N3.6 studies. It supplies reproducible numerical
models, independent-in-time-integration normal-contact comparisons, prescribed
pressure-patch friction calculations, and reference regression fixtures.
**It does not provide an experimentally validated prediction of impact of a
real inflated hyperelastic shell.**

## Installation

Requires Python >= 3.10 and compatible NumPy/SciPy releases.

**Current verified public release:** version `0.1.2` on TestPyPI (wheel and
source distribution). To install it into a new environment, obtain NumPy and
SciPy from PyPI and the ContactImpactBench package from TestPyPI:

```bash
python -m pip install numpy scipy
python -m pip install --no-deps --index-url https://test.pypi.org/simple/ contactimpactbench==0.1.2
python -m pip check
python -m contactimpactbench verify --full
```

**From this repository's source tree (0.1.3):**

```bash
python -m pip install -e '.[test]'
python -m pytest -q
python -m contactimpactbench verify --full
```

**After version 0.1.3 has been published to the main PyPI index:**

```bash
python -m pip install contactimpactbench==0.1.3
```

These are separate distribution channels: version 0.1.3 is not represented
here as already published to PyPI. On Windows use a virtual environment and
its `Scripts\python.exe` as explained in
[reproducibility instructions](docs/REPRODUCIBILITY.md).

## Main commands

```bash
python -m contactimpactbench impact --spin 20
python -m contactimpactbench normal --pressure-psi 8
python -m contactimpactbench friction --q 1 --alpha 0
python -m contactimpactbench verify --full
python -m contactimpactbench env
```

The commands print JSON or accept `--output FILE.json`. For an auditable local
report, run `python tools/verification_record.py --output local_verification.json --full`.
Check generated reports for personal filesystem paths before sharing them.

## Scientific scope and limitations

- **N3.3:** reduced spatial oblique impact with Kelvin-type tangential memory,
  coupled sliding/drilling-spin friction and a phenomenological normal law.
- **N3.4:** separately event-resolved DOP853 **normal-only** integration for
  the **same** normal law, an independent integration-method check rather than
  independent physical validation.
- **N3.6:** distributed friction for a circular gross-slip patch under
  **prescribed** radial pressure, with analytical limits and quadrature.
- **N3.1 negative fixture:** known energy-inconsistent legacy algorithm;
  provided as an explicit failure example, not as a valid physics prediction.

The full N3.7 / JM–3D shell code is excluded because trustworthy convergence
of local contact area and pressure has not been demonstrated. The archived
**64-case regression** (N3.3: 36, N3.4: 24, N3.6: 4) checks numerical
reproducibility against stored results, **not accuracy against experiments**.

## Verification status

- 0.1.2 was uploaded to public TestPyPI (wheel + sdist) on 2026-11-10.
- The user verified a clean Windows/Python 3.14.3 TestPyPI installation:
  NumPy 2.5.4, SciPy 1.18.1, `pip check` clean, full regression **64/64**.
- 0.1.3 changes release metadata and documentation; it is a new source
  candidate until its own local/CI tests and subsequent distribution checks
  are completed. A passing regression is not experimental validation.

## Project documentation

- [API reference](docs/API_REFERENCE.md)
- [Reproducibility](docs/REPRODUCIBILITY.md)
- [Scientific scope and prior art](docs/SCIENTIFIC_SCOPE_AND_PRIOR_ART.md)
- [Release checklist](RELEASE_GATE.md)
- [Windows publication instructions](docs/PUBLISHING_WINDOWS_RU.md)
- [Changelog](CHANGELOG.md)
- [Citable software authors](CITATION.cff)
- [Provenance hashes](provenance/SOURCES_SHA256.csv)

## License and citation

Copyright (c) 2026 Serhii Podliesnyi and contributors. Distributed under the
[MIT License](LICENSE). For software citation metadata see [CITATION.cff](CITATION.cff).
The software is provided as-is, without any warranty or claim of experimental
validation. The GitHub repository is intended to provide publicly inspectable
source and release history; publication in an index is not journal peer review.
