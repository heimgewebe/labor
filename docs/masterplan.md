---
title: "Masterplan — Labor Zielbild"
status: active
canonicality: operative
updated: "2026-09-07"
relations:
  - type: derived_from
    target: foundations/vision.md
  - type: derived_from
    target: foundations/repo-plan.md
---

# Masterplan

## Rolle

Labor ist ein kleiner, verbrauchergebundener Experiment- und Evidenzraum. Dieses Dokument besitzt keine eigene Status- oder Expansionswahrheit; bei Widersprüchen gelten `repo.meta.yaml`, `AGENTS.md`, `agent-policy.yaml` sowie die beiden Grundlagendokumente.

GitHub, Systemkatalog und Bureau führen das Organ als **Labor**. `repo.meta.yaml` ist human-protected und trägt bis zu einer menschlichen Änderung weiterhin die repo-interne Maschinenidentität `vibe-lab`. Historische Experiment-IDs, Evidenzreferenzen und stabile Dateinamen werden nicht wegen der Umbenennung umgeschrieben.

## Arbeitszyklus

1. **Roh erfassen:** Eine Beobachtung oder Frage darf billig in `raw-vibes/` entstehen.
2. **Prospektiv registrieren:** Ein Experiment benötigt vor der Beobachtung einen aktuellen externen Verbraucher, eine konkrete Entscheidung, Kontrolle und Behandlung, Mess- und Falsifikationsgrenzen sowie Review und Ablauf. Der aktuelle Optimierungsplan verlangt für den nächsten aktiven Versuch zusätzlich eine bereits ausführbare Beobachtungsroute, ein Kostenbudget und eine Stopregel.
3. **Evidenz binden:** Beobachtungen verweisen auf konkrete Commits, Pull Requests, CI-Prüfungen, Receipts oder andere benannte Primärbelege.
4. **Begrenzt auswerten:** Vergleichbarkeit, Unsicherheit, Aufwand und Nichtaussagen werden getrennt von Beobachtung und Entscheidung ausgewiesen.
5. **Explizit schließen:** `promote`, `pilot`, `defer`, `reject` oder `archive` wird reviewt dokumentiert; keine stille Verlängerung.
6. **Extern übernehmen:** Eine Praxis wird erst außerhalb von Labor durch das zuständige Organ wirksam. Labor selbst erhält dadurch keine Queue-, Routing-, Merge-, Deploy- oder Runtime-Autorität.

## Aktive Wahrheit

- `experiments/active.v1.json` ist die einzige Wahrheit über laufende Experimente.
- Ein vorhandener Experimentordner oder Validator macht Arbeit nicht automatisch aktiv.
- Bibliotheksartefakte sind nur bei benanntem Verbraucher, Entscheidungsziel und Reviewregel aktuelle Nutzfläche; sonst sind sie historischer Bestand.
- Legacy-Spezialvalidatoren bleiben nur so lange blocking, wie ihre Fehlerklasse nicht archiviert oder gleichwertig durch generische Core-Gates geschützt ist.
- Dynamische Bestandszahlen werden nicht in diesem Masterplan gespiegelt; dafür gelten das Validatorinventar und die aktuelle Roadmap.

## Nichtziele

Labor ist kein Scheduler, keine Queue, kein Dashboard, kein Agenten-Orchestrator, kein zweites Bureau, kein zweiter Grabowski-Governor, kein Routingdienst und keine automatische Lerninstanz. Neue Dienste, Datenbanken, instruktionsführende Projektionsschichten oder selbsttätige Policy-/Routing-Änderungen gehören nicht zum Zielbild.

## Aktuelle Steuerungsreferenzen

- [Vision](foundations/vision.md) — stabile fachliche Rolle und epistemische Grenzen
- [Repo-Plan](foundations/repo-plan.md) — Architektur, Survivor-Programm und Stopregeln
- [Roadmap](roadmap.md) — aktuelle, quellengebundene Koordination
- [Optimierungsplan](plans/vibe-lab-optimization-plan-v1.md) — laufende Oberflächenreduktion; historischer Dateiname bleibt stabil
- [`experiments/active.v1.json`](../experiments/active.v1.json) — einzige aktive Experimentwahrheit
