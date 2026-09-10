---
schema_version: "0.1.0"
title: "Spec-First + Constraint-Control"
status: adopted
summary: "Begrenzte Heuristik: Spec-First mit expliziten, prüfbaren Constraints verbinden; ein Qualitätsgewinn, Mechanismus oder Transfer ist nicht allgemein belegt."
components:
  - practice: "../techniques/spec-first-prompting.md"
    role: "Strukturgeber: Erzwingt formale Spezifikation vor Code-Generierung"
  - practice: "../techniques/prompt-length-control.md"
    role: "Beobachtungsanker: erinnert an den einzelnen 0.8/1.0/0.8-Vergleich, ohne einen kausalen Mechanismus zu behaupten"
evidence_source: "experiments/2026-04-14_prompt-length-control/"
synergy_description: "Die Kombination soll Spezifikationsarbeit auf prüfbare Constraints statt auf Länge ausrichten. Das ist eine operative Begründung; die Synergie selbst wurde im einzelnen Prompt-Length-Control-Setup nicht verglichen."
created: "2026-04-20"
updated: "2026-09-10"
author: "heimgewebe"
tags:
  - combo
  - spec-first
  - cognitive-modes
  - constraint-design
---

# Spec-First + Constraint-Control

## Synergie

Spec-First Prompting stellt eine Spezifikation vor die Code-Generierung. Als operative Ergänzung richtet Constraint-Control diese Spezifikation auf explizite, prüfbare Constraints aus:

1. **Spec-First:** Schreibe eine formale Spezifikation (z.B. OpenAPI, Interface-Definition).
2. **Constraint-Control:** Stelle sicher, dass die Spec echte Constraints enthält (Edge Cases, Validierungsregeln, Fehlerfälle) — nicht nur Struktur-Boilerplate.

Im zugrunde liegenden einzelnen Text-Parsing-Setup wurden für Code-First, Spec-First und Ramble-First `test_pass_rate`-Werte von `0.8`, `1.0` und `0.8` beobachtet. Dieser Vergleich hat weder die Kombination selbst getestet noch gezeigt, dass Constraint-Formulierung den Unterschied verursacht.

## Wann als Heuristik kombinieren

- Wenn eine Spezifikation konkrete Eingaben, Ausgaben, Edge Cases oder Fehlerfälle prüfbar machen soll.
- Wenn zusätzlicher Spezifikationstext keinen erkennbaren Bezug zu späteren Prüfungen hat.
- Als Ausgangspunkt für einen eigenen Vergleich in der betroffenen Aufgabenklasse.

## Anti-Synergie vermeiden

- Spec-First ohne prüfbare Constraints kann in lange, operativ schwache Specs abgleiten.
- Constraint-Formulierung ohne erkennbare Struktur kann schwer überprüfbare Listen erzeugen.

## Nicht-Claims

- Die Kombination maximiert nach der vorliegenden Evidenz keinen Qualitäts- oder Strukturgewinn.
- Ein kognitiver Moduswechsel oder anderer interner Mechanismus wurde nicht gemessen.
- Die einzelne 0.8/1.0/0.8-Beobachtung belegt keine Wirkung bei anderen Aufgaben, Modellen oder Setups.
