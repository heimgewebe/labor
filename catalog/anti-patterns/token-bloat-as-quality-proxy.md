---
schema_version: "0.1.0"
title: "Token-Bloat-as-Quality-Proxy"
status: adopted
category: anti-pattern
summary: "Warnheuristik gegen Textmenge als Qualitätsproxy; ein einzelner Text-Parsing-Vergleich beobachtete 0.8/1.0/0.8, ohne einen allgemeinen oder kausalen Effekt zu belegen."
evidence_source: "experiments/2026-04-14_prompt-length-control/"
created: "2026-04-20"
updated: "2026-09-10"
triggered_by: "github:heimgewebe/bureau#442; github:heimgewebe/labor#371:review"
author: "Jules"
tags:
  - prompting
  - anti-pattern
  - cognitive-modes
  - chain-of-thought
relations:
  - type: validated_by
    target: ../../experiments/2026-04-14_prompt-length-control/results/result.md
  - type: references
    target: ../../catalog/techniques/prompt-length-control.md
---

# Token-Bloat-as-Quality-Proxy

## Warum ist das ein Anti-Pattern?

Als allgemeine Qualitätsregel ist die Annahme unbelegt: „Wenn ich das Modell dazu bringe, mehr Text auszugeben, wird der nachfolgende Code besser."

Im Prompt-Length-Control-Experiment erzielten Ramble-First und Code-First in einem einzelnen Text-Parsing-Setup jeweils `0.8` `test_pass_rate`; Spec-First erzielte dort `1.0`. Damit ging die angeforderte längere, sachfremde Vorrede in diesem Durchlauf nicht mit einer höheren Pass-Rate gegenüber Code-First einher. Das ist keine allgemeine Widerlegung eines Nutzens zusätzlicher Tokens und isoliert Constraint-Formulierung nicht als Ursache.

## Evidenz

- **Code-First:** `test_pass_rate` 0.8
- **Spec-First:** `test_pass_rate` 1.0
- **Ramble-First:** `test_pass_rate` 0.8
- **Evidenzgrenze:** ein Task, ein Setup, eine Iteration; die Evidenz protokolliert keine quantitativen Tokenzahlen und keinen internen Mechanismus

## Typische Manifestationen

- „Erkläre erst ausführlich, was du tun willst, bevor du codierst" — ohne Bezug zu prüfbaren Anforderungen
- Lange Vorreden, die das Modell zum Schreiben irrelevanter Erklärungen zwingen
- Annahme, dass verboses Reasoning automatisch besseren Code erzeugt

## Stattdessen

Als operative Heuristik:

- Relevante Constraints vor der Implementierung explizit machen.
- Das Ergebnis gegen diese Constraints prüfen.
- Den Nutzen für die jeweilige Aufgabenklasse separat evaluieren, statt Textlänge als Qualitätsproxy zu verwenden.

## Nicht-Claims

- Zusätzliche Tokens sind nicht generell wirkungslos.
- Constraint-Formulierung ist durch diesen Einzeldurchlauf nicht als Ursache der höheren Pass-Rate belegt.
- Ein kognitiver Moduswechsel wurde nicht gemessen.
- Eine Übertragung auf andere Aufgaben, Modelle oder Setups ist nicht belegt.
