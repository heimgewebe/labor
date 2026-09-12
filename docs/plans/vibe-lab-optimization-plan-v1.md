---
title: "Labor Optimization Plan v1"
status: active
canonicality: operative
created: "2026-07-12"
updated: "2026-09-12"
triggered_by: "github:heimgewebe/bureau#2289; conversation:user-request-2026-09-12-labor-zero-to-decision"
origin_triggered_by: "user-request-2026-07-12"
---

# Labor Optimization Plan v1

## Decision

Labor is a small experiment and decision-support surface. It may register a prospective comparison, validate evidence identity, capture bounded observations, evaluate a bounded effect and close with a reviewed decision. It must not become a scheduler, dashboard, runtime service, routing authority, second Bureau or second Grabowski governor.

The primary optimization objective is now **decision yield per handling and durable surface cost**, not surface reduction by itself. Surface reduction remains a constraint and a simplification tool, not the mission.

Working heuristic, using existing evidence rather than a new metrics platform:

- `decision_yield` = relevant reviewed decisions / started experiments;
- `handling_cost` = human plus machine effort from registration to reviewed decision;
- `surface_cost` = durable special contracts, validators, artifacts and maintenance obligations left behind;
- Labor value is improved when decision yield rises without handling or surface cost growing faster.

These terms are decision aids, not a new scoring authority. If they would require a service, database or standing metrics subsystem, stop rather than build one.

## Verified current state

As of 2026-09-12:

- `experiments/active.v1.json` is empty after the only active Outcome-Bound activation pilot reached its 2026-09-07 review boundary without an executable pre-existing slot-capture provider; the experiment remains `not_executed` and closes this revision with `defer`;
- earlier Chronik, operator-routing, RepoBrief, PR-context, rLens agent-context, Model-Lab and Operator-Lab work remains historical evidence and is not active merely because validators or files still exist;
- natural-case admission, generic observation capture and deterministic evaluation are review tooling only; admission now accepts any current valid `registration.v2.json` instead of being hard-bound to the archived Chronik experiment, while the registration authority boundary and create-only evidence semantics remain fail-closed;
- custom agent profiles and instruction-bearing Cursor/Copilot projections are retired, while generated compatibility markers and their blocking parity contracts remain active;
- the validator inventory contains 89 classified validation targets: 45 core, 6 active-group and 38 legacy, plus two supplemental checks; the archived routing-readiness test frontdoor, the two Phase-1c archive frontdoors and the four dedicated frontdoors of the never-executed PR-context and rLens agent-context designs are no longer blocking, while the six active-group targets retain current registry/registration or frozen Operator-Lab consumers;
- the active prompt-length-control library claim has been narrowed to the observed single-task evidence; its proposed cognitive mechanism and cross-task transfer remain unproven;
- no Labor surface has runtime, queue, merge, deploy, routing or policy authority.

## Completed slices

1. **Close Operator-Lab.** A deterministic cross-run assessment exposed missing metadata, missing timing and lack of comparable control/treatment groups. Anecdotal run-card growth is frozen.
2. **Make active work explicit.** `experiments/active.v1.json` is the bounded active-work truth with a maximum of five entries.
3. **Introduce prospective registration.** New experiments require consumer, decision target, control, treatment, primary metric, material threshold, comparability constraints, review date, expiry and closure outcomes.
4. **Build generic capture and evaluation tooling.** Observation capture is evidence- and registration-bound, atomic, deduplicated and expiry-aware. The evaluator reports comparability, uncertainty, effort and non-claims.
5. **Consolidate validation.** The current inventory classifies 89 validation targets behind core, active and legacy frontdoors plus two supplemental checks; GitHub exposes a smaller CI presentation, and terminal historical frontdoors are retired only when their evidence remains reproducible or generic core coverage is proven.
6. **Archive the blocked evaluator pilot.** No synthetic or retrospective pilots were manufactured after the registered intervention proved causally non-executable.
7. **Bind active lifecycle truth.** Active entries now point only to the canonical decision file. Registered entries must exactly match registration consumer, decision question, primary metric, review date and expiry; pre-registration experiments remain explicit grandfathered cases.

## Canonical zero-to-decision path

Labor's normal product path is deliberately file-backed and boring:

1. **register** — create one current `registration.v2.json` with a confirmed external consumer, decision question, control/treatment, primary metric, cost metric, stop/review/expiry rules and reviewed closure mapping;
2. **activate** — add exactly one coherent entry to `experiments/active.v1.json`; the registry stays the bounded active truth;
3. **admit** — before planning or execution, publish each eligible natural-case record create-only with `tools/vibe-cli/admit_natural_case.py --registration ... --request ...`; the writer derives `<experiment>/artifacts/admissions` by default and has no task or runtime authority; downstream capture/evaluation recompute the record’s registration, request, assignment and review commitments before trusting it;
4. **observe** — append evidence-bound measurements through `tools/vibe-cli/capture_effect_observation.py`;
5. **evaluate** — deterministically compute the registered comparison with `tools/vibe-cli/evaluate_effect.py`;
6. **decide** — a reviewer records the current canonical `results/decision.yml` (or the explicitly bound current `pN/decision.yml` where an existing phased experiment requires it); evaluation never changes policy automatically;
7. **archive** — after the reviewed decision, remove the experiment from `active.v1.json` and preserve the immutable evidence/decision under the registered archive path through ordinary reviewed Git history.

The intended minimum durable experiment surface is one registration, one active-registry binding while running, one evidence stream and one canonical decision. Admission receipts are case evidence, not a second state system. No wrapper, database or workflow engine is justified until a real run proves that the remaining manual ceremony costs more than the wrapper would permanently add.

## Current decision gate

No new Labor service, agent profile, instruction-bearing projection target, specialist validator or effect-analysis feature should be added merely because the active registry is now empty. The next experiment must first name a current external consumer, a concrete decision, an already-executable observation path, a cost budget and a stop rule.

The Outcome-Bound activation revision reached its review boundary on 2026-09-07 without activation. Fresh deployed-runtime inspection still did not prove the frozen provider contract, so this revision is deferred rather than extended or rescued by new provider development.

The former RepoBrief Workbench, Chronik and routing-readiness experiments remain historical. RepoGround is the current cited repository-context organ and requires its own prospective utility decision if Labor evidence is ever needed.

## Survivor / retirement disposition

The broad survivor phase is largely complete. Remaining retirement work is subordinate to current decision utility and proceeds only when consumer, coverage and archive evidence prove a net simplification.

### Keep

- active experiment registry;
- prospective registration schemas;
- generic evidence-, claim-, relation- and promotion-integrity checks;
- evidence-bound observation capture;
- deterministic review-only evaluation;
- reviewed decisions and immutable archive records;
- generated compatibility markers while their operative contracts remain active.

### Retired or archived

- active custom-agent instruction layer;
- instruction-bearing Cursor/Copilot projection content;
- the frozen 36-card Operator-Lab series and its four dedicated run-card/metrics blocking frontdoors; historical scripts/tests remain for manual audit while the deterministic closeout stays blocking from the archive;
- the blocked operator-intervention evaluator experiment;
- the never-executed rLens agent-context and PR-context designs and their dedicated blocking frontdoors;
- any implied Heimlern, dashboard, Plexer, routing or runtime integration.

### Review for removal

The 38 remaining legacy targets remain blocking only until their protected family is archived or equivalent generic coverage is demonstrated. Review order:

1. retired agent-handoff, agent-command and command-chain contracts;
2. Model-Lab specialist validators only after a separate terminal disposition; the current manifest remains `testing`, Run-004 is not authorized/executed, and all Model-Lab guards therefore remain blocking;
3. historical replay and fixture semantics already covered by generic schema, relation, run-bundle and claim/evidence gates;
4. the never-executed PR-context and rLens agent-context designs are archived and their dedicated blocking frontdoors retired; any remaining historical specialist surface still requires separate current-consumer or archive evidence.

Each reduction slice must identify the protected failure class, prove archive or equivalent generic coverage, remove more permanent surface than it adds, and keep current active evidence integrity intact.

## Operating target

The legacy review date of 2026-09-01 has passed. Of the earlier 48-target baseline, 38 blocking legacy targets remain after the Operator-Lab and PR-context archive reductions. Every further target must still receive one of three dispositions: `retain_with_consumer`, `covered_by_core` or `retire`; no numeric reduction target authorizes deletion without proof.

For new work, the stronger success signal is a reviewed external decision reached with low handling cost and little new durable surface. A run that produces no admissible decision is a valid terminal result when the admission rule was prospective and the reason is recorded rather than repaired after the fact.

## Library consumer audit

Catalog entries, prompts, benchmarks and instruction blocks are active library surfaces only when an external consumer, decision target and review rule are named. Unconsumed artifacts remain historical records and must not justify new instruction-bearing exports or compatibility layers by themselves.

## Stop rules

Stop or remove an optimization slice if it requires a new service, database, dashboard, LLM-based pattern detector, automatic Bureau mutation, automatic routing change, synthetic productive mutations, retrospective metric invention or more specialist validators than it removes.

## Organ boundaries

- Grabowski owns execution and typed receipts.
- GitHub and CI own code, review, merge and check truth.
- RepoGround supplies cited, commit-bound repository context.
- Bureau owns task and promotion decisions.
- Chronik may own longitudinal append-only history when needed.
- Labor owns bounded prospective experiment design, evidence binding and reviewed closure only.
