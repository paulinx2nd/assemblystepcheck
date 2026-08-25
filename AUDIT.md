# Audit Record

Audit date: 2026-08-25

## Automated results

- GenVM lint and SDK validation: PASS
- Strict Pyright through genvm-lint: PASS
- Direct-mode tests: 7 PASS
- Five-validator GLSim integration: 1 PASS
- ABI regenerated from final source: PASS
- Pinned runner header: PASS
- Dependency vulnerability audit: PASS, zero known vulnerabilities
- Full-workspace structural originality scan: PASS, 121 contracts scanned; every nearest external match is below 0.35 and has a different public method shape
- StudioNet: PASS - fresh owner-isolated wallets, all transactions finalized and executed successfully, deployed source/schema matched, and mechanism-specific bound state read back
- GitHub publication: PASS - private remote and clean one-commit reachable history verified

## Artifact hashes

- Source: `7328dbf8f7fa2c68d4af481e63a359161956235ee2f3d272a698d536220981a3`
- ABI: `1e2c4f64d38dfd088646a8c722ade691c3733de945663b2660238469f184854d`

## Manual findings

The substantive validator independently reruns the task. The contract documents caller-attested source limitations, public-data exposure, role boundaries, terminal states, and residual risk. Its primitive is a prerequisite-unlock workflow with two-stage evidence acceptance and a content-bound verification chain. The StudioNet manifest records the contract address, transaction receipts, fresh public test roles, exact source and schema readback, and the mechanism-specific terminal assertion.
