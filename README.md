# AssemblyStepCheck

A reusable assembly prerequisite graph where builder evidence is screened by validators, accepted by a distinct verifier, and folded into an ordered hash chain before closure.

## Why GenLayer

Validators agree whether each public evidence submission is ready for a human verifier or requires rework. Only prerequisite-complete steps unlock; verifier acceptance advances the verified mask and chain head, while rejection returns the step to rework.

## Roles

- plan designer
- builder
- distinct verifier
- GenLayer validators

## Lifecycle

publish topological plan -> start build -> submit unlocked step -> consensus screening -> verifier accept or rework -> hash-chain closure

## Contract interface

- Constructor: none
- Write methods: abort_build, close_build, publish_plan, start_build, submit_step, verify_step
- View methods: get_build, get_build_count, get_build_id, get_plan, get_plan_count, get_plan_id
- Runner: `py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6`

## Public-data warning

All contract inputs, evidence, notes, addresses, model results, and state are public. Do not submit secrets, private documents, personal contact information, or confidential identifiers.

## Source model

No web collection occurs. Instructions, subject description, builder evidence, and verifier notes are public caller-attested data.

## Verification

```text
genvm-lint check contracts/assembly_step_check.py
genvm-lint typecheck contracts/assembly_step_check.py --strict
python -m pytest tests/direct -q
python tests/run_glsim.py --port 4000 --validators 5 --no-browser
python -m pytest tests/integration -q -s
```

The repository contains seven direct tests and one full five-validator GLSim flow. StudioNet evidence is recorded separately under `deployments/` after network execution.

## Limitations

The protocol does not inspect the physical assembly or certify safety. A verifier wallet is not an authenticated professional credential.

Licensed under MIT. See `LICENSE`.
