---
title: "Operator-Lab Loop — Archive Decision"
status: archived
canonicality: derived
created: "2026-09-09"
updated: "2026-09-09"
triggered_by: "heimgewebe/bureau#442"
---

# Operator-Lab Loop — Archive Decision

The 36-card Operator-Lab series was completed and frozen after its 2026-07-12 deterministic closeout with verdict `insufficient_evidence`. This change moves the existing family to `experiments/_archive/2026-07-01_operator-lab-loop/` without rewriting its historical cards, manifests, result records or missing-data history.

The deterministic cross-run closeout remains active and blocking from the archive. The four dedicated run-card/metrics Make frontdoors are retired because the family is no longer an active write surface; their Python scripts and regression tests remain available for manual historical audit.

Missing `run_meta.json` records and unmeasured task-completion times are intentionally not reconstructed. The archive does not upgrade the evidence and does not establish Operator-Lab effectiveness, condition superiority, causal effect or workflow-adoption readiness.

Any future operator-process experiment requires a new prospective registration with an external consumer and decision target, control/treatment definition, primary metric, material-effect threshold, review date, expiry and explicit closure mapping. The archived experiment ID does not retain a grandfather exemption for reuse as new work.
