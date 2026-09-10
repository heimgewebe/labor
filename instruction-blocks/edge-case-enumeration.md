---
title: "Edge-Case-Enumeration"
type: instruction_block
status: adopted
canonicality: operative
evidence_source: "experiments/2026-04-14_prompt-length-control/"
created: "2026-04-20"
updated: "2026-09-10"
triggered_by: "github:heimgewebe/bureau#442; github:heimgewebe/labor#371:review"
tags:
  - edge-cases
  - completeness
  - prompting
relations:
  - type: derived_from
    target: ../catalog/techniques/spec-first-prompting.md
  - type: references
    target: ../catalog/techniques/prompt-length-control.md
---

Before implementation, enumerate relevant edge cases explicitly:
1. Empty or absent values.
2. Minimum, maximum, and boundary values.
3. Special characters and encoding cases.
4. Repeated operations when relevant.
5. Inputs outside the expected format.

For each relevant case, define expected behavior and verify the result against it.

Evidence boundary: one text-parsing run observed complete coverage of the tested cases in the Spec-First arm, while Code-First and Ramble-First each missed one. This supports explicit enumeration only as a bounded heuristic. It does not prove that an omitted specification case necessarily becomes an omitted output case or that the heuristic has a general causal quality effect.
