# Architecture

## Boundary

- Frontend or backend: wallet UX, indexing, private drafts, non-authoritative previews, notifications, and optional off-chain source retrieval.
- GenLayer contract: Validators agree whether each public evidence submission is ready for a human verifier or requires rework. Only prerequisite-complete steps unlock; verifier acceptance advances the verified mask and chain head, while rejection returns the step to rework.
- External world: No web collection occurs. Instructions, subject description, builder evidence, and verifier notes are public caller-attested data.

## Event path

publish topological plan -> start build -> submit unlocked step -> consensus screening -> verifier accept or rework -> hash-chain closure

## Actors

- plan designer
- builder
- distinct verifier
- GenLayer validators

## Consensus design

The leader produces a normalized bounded result. Each validator independently reruns the substantive task from the same frozen public inputs. Validators compare the decision fields that change state, not merely JSON shape. Invalid model output raises `[LLM_ERROR]` so a broken leader is not accepted.

## Deterministic layer

Only prerequisite-complete steps unlock; verifier acceptance advances the verified mask and chain head, while rejection returns the step to rework. Identifiers, bounds, access checks, ordering, counters, masks, hashes, and terminal-state guards are computed deterministically.

## Persistence

State uses GenLayer storage types only. Public composite records are serialized as canonical JSON where appropriate. Source SHA-256 at evidence generation: `7328dbf8f7fa2c68d4af481e63a359161956235ee2f3d272a698d536220981a3`.
