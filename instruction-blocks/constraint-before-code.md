---
title: "Constraint-Before-Code"
type: instruction_block
status: adopted
canonicality: operative
evidence_source: "experiments/2026-04-14_prompt-length-control/"
created: "2026-04-20"
updated: "2026-09-10"
tags:
  - constraints
  - cognitive-modes
  - prompting
relations:
  - type: derived_from
    target: ../catalog/techniques/prompt-length-control.md
---

Before implementation:
1. List relevant input constraints such as types, ranges, formats, and required fields.
2. List output constraints and expected edge-case behavior.
3. Define behavior for invalid input.
4. Identify material edge cases explicitly.
5. Verify the result against those constraints.

Treat this as an operational heuristic, not as a proven mechanism. In the source experiment, one text-parsing setup observed `test_pass_rate` values of `0.8`, `1.0`, and `0.8` for Code-First, Spec-First, and Ramble-First. It did not measure a cognitive mode, quantitatively isolate token volume, or establish general transfer.
