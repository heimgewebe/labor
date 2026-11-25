---
title: "Model-Lab Replication Series — In-place Archive Decision"
status: archived
canonicality: derived
created: "2026-11-25"
triggered_by: "github:heimgewebe/bureau#2290; github:heimgewebe/bureau#442"
---

# Model-Lab Replication Series — In-place Archive Decision

The historical series is closed without a comparative result or adoption decision. Its
manifest now says `inconclusive` (administrative terminal disposition; no new result
assessment). Runs 001–003 retain their original execution and evidence qualifications.
Run-003 runtime verification remains partial and independent model/tool attestation was
not established. Run-004 was prepared but never executed or authorized; its remaining
blockers and all frozen artifacts remain exactly as recorded. No effect, model-quality,
promotion, runtime, sandbox or production-readiness claim is upgraded.

## Why the archive stays at its original path

The active register is empty. A targeted search of Labor, Bureau, Grabowski,
Systemkatalog, Claim-Audit-Lab, RepoGround and Heim-PC found no current external
execution consumer for the Run-004-specific validators; the Bureau hit is a discovery
inventory, not a runtime dependency (Grabowski task
`ba767c00796649e7b36ae47f`). This is bounded consumer evidence, not a proof about
every possible external repository. A real consumer has not requested continuation.
The series remains valuable as historical evidence for the generic AP-1/AP-2 and
claim/evidence checks.

A disposable path-move probe (`799ba8a1dbbf45a380507ece`) failed because frozen
repo-local evidence references resolve to the original paths. A Git-pointer-only
archive probe (`0e9a03dc75e9430cb11c10c5`) failed because the generic challenge-version
regression expects a real opt-in decision. Moving or rewriting frozen bytes, adding
path aliases, or weakening generic checks would impose needless maintenance.

The exact pre-closure commit is [`1c8f70257a05be65cde2f486232752f58827a5cf`](https://github.com/heimgewebe/labor/tree/1c8f70257a05be65cde2f486232752f58827a5cf/experiments/2026-05-31_model-lab-replication-series),
experiment subtree `7974194fdf139a4515f6793df9d4ce2e740cf90d`. All 135 original
tracked files are retained at their existing paths; only the manifest lifecycle status
and update date change. The original manifest remains available at the pinned commit.
This path-bound pre-registration legacy series is archived in place, not a new archive
mechanism for registered v2 experiments. The existing active-registry validator rejects
its terminal manifest. Future experiments need a new current consumer, decision and
registration; do not restart this series by relabeling its historical manifest.

## Retired routine checks

The nine specialist fixture-test Make targets below are removed from routine local and
CI validation, not their implementation files or fixtures. Their real artifact checks
remain blocking, as do the generic AP-1/AP-2, claim/evidence, runtime-evidence,
result-assessment, registration, replay and other retained checks. There is no new
conditional routing or replacement gate.

- `validate-model-lab-next-blocker-triage-tests`
- `validate-model-lab-condition-contrast-design-gate-tests`
- `validate-model-lab-condition-design-tests`
- `validate-model-lab-access-policy-tests`
- `validate-model-lab-runtime-binding-tests`
- `validate-model-lab-runtime-candidate-tests`
- `validate-model-lab-execution-readiness-tests`
- `validate-model-lab-execution-seed-tests`
- `validate-model-lab-workspace-isolation-tests`


For an exact historical replay, create a disposable checkout of the pinned commit and
run its original `make validate-legacy` with the documented Python dependencies.
That replay verifies the archived contract, not current sandbox availability or
permission to execute Run-004. For maintenance of the surviving specialist validators,
run the corresponding existing Python regression scripts explicitly. No changes to the
archived evidence or validator code are required by this retirement.
