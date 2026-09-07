---
title: "Prompt-Length-Control Prompt"
status: adopted
canonicality: operative
relations:
  - type: derived_from
    target: ../../catalog/techniques/prompt-length-control.md
  - type: validated_by
    target: ../../experiments/2026-04-14_prompt-length-control/results/result.md
---

# Prompt-Length-Control Prompt

> Begrenzte Heuristik aus einem einzelnen Spec-First-vs.-Vergleich

## Schritt 1 — Spec-First (Constraint-Modus)

```
Bevor du Code schreibst:

1. Definiere alle Eingabe-Constraints (Formate, Grenzen, Sonderfälle)
2. Definiere alle erwarteten Outputs (Struktur, Edge Cases)
3. Definiere Fehlerverhalten (was passiert bei ungültigen Inputs?)

Erst dann: Implementiere den Code exakt nach diesen Constraints.
```

## Schritt 2 — Validierung

```
Prüfe den generierten Code gegen die Constraints aus Schritt 1:
- Sind alle Edge Cases abgedeckt?
- Stimmt das Fehlerverhalten?
- Sind die Outputs konsistent mit der Spezifikation?

Korrigiere Abweichungen.
```

## Warum nicht Ramble-First?

Im zugrunde liegenden einzelnen Text-Parsing-Versuch schnitt Ramble-First trotz zusätzlichem Text nicht besser als Code-First ab, während Spec-First alle dort geprüften Fälle bestand. Das unterstützt die praktische Heuristik, vor der Implementierung relevante Constraints explizit zu formulieren. Es beweist weder, dass zusätzliche Tokens generell wirkungslos sind, noch dass Constraint-Formulierung einen bestimmten internen kognitiven Modus verursacht oder dass der Effekt auf andere Aufgaben und Modelle übertragbar ist.
