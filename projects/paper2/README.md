# Paper II — controlled evidence intake

**Status:** infrastructure only. No original spectra, unpublished manuscript, or
third-party PhotochemCAD data have been imported into this public repository.

## Evidence intake protocol

1. Preserve the authoritative local manuscript and original input bytes.
2. Confirm publication/distribution rights for every input file before committing it.
3. Record source URI, bibliographic citation, solvent, units, measurement type,
   processing steps, and the exact SHA-256 of each original input.
4. Keep original measured data separate from derived normalized comparison metrics.
5. Run G3 to screen physical claims, G4 on the actual local spectra, and G6 on
   a traceable evidence register. A synthetic CI PASS is **not** a data-validation PASS.
6. Link each quantitative manuscript claim to an evidence record, analysis version,
   conditions, limitations, and a manuscript section or figure.
7. Release only after independent scientific review and G7 publication checks.

## Public-repository boundaries

The directory `private/`, raw input directories, manuscripts, and generated
reports are intentionally ignored by this subproject. Do not upload licensed
datasets or unpublished manuscript content without explicit authorization.

## Scientific boundary

Two normalized chlorophyll absorption spectra can support a comparison of
**absorption spectral shapes under stated conditions**. They cannot establish
optical gain, laser threshold, stimulated emission, or laser suitability on
their own. Pearson correlation is not a repeatability or uncertainty estimate.

## Current gates

- G3: physical evidence eligibility, synthetic tests in CI
- G4: interpolation/normalization sensitivity, synthetic tests in CI
- G6: claim–source–method–condition–result traceability, synthetic tests in CI
- G1/G2/G5/G7: full CI integration pending authoritative inputs and checks

A G6 metadata PASS confirms required fields are present, not that hashes were
verified against original bytes or that the scientific results are correct.
