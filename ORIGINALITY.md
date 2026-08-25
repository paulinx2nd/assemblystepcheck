# Originality

## Mechanism fingerprint

Its primitive is a prerequisite-unlock workflow with two-stage evidence acceptance and a content-bound verification chain.

Lifecycle: publish topological plan -> start build -> submit unlocked step -> consensus screening -> verifier accept or rework -> hash-chain closure.

Consensus boundary: Validators agree whether each public evidence submission is ready for a human verifier or requires rework.

Settlement boundary: Only prerequisite-complete steps unlock; verifier acceptance advances the verified mask and chain head, while rejection returns the step to rework.

## Review-cohort defense

Names, prompts, labels, and method names are not the basis of the distinction. The actor topology, stored state, allowed transitions, validator decision, and deterministic settlement described above are the reusable mechanism. A full-workspace structural scan is run before publication; its JSON report is retained outside the repository-wide source tree and summarized in `AUDIT.md` after the final pass.
