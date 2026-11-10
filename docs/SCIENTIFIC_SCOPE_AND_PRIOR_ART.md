# Scientific scope and contribution boundary

**Purpose**: narrow, reproducible reduced-contact verification benchmarks.

The suite is not a new general-purpose contact dynamics solver and does not
claim accurate physical predictions for a pressurized hyperelastic shell.

## Distinguishing uses

1. One command replays a known reduced 3D tangential viscoelastic impact case
   and reports force, moment and discrete energy diagnostics.
2. An independently event-resolved normal reference allows numerical-method
   comparisons for exactly the same pressure-dependent normal force law.
3. Analytical and quadrature limits compare a prescribed circular friction
   patch with a reduced friction ellipsoid.
4. A known algorithmic energy-gain case is preserved as a *negative* fixture,
   demonstrating that total energy loss over an impact does not imply
   nonincrease on every discrete step.

These are **usability and reproducibility features**. We have not proved they
are unavailable in existing open packages. Before a SoftwareX submission,
show concrete comparison tasks against at least one established environment
(e.g. Siconos or Chrono) without claiming superiority based only on a smaller
scope or a simpler CLI.

## Verification hierarchy

- Analytic identities and local constitutive tests: verify formulas/limits.
- Exact archived-CSV regression: verify repeatability of one implementation.
- Independent normal solver DOP853: verifies **normal subsystem numerics only**.
- Independent experiment or fully resolved distributed shell contact: **absent**.

## Known exclusions

N3.7 and JM–3D contact patch simulations are not exported as validated
prediction APIs due to unresolved mesh sensitivity and material-memory
questions. Their development findings can be cited as limitations but may not
be used as numerical ground truth.

## Candidate paper format

If external gates pass, a SoftwareX paper should focus on reusability,
software architecture, documentation and narrowly verified examples.
It must include an available open-source distribution and licence, after
rights and contributor approvals. Do not reuse claims of new physical
laws from the rejected multibody impact manuscript.
