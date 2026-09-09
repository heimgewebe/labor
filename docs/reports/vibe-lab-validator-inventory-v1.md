---
title: "Vibe-Lab Validator Inventory v1"
status: active
canonicality: operative
created: "2026-07-12"
updated: "2026-09-09"
triggered_by: "github:heimgewebe/bureau#442; conversation:user-request-2026-09-09-continue-labor-survivor-audit"
origin_triggered_by: "vibe-lab-optimization-plan-v1-phase-c"
relations:
  - type: informs
    target: ../plans/vibe-lab-optimization-plan-v1.md
---

# Labor Validator Inventory v1

## Current result

The current machine-readable source is `.vibe/validator-inventory.v1.json`. After the operator-intervention effect-evaluator experiment was archived, the effect-evaluator test target moved from the active group into the generic core group.

| Group | Targets | Current consumer |
| --- | ---: | --- |
| Core | 45 | Repository contracts, generic evidence integrity and every experiment |
| Active | 6 | Active registry, prospective registration and frozen Operator-Lab closeout |
| Legacy | 38 | Grandfathered historical experiments, retired agent-operability corpus and closed specialist families |
| Supplemental | 2 | Replay non-mutation and committed generated artifacts |

The grouped inventory therefore contains 89 classified validation targets plus two supplemental checks. GitHub exposes a compact grouped frontdoor while all groups remain blocking on pull requests and `main`.

The active experiment registry is currently empty. The six targets in the inventory group named `active` therefore must not be read as six active experiments: they protect active-registry/registration boundaries plus the frozen Operator-Lab closeout. The archived routing-readiness regression frontdoor is no longer part of current blocking validation; its scripts and evidence remain historical. Former Chronik, RepoBrief and routing-readiness experiment files remain historical evidence.

## Correction of the previous report

The earlier report was internally inconsistent after the routing-readiness work: its current-state section correctly named three active experiments and 11 active targets, while its practical-effect section still claimed two experiments and 10 targets. This revision removes that drift. It also archives the former RepoBrief pilot after its named consumer completed and retires the four pilot-only blocking targets without deleting the historical scripts or evidence.

## Safety boundary

Classification is not a usefulness claim. In particular:

- 38 legacy targets are not presumed useful forever;
- historical evidence retention does not require every historical specialist validator to remain permanently blocking;
- a green validator proves its encoded contract, not practical workflow benefit;
- full CI does not give Labor runtime, routing, queue, merge, deployment or policy authority.

Every new `validate-*` target must be classified. The inventory validator fails when:

- a target is unclassified or listed twice;
- Makefile group dependencies drift from the inventory;
- the active specialist budget exceeds 12 targets;
- GitHub bypasses the grouped frontdoor with direct validator commands;
- a referenced scope or target disappears.

The existing active-experiment validator additionally requires a canonical `results/decision.yml` source. For registered entries it enforces exact consumer, decision question, primary metric, review date and expiry coherence; missing registration is permitted only before the registration enforcement date.

## Survivor disposition

### Keep as active core

- schemas and schema counterevidence;
- execution-proof and run-bundle integrity;
- relation, claim/evidence and promotion-readiness boundaries;
- active-registry and prospective-registration integrity;
- evidence-bound observation capture and generic effect-evaluator regression tests;
- generated-artifact non-mutation and drift protection.

These surfaces have a current consumer or protect a generic failure class used by every experiment.

### Keep temporarily as active specialist surface

- active experiment registry checks;
- frozen Operator-Lab closeout checks;
- prospective experiment registration checks;

The group now contains 6 of the permitted maximum 12 targets, but the experiment registry is empty. Generic active-registry and registration checks retain a current lifecycle role; the frozen Operator-Lab closeout remains until separately proven redundant. No new specialist target is justified merely by a new idea.

### Review for retirement

The 38 remaining legacy targets are reviewed in this order:

1. retired agent-handoff, agent-command and command-chain contracts;
2. Model-Lab control, access, runtime, workspace and condition-design contracts only after a separate terminal disposition; the current manifest remains `testing`, Run-004 is not authorized/executed, and this survivor slice therefore retains all Model-Lab guards;
3. historical replay, fixture and cross-contract semantics that may duplicate generic core gates;
4. The never-executed PR-context and rLens agent-context designs are archived and their dedicated blocking frontdoors retired. Any remaining historical specialist surface still requires separate current-consumer or archive evidence.

A legacy target may move to removal only when one of these material proofs exists:

1. its protected experiment family is closed and archived and no active contract imports it; or
2. a core validator demonstrably covers the same failure class and relevant fixtures.

A head- and diff-bound review is still mandatory for the removal PR, but it verifies one of those proofs and is not an independent substitute for archive or equivalent core coverage.

## Quantitative reduction gate

The 2026-09-01 legacy review gate has passed. After the archived Operator-Lab and PR-context retirement slices, 38 blocking legacy targets remain and each future retirement slice must classify its targets as:

- `retain_with_consumer`;
- `covered_by_core`;
- `retire`.

The directional objective is a 30–50 percent reduction of the blocking legacy group. It is a review target, not permission for blind deletion.

## Practical effect

- Current active specialist surface: 6 targets instead of an undifferentiated historical frontdoor.
- Current active experiments: zero; `experiments/active.v1.json` is empty after the 2026-09-07 deferred Outcome-Bound review.
- Four RepoBrief-pilot-only blocking targets are retired from the grouped frontdoor; their scripts and historical evidence remain available for audit.
- Three additional specialist frontdoors are retired on 2026-09-07: the archived routing-readiness audit test target plus the Phase-1c archive guard and its regression-test target. Phase-1c current semantics remain covered by generic schema, run-bundle, relation and claim/evidence gates as established by commit `17a81f3`; historical scripts and fixtures are retained.
- Two rLens agent-context condition frontdoors are retired on 2026-09-08 after the July design remained `not_executed` with zero runs and no current external consumer. The complete design bundle and historical validator script/tests remain available under the archive/audit surface; this does not claim anything about current rLens or RepoGround utility.
- Two PR-context pilot frontdoors are retired on 2026-09-09 after the frozen B-vs-D pilot remained `prepared`, `execution_allowed: false` and `not_executed`, with all six task slots and three role bindings absent. Fresh organization-wide code search demonstrated only Labor-local references; all 17 pre-existing experiment files remain byte-identical under `_archive`, while the historical validator/capture tools remain available for manual audit.
- Four Operator-Lab run-card/metrics frontdoors are retired after the already frozen 36-card family moved to `experiments/_archive/`. Their scripts, regression tests and historical evidence remain available for manual audit; the deterministic `validate-operator-lab-closeout` guard remains active and blocking from the archive.
- Retired custom-agent and instruction-bearing projection content: no longer active authority; generated compatibility markers and parity contracts remain active.
- Next engineering work: reclassify now-consumerless specialist targets and remove only proven-redundant legacy groups rather than add new Labor capabilities.
