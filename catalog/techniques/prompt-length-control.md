---
schema_version: "0.1.0"
title: "Prompt-Length Control (Cognitive-Mode-Switching)"
status: adopted
category: technique
summary: "In einem einzelnen Text-Parsing-Versuch schnitt Spec-First besser ab als Code-First und Ramble-First; Mechanismus und Übertragbarkeit bleiben offen."
evidence_source: "experiments/2026-04-14_prompt-length-control/"
created: "2026-04-14"
updated: "2026-09-07"
author: "Jules"
tags:
  - prompting
  - cognitive-modes
  - spec-first
  - causal-control
  - vibe-coding
relations:
  - type: validated_by
    target: ../../experiments/2026-04-14_prompt-length-control/results/result.md
  - type: references
    target: ../../catalog/techniques/spec-first-prompting.md
---

# Prompt-Length Control (Cognitive-Mode-Switching)

## Kernaussage

Im dokumentierten einzelnen Text-Parsing-Versuch erreichte Spec-First eine höhere Test-Pass-Rate als Code-First und Ramble-First. Das spricht **in diesem Setup** gegen die einfache Erklärung, dass bloß mehr vorangestellter Text den beobachteten Unterschied erzeugt. Der interne Mechanismus wurde nicht direkt gemessen; ein „kognitiver Moduswechsel“ bleibt eine Hypothese, keine nachgewiesene Ursache.

## Evidenz

Eine Kontrollstudie mit drei Armen an einem Text-Parsing-Task:

| Arm | Token-Volumen | Struktur | test_pass_rate |
|-----|--------------|----------|----------------|
| Code-First | niedrig | keine | 0.8 |
| Spec-First | hoch | ja (Constraints) | 1.0 |
| Ramble-First | hoch | nein (Essay) | 0.8 |

Ramble-First produzierte hohes Token-Volumen (wie Spec-First), fiel aber in denselben Naiv-Regex-Fehler wie Code-First zurück.

## Wann anwenden

- Als begrenzte Heuristik, wenn vor der Implementierung explizite Constraints hilfreich sein könnten.
- Als Ausgangspunkt für einen neuen, auf die konkrete Aufgabenklasse registrierten Vergleich.
- Nicht als allgemeiner Wirksamkeits- oder Mechanismusbeweis für Spec-First verwenden.

## Einschränkungen

- n=1 Task, 1 Modell, 1 Experimentator
- Nur Text-Parsing-Kontext — andere Task-Typen nicht getestet
- Ein interner Cognitive-Mode-Mechanismus wurde nicht direkt gemessen
- Die 0.8/1.0/0.8-Beobachtung trennt Struktur und Textmenge nur in diesem einen Versuchsaufbau


## Consumer- und Claim-Grenze

Bei der lokalen Ökosystemsuche am 7. September 2026 wurden außerhalb des Labor-Bestands, eines historischen `vibe-lab`-Checkouts und generierter RepoGround-/Manifest-Bundles keine aktuellen Verbraucherreferenzen auf diesen Artefaktnamen gefunden. Das ist kein Beweis für Nichtnutzung außerhalb des untersuchten Bestands. `status: adopted` bezeichnet deshalb hier nur die bestehende repo-interne Übernahme und keinen Nachweis allgemeiner Wirksamkeit.
