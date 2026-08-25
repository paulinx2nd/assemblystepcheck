# Reviewer Guide

## Mechanism in one sentence

A reusable assembly prerequisite graph where builder evidence is screened by validators, accepted by a distinct verifier, and folded into an ordered hash chain before closure.

## What consensus actually decides

Validators agree whether each public evidence submission is ready for a human verifier or requires rework.

## What code settles afterward

Only prerequisite-complete steps unlock; verifier acceptance advances the verified mask and chain head, while rejection returns the step to rework.

## Why this is distinct

Its primitive is a prerequisite-unlock workflow with two-stage evidence acceptance and a content-bound verification chain.

## Fast review path

1. Confirm the pinned dependency on the first source line.
2. Inspect the custom validator and verify it reruns the substantive task.
3. Trace role checks and terminal-state guards in each write method.
4. Run lint, strict type checking, seven direct tests, and the five-validator integration test.
5. Compare `abi.json` and the StudioNet manifest to the committed source hash.

## Known limitations

The protocol does not inspect the physical assembly or certify safety. A verifier wallet is not an authenticated professional credential.
