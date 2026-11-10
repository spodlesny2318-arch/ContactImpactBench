# SoftwareX publication preparation — future scientific review

ContactImpactBench is intended as reusable, reproducible numerical-verification
software. **It is not an experimentally validated inflated-shell impact solver.**

## Verified engineering evidence

- Public TestPyPI version 0.1.2: wheel and source archive published.
- User-reported Windows 3.14.3 / NumPy 2.5.4 / SciPy 1.18.1:
  64/64 archived cases reproduced in a clean environment.
- MIT license, authorship and citation metadata are included.

## Remaining independent publication requirements

1. Commit current source to a public Git repository and confirm automated CI.
2. Release updated package via main PyPI with source and artifact hashes.
3. Provide a reproducible scientific use case that illustrates software utility.
4. Clearly distinguish these numerical regression tests from physical
   validation or independent contact-model verification.
5. Compare scope and demonstrated capabilities to established tools such as
   Project Chrono and Siconos without unsupported superiority claims.
6. Obtain an external usability report if possible and archive a software
   release with a persistent DOI (e.g., Zenodo), with correct code version.
7. Draft a SoftwareX manuscript aligned with verifiable public software.

The existence of an installable package is **not** evidence of SoftwareX
acceptance or proof of scientific originality.
