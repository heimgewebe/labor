---
title: "Playbook: PR Context Capture"
status: archived
canonicality: derived
schema_version: "0.1.0"
created: "2026-07-02"
updated: "2026-09-09"
triggered_by: "github:heimgewebe/bureau#442; conversation:user-request-2026-09-09-continue-labor-survivor-audit"
author: "heimgewebe"
relations:
  - type: references
    target: ../../experiments/_archive/2026-06-10_pr-agent-context-comparison-series/pilot-v1.yml
  - type: references
    target: ../../tools/vibe-cli/pr_context_capture.py
  - type: references
    target: ../../scripts/docmeta/validate_pr_context_pilot.py
tags: [playbook, pr, evidence, historical]
---

# Playbook: PR Context Capture

## Status

Historical only. The B-vs-D PR-context pilot was never executed and is archived. Its frozen `pilot-v1.yml` remained `execution_allowed: false` because task and role bindings were absent. No new run may be admitted under that revision.

`tools/vibe-cli/pr_context_capture.py`, `scripts/docmeta/validate_pr_context_pilot.py` and their regression tests remain available solely to inspect or reproduce the historical contract. They are not blocking Make frontdoors and do not authorize new capture runs.

## Historical audit

```bash
python3 scripts/docmeta/test_validate_pr_context_pilot.py
python3 tools/vibe-cli/test_pr_context_capture.py
python3 scripts/docmeta/validate_pr_context_pilot.py
```

The expected result is a structurally valid but execution-blocked archived pilot. `--require-ready` must fail for that frozen revision.

## Boundary

A future PR-context comparison requires a new prospective experiment with a current external consumer, fresh task and role bindings, current decision target, review/expiry and explicit outcome criteria. The archived experiment id and its old condition assignments must not be reused as an active shortcut.

Nothing in this archive establishes condition superiority, general agent quality, Lenskit necessity, adoption readiness or the absence of value in repository context.
