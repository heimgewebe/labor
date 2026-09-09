---
title: "Playbook: Operator Lab Loop"
status: archived
canonicality: derived
schema_version: "0.1.0"
created: "2026-07-01"
updated: "2026-09-09"
author: "heimgewebe"
triggered_by: "heimgewebe/bureau#442"
origin_triggered_by: "user-request-vibe-lab-operator-lab-loop-2026-07-01"
relations:
  - type: references
    target: pr-run-evidence-pack.md
  - type: references
    target: pr-context-capture.md
  - type: references
    target: pr-review-evidence-wait-gate.md
    reason: "PR work with review claims must record expected review surfaces before readiness claims."
  - type: references
    target: plan-execution-checklist.md
  - type: references
    target: ../roadmap.md
  - type: references
    target: ../../experiments/_archive/2026-07-01_operator-lab-loop/manifest.yml
  - type: references
    target: ../../experiments/_archive/2026-06-10_pr-agent-context-comparison-series/pilot-v1.yml
    reason: "Historical Operator-Lab runs referenced the now archived PR-context pilot; this relation is provenance only."
tags:
  - playbook
  - operator
  - evidence
  - pr
  - agent-workflow
---

# Playbook: Operator Lab Loop

> **Archivstatus:** Dieses Playbook dokumentiert den abgeschlossenen Operator Lab Loop. Die 36-Karten-Serie ist eingefroren (`insufficient_evidence`) und liegt im Archiv. Es ist keine operative Anleitung fuer neue Run Cards. Neue Operator-Prozess-Experimente muessen als eigener Versuch prospektiv registriert werden. Archivierung ausgelöst durch `heimgewebe/bureau#442`.
>
> **Historischer Zweck:** Vibe-Lab wurde als Messrahmen fuer echte Repo-, PR- und Agentenarbeit genutzt. Es erzeugte keine Freigabe, keinen Merge und kein Erfolgsverdikt.

## 1. Dialektischer Kern

### These

Vibe-Lab soll reale Arbeit verbessern: PRs, Reviews, Agenten-Delegation, Operator-Entscheidungen und Handoffs werden vergleichbarer, wenn jeder relevante Arbeitslauf eine kleine, pruefbare Spur bekommt.

### Antithese

Zu viel Labor macht Arbeit langsamer. Ein zusaetzlicher Validator, eine weitere Pflichtdatei oder ein weiterer Review-Gate kann mehr Reibung erzeugen als er entfernt.

### Synthese

Der Operator Lab Loop ist bewusst klein: Er dokumentiert nur Entscheidung, Kontext, Evidence, Reibung und naechste Konsequenz. Er ist ein Nutzungsprotokoll, kein neues Kontrollregime.

## 2. Alternative Sinnachse

Nicht fragen: "Wie bauen wir Vibe-Lab weiter aus?"

Sondern fragen: "Welche Unsicherheit in unserer echten Arbeit muss kleiner werden?"

Primaere Unsicherheit:

> Kann ich einem Agenten-, Tool- oder Review-Ergebnis trauen, und warum?

Sekundaere Unsicherheit:

> War der zusaetzliche Prozess selbst nuetzlich oder nur methodischer Schmuck?

## 3. Ausloeser

Der Loop wird genutzt, wenn mindestens eine Bedingung zutrifft:

- ein PR-Review oder PR-Rework beeinflusst eine Entscheidung;
- Codex, Claude, Aider, agy, Grabowski oder Bureau werden fuer Repo-Arbeit eingesetzt;
- ein starker Claim entstehen koennte, zum Beispiel "CI gruen", "Agent hat korrekt umgesetzt", "Review war unabhaengig", "Kontext hat geholfen";
- eine neue Arbeitsweise dauerhaft uebernommen werden soll;
- ein Operator-Fehler, eine Friktion oder ein Scope-Drift sichtbar wurde.

Nicht nutzen fuer triviale Aenderungen ohne Claim, Entscheidung oder Lernwert.

## 4. Historischer Ablauf

Die folgenden Schritte beschreiben den frueheren Loop und sind keine aktuelle Run-Card-Anweisung.

1. **Praemissencheck:** Was muesste wahr sein, damit der Arbeitsmodus sinnvoll ist?
2. **Condition festhalten:** baseline, Vibe-Lab-Handoff, Lenskit-Handoff, decision-first checklist oder other.
3. **Steuerboard-Signal lesen:** `steuerboard operator report --branch-warning-threshold 5 --json` als Nutzungsprobe; kein Gate.
4. **Run Card schreiben:** kleine YAML-Card unter `artifacts/run-*/run-card.yml`.
5. **Evidence binden:** kleine repo-lokale Artefakte oder stabile Referenzen. Keine Loghalde.
6. **Review-Evidence-Wartegate pruefen:** Bei PR-Arbeit mit Review- oder Merge-Readiness-Claim erwartete Review-Surfaces fuer den aktuellen Head einordnen; siehe `pr-review-evidence-wait-gate.md`.
7. **Reibung zaehlen:** Zeit, Korrektur, Nacharbeit, falsche Claims, Entscheidungsaufwand.
8. **Entscheiden:** adopt, iterate, defer, reject oder no_decision.
9. **Rueckfuehren:** Nur bei wiederholtem Nutzen in Playbook, Instruction Block, Agent-Regel oder Bureau-Kandidat uebertragen.

## 4.1 Archivregel fuer Run Cards

Die eingefrorene Serie liegt unter:

```text
experiments/_archive/2026-07-01_operator-lab-loop/artifacts/run-*/run-card.yml
```

Diese Karten und ihre vorhandenen `run_meta.json`-Dateien sind historische Evidenz. **Keine neue Run Card wird in diese Serie geschrieben und fehlende historische Metadaten oder Laufzeiten werden nicht nachtraeglich rekonstruiert.**

Die Python-Werkzeuge `validate_operator_lab_run_cards.py` und `operator_lab_metrics.py` samt Regressionstests bleiben fuer manuelle historische Audits erhalten. Ihre vier dedizierten Make-Frontdoors sind nach der Archivierung nicht mehr Teil der blocking Legacy-Validierung. Der deterministische Cross-Run-Closeout bleibt dagegen aktiv und blocking und liest die eingefrorene Serie aus dem Archiv.

Ein neuer Operator-Prozess-Vergleich benoetigt einen neuen prospektiv registrierten Experimentordner mit Verbraucher, Entscheidung, Kontrolle/Behandlung, primaerer Messgroesse, materieller Wirkungsschwelle, Review, Ablauf und Closure-Regel.

## 5. Run Card Mindestfelder

```yaml
schema_version: "0.1.0"
run_id: "run-YYYYMMDD-short-name"
date: "YYYY-MM-DD"
operation: "kurze Beschreibung"
target_repo: "repo oder Pfad"
condition: "baseline | vibe_lab_handoff | lenskit_handoff | decision_first | other"
operator_tooling:
  - "ChatGPT"
  - "Grabowski"
claims:
  - claim: "enger Claim"
    status: "observed | plausible | missing_evidence | not_claimed"
    evidence:
      - path: "repo-lokaler Pfad oder stabile Referenz"
        evidence_status: "repo_local | external_verified | external_unverified | missing_evidence"
metrics:
  scope_drift_count: 0
  unsupported_claim_count: 0
  missing_locator_count: 0
  validation_gap_count: 0
  review_friction_count: 0
  rework_count: 0
  false_block_count: 0
  task_completion_time_observed: "not_measured"
steuerboard_probe:
  useful_signal: "..."
  changed_decision: "yes | no"
  noise: "low | medium | high"
bureau_bridge:
  create_or_update_candidate: false
  reason: "..."
decision: "adopt | iterate | defer | reject | no_decision"
does_not_establish:
  - "condition_superiority"
  - "general_agent_quality"
  - "adoption_readiness"
```

## 6. Claim-Grenzen

Belegt:

- Ein Befehl lief, wenn Output, Exit-Code oder stabile externe Evidence vorliegt.
- Ein Review-Kommentar existiert, wenn ein Review-Export oder eine stabile Referenz vorliegt.
- Ein Scope-Drift wurde beobachtet, wenn geaenderte Dateien, erwartete Zielpfade und Abweichung dokumentiert sind.

Plausibel:

- Eine Arbeitsweise half, wenn weniger Rework oder weniger Review-Friction beobachtet wurde, aber nur in einem Run.
- Ein Handoff war nuetzlich, wenn der Agent weniger Rueckfragen oder weniger falsche Claims produzierte.

Nicht behauptbar:

- "Besser als Alternative" ohne Vergleichsrun.
- "Agent ist zuverlaessig" aus einem erfolgreichen Run.
- "Vibe-Lab beweist Nutzen" ohne replizierte Outcome-Evidence.
- "Bureau soll automatisch priorisieren" ohne Rueckkopplung aus mindestens drei Runs.

## 7. Bureau-Bruecke

Bureau darf Operator-Lab-Ergebnisse als Priorisierungs- oder Frontier-Signal nutzen, aber Vibe-Lab bleibt Quelle fuer methodische Evidence.

Bureau wird erst beruehrt, wenn eine dieser Bedingungen wahr ist:

- mindestens drei Operator-Lab-Runs zeigen dieselbe Reibungsklasse;
- ein Run erzeugt einen klaren Folge-Task fuer ein anderes Repo;
- ein wiederkehrender Operator-Engpass braucht systemische Priorisierung.

Bis dahin gilt:

- keine Bureau-Mutation nur zur Dokumentations-Schoenheit;
- kein Bureau-Kandidat ohne Vibe-Lab-Run-Card;
- Bureau darf zusammenfassen und priorisieren, aber keine Vibe-Lab-Claims erhoehen.

## 8. Stop-Regeln

Den Loop abbrechen oder kuerzen, wenn:

- die Dokumentation laenger wird als die eigentliche Aenderung;
- keine Entscheidung, kein Claim und keine Reibung vorliegt;
- Evidence nur aus Selbstbericht besteht und trotzdem als PASS wirken wuerde;
- der Loop selbst eine Blockade erzeugt.

## 9. Erste und abgeschlossene Umsetzung

Der historische Nutzungsfall liegt unter `experiments/_archive/2026-07-01_operator-lab-loop/`.

Dieser Run beweist nicht, dass der Operator Lab Loop besser ist. Er beweist nur, dass der Loop als leichtgewichtige Repo-Spur angelegt und mit den bestehenden PR-Evidence-Regeln kompatibel dokumentiert werden kann.

## 10. Historisches Optimierungsziel

Was: Vibe-Lab als reale Operator-Feedbackschleife nutzbar machen.

Wie: kleine Run Cards statt grosser neuer Validatoren.

Wodurch: bestehende Evidence-Pack-, PR-Kontext- und Roadmap-Mechanik wiederverwenden.

Wirkung: weniger Overclaiming, klarere Delegationsentscheidungen, reproduzierbare Lernspuren.

Nebenwirkung: zusaetzliche Dokumentationsarbeit. Deshalb bleibt der Loop opt-in und muss Reibung sichtbar machen.
