---
schema_version: "0.1.0"
title: "Constraint-First"
status: adopted
category: style
summary: "Stil für explizite, prüfbare Constraints vor der Implementierung; allgemeine Wirkung und interner Mechanismus sind nicht belegt."
evidence_source: "experiments/2026-04-14_prompt-length-control/"
created: "2026-04-20"
updated: "2026-09-10"
author: "heimgewebe"
tags:
  - style
  - prompting
  - constraint-design
  - cognitive-modes
relations:
  - type: validated_by
    target: ../../experiments/2026-04-14_prompt-length-control/results/result.md
  - type: references
    target: ../techniques/spec-first-prompting.md
---

# Style: Constraint-First

## Beschreibung

Relevante Constraints werden vor der Implementierung explizit und prüfbar gemacht. Der Stil unterscheidet sich von sachfremder Vorrede durch seinen Bezug zu Anforderungen und späteren Prüfungen.

## Stil-Merkmale

1. Eingangs-, Ausgangs- und Fehlerbedingungen vorab explizit machen.
2. Constraints in überprüfbarer Form strukturieren.
3. Aussagen nach Möglichkeit in Tests oder Checks überführen.
4. Zusätzlichen Text nur verwenden, wenn er Anforderungen oder Prüfung dient.

## Evidenzgrenze

Im einzelnen Quell-Setup wurden für Spec-First, Ramble-First und Code-First `test_pass_rate`-Werte von `1.0`, `0.8` und `0.8` beobachtet. Die Prompt-Arme unterschieden sich in mehreren Merkmalen; quantitative Tokenzahlen und ein interner Mechanismus wurden nicht gemessen.

## Beispiel

```
Bevor du Code schreibst, definiere:
1. Input-Constraints: [Format, Grenzen, Sonderfälle]
2. Output-Constraints: [Struktur, Typen, Formatierung]
3. Fehlerverhalten: [Ungültige Inputs → erwartetes Verhalten]
4. Edge Cases: [Leere Eingabe, Maximalwerte, Sonderzeichen]

Erst dann: Implementiere.
```

## Nicht-Claims

- Ein allgemeiner Qualitätseffekt ist nicht belegt.
- Ein kognitiver Moduswechsel wurde nicht direkt gemessen.
- Constraint-Formulierung ist nicht als Ursache der beobachteten Differenz belegt.
- Transfer auf andere Aufgaben, Modelle oder Setups bleibt offen.
