---
title: "Archive Decision: rLens Agent Context Conditions"
status: archived
canonicality: operative
triggered_by: "github:heimgewebe/bureau#442; conversation:user-request-2026-09-08-continue-labor-survivor-audit"
---

# Archive decision

## Finding

The historical rLens agent-context condition design remains valid as a measurement-plan and guard seed. It never became an executed comparison: the frozen manifest remains `status: designed`, `execution_status: designed`, and has no `execution_refs`; the preserved `results/decision.yml` records `verdict: not_executed`, zero observations and zero documented runs.

## Why it leaves the live experiment surface

The original Bureau consumer `BUR-2026-002-T005` is verified, but its verified outcome explicitly covers only the design and guard seed delivered in the historical implementation. It does not establish an outstanding current request to execute the condition comparison. The current Labor active registry is empty, and the current canonical Bureau control surface contains no newer external consumer bound to this historical experiment.

Rebinding the July design after the fact to the generic Labor experiment gate, RepoGround, or another current organ would change the consumer and decision context after the measurement design was created. This archive therefore does not invent a successor consumer.

## Disposition

- Preserve the complete experiment bundle under `experiments/_archive/2026-07-08_rlens-agent-context-conditions/`.
- Preserve the historical `results/decision.yml` unchanged.
- Retire the two rLens-condition-only validator targets from the blocking `validate-legacy` frontdoor and validator inventory.
- Keep `scripts/docmeta/validate_rlens_agent_context_conditions.py` and its regression tests as historical audit tools; they are no longer blocking CI frontdoors.
- Any future question about rLens, RepoGround or agent-context effectiveness requires a new prospective, current-consumer-bound experiment rather than replaying this stale design.

## Evidence

- Historical consumer task: `bureau:BUR-2026-002-T005` — verified as design/guard seed only.
- Preserved decision: `results/decision.yml` — `not_executed`, observations `0`, runs documented `0`.
- Labor active registry at archive review: empty.
- Dedicated frontdoor runtime before retirement was approximately 0.16 seconds locally; runtime saving is incidental, not the justification for retirement.

## Non-claims

This archive does not prove that rLens is ineffective, that any current RepoGround context surface is useful or useless, or that another legacy validator family is safe to retire. It does not modify Model-Lab, Outcome-Evidence, PR-Context, Agent-Handoff, Command-Chain or Replay evidence and guards.
