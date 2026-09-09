---
title: "Roadmap — Koordination offener Arbeitsstränge"
status: active
triggered_by: "user-request-vibe-lab-operator-loop-2026-07-01"
canonicality: navigation
role: roadmap_index
created: "2026-05-10"
updated: "2026-09-07"
relations:
  - type: references
    target: masterplan.md
  - type: references
    target: foundations/vision.md
  - type: references
    target: foundations/repo-plan.md
  - type: references
    target: index.md
  - type: references
    target: blueprints/blueprint-agent-operability.md
  - type: references
    target: blueprints/blueprint-agent-operability-phase-1c.md
  - type: references
    target: blueprints/blueprint-evidence-control-plane-v1.md
  - type: references
    target: blueprints/blueprint-v2-roadmap.md
  - type: references
    target: blueprints/blueprint-v2.md
  - type: references
    target: blueprints/blueprint-agent-skill-minimal-layer-v0.1.md
  - type: references
    target: blueprints/blueprint-model-lab-control-plane-v1.md
  - type: references
    target: evaluations/agent-skill-file-fruitfulness.md
  - type: references
    target: evaluations/replay-gap-cross-diagnosis-rrg01-rrg02.md
  - type: references
    target: evaluations/rrg03-remediation-strategy-comparison.md
  - type: references
    target: playbooks/evidence-control-plane-roadmap-checklist.md
  - type: references
    target: playbooks/outcome-evidence-replication-series-gate.md
  - type: references
    target: playbooks/plan-execution-checklist.md
  - type: references
    target: playbooks/operator-lab-loop.md
  - type: references
    target: policies/interpretation-budget.md
  - type: references
    target: policies/model-lab-control-minimum.md
  - type: references
    target: ../decisions/process/2026-04-30-rrg03-remediation-boundary.yml
  - type: references
    target: ../decisions/process/2026-05-01-rrg-v02-remediation-preimage.yml
  - type: references
    target: ../decisions/process/p5-validator-scope-boundary.yml
  - type: references
    target: ../decisions/system/2026-04-23-metrics-enabled.yml
  - type: references
    target: ../decisions/system/2026-04-23-catalog-staleness-dormant.yml
---

# Roadmap — begrenzte aktive Navigation

## Zweck und Grenze

Diese Datei ist eine Wegkarte, kein Aufgabenregister und keine Wahrheitsquelle für aktive Experimente.

- Aktive Experimentwahrheit: `experiments/active.v1.json`.
- Aufgaben, Prioritäten und Promotionsentscheidungen: Bureau.
- Code-, Review-, Merge- und Prüfzustand: GitHub und CI.
- Ausgeführte Operatorarbeit: Grabowski-Receipts.
- Zielbild und Architekturgrenze: `docs/foundations/vision.md` und `docs/foundations/repo-plan.md`.

Bei jedem Widerspruch gilt die höher eingestufte Quelle. Historische Blueprints oder Experimentordner werden nicht durch eine Referenz in dieser Datei reaktiviert.

## Aktueller Zustand

Stand 8. September 2026:

- Labor ist auf einen kleinen Experiment- und Evidenzraum verengt; GitHub und Systemkatalog führen das System als `labor`/„Labor“. Historische Pfade und Dateinamen mit `vibe-lab` bleiben Provenienz und werden nicht pauschal umgeschrieben.
- `experiments/active.v1.json` enthält nach dem fälligen Review des Outcome-Bound-Aktivierungspiloten keinen aktiven Versuch. Der Pilot bleibt `not_executed` und ist mit `closure_outcome: defer` aus dem Aktivregister genommen, weil kein bereits vorhandener Provider den eingefrorenen Slot-Capture-Vertrag erfüllt.
- Die Custom-Agent-Schicht und instruktionsführende Cursor-/Copilot-Projektionsinhalte sind stillgelegt; generierte Kompatibilitätsmarker und ihre blocking Paritätsverträge bleiben aktiv.
- Die 36 Operator-Lab-Karten sind mit `insufficient_evidence` eingefroren und nach `experiments/_archive/` verschoben; ihre vier dedizierten Run-Card-/Metrics-Frontdoors sind nicht mehr blocking, der deterministische Closeout bleibt aus dem Archiv aktiv. Frühere Chronik-, Routing-, RepoBrief- und Model-Lab-Versuche sind historische Evidenz, keine aktive Experimentwahrheit.
- Die maschinenlesbare Validatorfläche besteht aus 45 Core-, 6 Active- und 40 Legacy-Zielen sowie zwei ergänzenden Checks, insgesamt 91 klassifizierten Validierungszielen. `Active` ist dabei eine Validatorgruppe und nicht die Zahl aktiver Experimente; der archivierte Routing-Readiness-Testfrontdoor und die beiden Phase-1c-Archivfrontdoors sind nach belegter Terminalität nicht mehr blocking.
- Das Bureau führt den Survivor-Audit weiterhin unter `heimgewebe/bureau#442`.

## Aktiver Repository-Ball

### RL-001 — Wahrheitsausrichtung und Survivor-Vertrag

**Ziel:** Alle maßgeblichen Labor-Dokumente einschließlich der kanonischen Steuerungsquellen beschreiben dieselbe begrenzte Rolle und bleiben über den überprüften Maschinenpflege-Pfad konsistent, ohne veraltete Bestandszahlen als Gegenwartswahrheit zu spiegeln.

**Umfang:**

- kanonischen Repo-Zweck und Maschinenidentität prüfen; `repo.meta.yaml` und die übrigen kanonischen Steuerungsquellen sind maschinell pflegbar und unterliegen denselben Scope-, Review-, CI- und Traceability-Gates;
- Grundlagenvision und Repository-Plan;
- README;
- Optimierungsplan und Validatorbericht;
- diese Roadmap;
- PR-Template und Dokumentfrische-Register.

**Nicht enthalten:**

- neue Runtime- oder Toolfunktion;
- neue Agentenrolle;
- neue instruktionsführende Exportprojektion;
- Entfernung bestehender Kompatibilitätsmarker oder ihrer operativen Verträge;
- Änderung an Experimentdaten, Schemas oder Validatorlogik;
- automatischer Bureau-, Routing-, Merge- oder Deploy-Eingriff.

**Erfolg:** vollständige CI, diffgebundener Review und Merge des Wahrheits- und Navigationsschnitts; kanonische Steuerungsquellen sind mit der begrenzten Labor-Rolle konsistent und können über denselben überprüften Maschinenpflege-Pfad aktualisiert werden.

## Nächste Arbeitsstränge

Die Reihenfolge ist verbindlich, soweit Bureau keine neue Prioritätsentscheidung trifft.

### RL-002 — Legacy-Validator-Survivor-Audit

Jedes der 38 verbleibenden Legacy-Ziele erhält eine Disposition:

- `retain_with_consumer`;
- `covered_by_core`;
- `retire`.

Prüfreihenfolge:

1. Agent-Handoff-, Agent-Command- und Command-Chain-Verträge;
2. Model-Lab-Spezialprüfungen erst nach separater terminaler Disposition; das aktuelle Model-Lab-Manifest bleibt `testing` und seine Guards bleiben blocking;
3. historische Replay-, Fixture- und Cross-Contract-Semantik;
4. die nie ausgeführten PR-Context- und rLens-Agent-Context-Designs sind archiviert und ihre je zwei dedizierten Frontdoors nicht mehr blocking; verbleibende historische Spezialflächen nur mit separater Consumer-/Archivevidenz reduzieren.

Der Reviewtermin 1. September 2026 ist überschritten. Von der früheren 48er-Baseline bleiben nach der Operator-Lab- und PR-Context-Archivierung 38 blocking Legacy-Ziele; weitere Reduktion erfolgt nur mit Archiv- oder Äquivalenzevidenz. Der Review eines Entfernungs-PR prüft diesen materiellen Beleg, ersetzt ihn aber nicht.

### RL-003 — fällige Experimentabschlüsse erzwingen

Der Outcome-Bound-Aktivierungspilot wurde am Reviewtermin 7. September 2026 ohne Aktivierung und ohne verbrauchten Slot `defer` geschlossen. Neue oder wiederaufgenommene Versuche benötigen eine neue prospektive Bindung; ein Reviewtermin darf nicht durch stilles Weiterlaufen ersetzt werden.

### RL-004 — Bibliotheksverbrauch prüfen

Katalog, Prompts, Benchmarks und Instruction Blocks auf reale externe Verbraucher, Entscheidungsziele und Reviewregeln prüfen. Nicht konsumierte Flächen archivieren oder als historisch behandeln. Bestehende Kompatibilitätsmarker bleiben erhalten, bis ihre operativen Verträge separat geändert werden.

## Historische Quellen

Die im Frontmatter referenzierten Blueprints, Evaluationen, Playbooks und Entscheidungen bleiben für Provenienz und Survivor-Prüfung erreichbar. Sie sind keine aktiven Arbeitsaufträge, solange sie nicht in `experiments/active.v1.json` oder Bureau ausdrücklich reaktiviert werden.

Insbesondere sind folgende frühere Expansionsrichtungen nicht aktiv:

- Agent-Operability als eigene Agentenschicht;
- Evidence-Control-Plane als Steuerungsebene;
- Model-Lab-Control-Plane als aktive Runtime;
- reaktive State→Signal→Policy→Action-Schleifen;
- automatische Ticketgenerierung;
- neue breite instruktionsführende Tool-Export-Abdeckung;
- Dashboard-, Plexer- oder Heimlern-Integration.

## Neue-Arbeit-Gate

Vor neuer Labor-Funktionalität oder einem neuen aktiven Versuch müssen alle Fragen mit Ja beantwortet sein:

1. Gibt es einen aktuellen externen Verbraucher?
2. Verändert das Ergebnis eine konkrete, reversible oder klar begrenzte Entscheidung?
3. Ist der Versuch **jetzt** mit bereits vorhandenen Oberflächen ausführbar, ohne die fehlende Messinfrastruktur erst für den Versuch bauen zu müssen?
4. Ist die Fehlerklasse nicht bereits generisch abgedeckt?
5. Besitzt die Arbeit Reviewdatum oder Ablauf und ein explizites Stop-Kriterium?
6. Sind Design-, Vorbereitungs-, Erfassungs-, Review- und Pflegeaufwand als getrennte Kosten sichtbar, ohne eingefrorene Experimentmetriken nachträglich zu ändern?
7. Entfernt die Änderung mindestens so viel dauerhafte Oberfläche, wie sie hinzufügt, oder besitzt sie einen belegten höheren Entscheidungsnutzen?
8. Bleiben Bureau, GitHub, CI, Grabowski und RepoGround die zuständigen Wahrheitsorgane?

Bei einem Nein wird die Idee roh dokumentiert, zurückgestellt oder archiviert.
