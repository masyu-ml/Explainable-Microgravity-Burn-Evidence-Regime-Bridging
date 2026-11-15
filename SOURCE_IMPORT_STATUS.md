# Source import and verification status — 15 November 2026

## Current GitHub repository

The current `main` branch contains the project overview, expanded README, formal architecture, mathematical methodology, NASA data-provenance notes, interactive documentation, a **synthetic** Gower demonstration, its unit tests, and a CI check. The main branch **does not yet contain the full EMBER backend or NASA data-ingestion source**.

## Independently recovered code archive

The separately prepared `EMBER_GitHub_Repository_Prepared_2026-11-15.zip` contains **84 entries** (approximately 2.42 MB uncompressed), including:

- `research_core/`: historical V2 FastAPI research core, model router, six physics families, Gower retrieval, Bayesian models, inverse design, source data, and tests.
- `evidence_pipeline/`: archived BASS-II V5 normalization, evidence-ledger data, NASA source parser material, and tests.
- `legacy_console/`: self-contained older v1.3 dashboard **not** equivalent to the currently deployed site.
- Documentation, interactive explainer, example configuration, source manifests, contribution/security notes, and CI files.

**Audited locally:** 14/14 archived scientific-core unit tests and 13/13 evidence-pipeline tests passed when run from their own working directories. Python bytecode compilation completed successfully. A basic pattern scan found no known key/token strings and no ChatGPT/Claude/OpenAI/Copilot remarks inside archived code files. These checks neither guarantee the absence of secrets nor independently validate combustion physics.

## Next source upload

Extract the prepared archive locally and import **only the missing source directories** first:

```text
research_core/
evidence_pipeline/
legacy_console/
SOURCE_MANIFEST.sha256
```

Preserve the current GitHub README, documentation, interactive explainer, tested Gower example and its workflow instead of overwriting them with older snapshot copies. Review `research_core/models/` and evidence files for rights, size and provenance before publishing. Add any new historical CI workflow only after confirming its dependency setup.

### Test the imported code

```bash
python -m pip install -r research_core/requirements.txt
cd research_core
python -m pytest -q tests/test_v2_scientific.py
cd ../evidence_pipeline
python -m pytest -q test_evidence.py
```

## Version limitation

These are **historical recovered sources**. The current Vercel application has more recent scientific, UI, voice and source-adjudication layers (V12–V29), which are **not reconstructed or falsely represented as present** in the recovered package.

The deployed website at https://ember-mvp-one-man-orbit.vercel.app/ remains unchanged by this repository publication. Physical experiments, real measurement verification and independent safety certification are separate from these software test results.
