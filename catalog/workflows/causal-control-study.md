---
schema_version: "0.1.0"
title: "Kausale Kontrollstudie"
status: adopted
category: workflow
summary: "Workflow-Heuristik für Kontrollarm-Vergleiche; alternative Erklärungen werden prüfbar gemacht, aber nicht allein durch das Design kausal ausgeschlossen."
evidence_source: "experiments/2026-04-14_prompt-length-control/"
created: "2026-04-20"
updated: "2026-09-10"
triggered_by: "github:heimgewebe/bureau#442; github:heimgewebe/labor#371:review"
author: "heimgewebe"
tags:
  - workflow
  - experiment-design
  - causal-control
  - methodology
relations:
  - type: validated_by
    target: ../../experiments/2026-04-14_prompt-length-control/results/result.md
---

# Workflow: Kausale Kontrollstudie

## Übersicht

Eine operative Heuristik für Vergleiche mit Kontrollarmen. Ziel ist, alternative Erklärungen explizit prüfbar zu machen und verbleibende Unterschiede sichtbar zu halten. Ein Kontrollarm isoliert nicht automatisch eine Ursache.

## Schritte

### 1. Hypothese formulieren

- Zu untersuchenden Faktor benennen.
- Alternative Erklärungen benennen.
- Vorab festlegen, welche Beobachtung welche Erklärung stützen oder schwächen würde.

### 2. Kontrollarm designen

- Einen Arm gestalten, der die alternative Erklärung gezielt prüft.
- Dokumentieren, welche Merkmale angeglichen sind und welche Unterschiede verbleiben.
- Nicht behaupten, eine Variable sei isoliert, solange relevante Confounder offen sind.

### 3. Messbare Metriken definieren

- Objektive Metrik wählen, z.B. `test_pass_rate`.
- Gleiche Messmethodik für alle Arme verwenden.
- Baseline als Referenz festlegen.

### 4. Durchführen und dokumentieren

- Bedingungen soweit möglich konstant halten und Abweichungen dokumentieren.
- Rohbeobachtungen zeitnah erfassen.
- Wiederholungen und Stichprobengröße explizit nennen.

### 5. Begrenzt interpretieren

- Direkt Beobachtetes von Mechanismushypothesen trennen.
- Interpretation Budget explizit setzen.
- Ungetestete Variablen und verbleibende Confounder offen halten.

## Beispiel: Prompt-Length-Control

Im historischen Quell-Setup lagen die beobachteten `test_pass_rate`-Werte für Code-First, Spec-First und Ramble-First bei `0.8`, `1.0` und `0.8`. Ramble-First ging dort nicht mit einer höheren Pass-Rate gegenüber Code-First einher. Die Evidenz enthält jedoch keine quantitative Tokenmessung, keine Wiederholungen pro Arm und keine Messung eines internen Mechanismus.

## Nicht-Claims

- Der Einzeldurchlauf belegt keinen kausalen Struktureffekt.
- Zusätzliche Textmenge ist nicht als generell wirkungslos belegt.
- Constraint-Formulierung ist nicht als Mechanismus der Differenz belegt.
- Ergebnisse sind nicht ohne neue, auf die Aufgabenklasse gebundene Vergleiche übertragbar.
