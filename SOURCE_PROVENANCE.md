# Source Provenance

## Collection behavior

No web collection occurs. Instructions, subject description, builder evidence, and verifier notes are public caller-attested data.

The contract performs no live web request, does not scrape a page, and does not silently claim that a label or URL authenticates its publisher. This avoids validator drift from changing pages. If an application needs live retrieval, that retrieval belongs in a separately reviewed mechanism whose validators independently fetch and normalize the same source.

## Integrity bindings

- Contract source SHA-256: `7328dbf8f7fa2c68d4af481e63a359161956235ee2f3d272a698d536220981a3`
- ABI SHA-256: `1e2c4f64d38dfd088646a8c722ade691c3733de945663b2660238469f184854d`
- Frozen text and canonical JSON records are hashed inside the contract where the workflow needs a content binding.
- Human-readable source references, when present, are expressly marked unverified.

## Fixture policy

Tests use synthetic public fixtures written for this repository. They are not copied production records and do not represent real people.
