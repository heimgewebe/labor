---
title: "Policy: Agent Reading Protocol"
status: active
canonicality: operative
schema_version: "0.1.0"
created: "2026-07-01"
updated: "2026-09-09"
author: "heimgewebe"
triggered_by: "user-request-vibe-lab-operator-consumption-bridge-2026-07-01"
relations:
  - type: references
    target: ../../AGENTS.md
  - type: references
    target: ../roadmap.md
  - type: references
    target: pr-run-evidence-policy.md
  - type: references
    target: interpretation-budget.md
tags:
  - policy
  - agent-workflow
  - evidence
  - reading
---

# Policy: Agent Reading Protocol

> Zweck: Diese Policy legt fest, welche Repo-Oberflaechen ein Agent vor welcher Claim-Klasse lesen muss. Sie erzeugt kein Erfolgsverdikt und ersetzt keine Evidence. Sie macht nur sichtbar, wann eine Antwort oder ein PR-Body genug Kontextkontakt fuer den behaupteten Claim hatte.

## 1. Kern

### These

Agenten liefern bessere Repo-Arbeit, wenn sie vor starken Claims die passenden Primaer- und Navigationsquellen lesen.

### Antithese

Zu viel Pflichtlektuere macht kleine Aenderungen langsam und erzeugt Scheinsicherheit: Eine gelesene Datei beweist noch kein Verstehen.

### Synthese

Das Protokoll ist task-profiliert. Kleine Aenderungen bleiben leicht, starke Status-, Evidence-, Review- oder Agenten-Claims muessen vorab an passende Quellen gebunden werden.

## 2. Task-Profile

| task_profile | Minimal zu lesen | Zusaetzlich lesen bei starken Claims | Nicht ausreichend |
|---|---|---|---|
| `small_docs_change` | betroffene Datei; `AGENTS.md`; `agent-policy.yaml` | `docs/roadmap.md`, wenn Status oder Arbeitsstrang beruehrt ist | nur Diff ohne Kontext |
| `pr_review` | PR-Diff; betroffene Policies/Schemas; `docs/playbooks/pr-run-evidence-pack.md` | Run-/Evidence-Artefakte; CI-/Test-Evidence; Review-Exports | PR-Beschreibung allein |
| `prospective_experiment` | neue Registrierung; betroffene Zielrepo-Doku; Kontroll-/Behandlungsdefinition | primaere Messgroesse, materielle Wirkungsschwelle, Review-/Expiry-/Closure-Regel und vorhandene Vergleichsevidence | historisches Experiment oder einzelne Run Card als Freigabe |
| `roadmap_status_claim` | `docs/roadmap.md`; die in der Roadmap genannte Quelle | `docs/doc-freshness-registry.yml`, wenn der Claim dort registriert ist | Roadmap-Zeile ohne Quellencheck |
| `claim_evidence_claim` | Claim-Tabelle oder Registry; Evidence-Artefakt; betroffene Policy | Rohlog ohne Status/Verdict-Bindung | Selbstbericht als PASS |
| `agent_or_bureau_bridge` | konkrete aktuelle Zielrepo-Quelle; relevante Evidence; aktuelle Bureau-Quelle fuer den behaupteten Bridge-Status | mehrere unabhaengige Faelle, wenn Prioritaets- oder Wirkungsclaims behauptet werden | einzelner historischer Run als Systemschluss |

## 3. Claim-Klassen

Belegt werden darf nur, was durch gelesene Quellen und Evidence gedeckt ist.

- `observed`: Eine Datei, ein Artefakt, ein PR-Kommentar oder ein Befehlsergebnis wurde konkret gesehen.
- `plausible`: Eine Ableitung ist naheliegend, aber nicht voll belegt.
- `missing_evidence`: Der Claim koennte wahr sein, aber die noetige Evidence fehlt.
- `not_claimed`: Der Lauf erzeugt bewusst keinen starken Claim.

## 4. Evidence-Pflichtlinie ohne Operator-Lab-Zwang

Normale Repo-, PR- oder Agentenarbeit erzeugt **keinen** Operator-Lab-Trigger-Check und **keine** Run-Card-Pflicht. Ein starker Claim erhoeht die benoetigte Evidence-Tiefe, macht die Arbeit aber nicht automatisch zu einem Experiment.

Es gilt:

- fuer PR-Claims `pr_review` bzw. `claim_evidence_claim` verwenden;
- fuer Statusclaims `roadmap_status_claim` verwenden;
- fuer Agent-/Bureau-Bruecken den aktuellen Zielrepo- und Bureau-Zustand lesen;
- nur wenn tatsaechlich ein vergleichender Prozessversuch geplant ist, `prospective_experiment` verwenden und einen **neuen** prospektiv registrierten Experimentpfad anlegen;
- historische oder archivierte Experimentserien werden niemals als neue Schreibflaeche wiederverwendet.

Eine prospektive Registrierung bindet mindestens Verbraucher und Entscheidungsziel, Kontrolle und Behandlung, primaere Messgroesse, materielle Wirkungsschwelle, Reviewdatum, Ablauf und Closure-Ausgang. Fehlende Evidence bleibt ein Gap; sie wird nicht durch eine neue Run Card ersetzt.

## 5. Answer- und PR-Body-Disziplin

Antworten und PR-Bodies muessen starke Claims kalibrieren:

- `PASS` nur mit repo-lokaler, CI- oder extern verifizierter Evidence.
- `self_reported` darf Prozess- oder Ergebnis-Claims nicht allein stuetzen.
- Health-, Index- oder Reading-Passes beweisen kein Repo-Verstehen.
- Wenn Quellen widersprechen, wird der Widerspruch genannt und nicht geglaettet.
- Wenn eine Pflichtquelle fehlt, wird das als Gap benannt: `X fehlt, noetig fuer Y`.

## 6. Minimaler Verbrauchsnachweis

Fuer nicht-triviale Agentenlaeufe soll der Agent am Ende knapp angeben:

```text
Reading Protocol:
- task_profile:
- primary_sources_checked:
- evidence_sources_checked:
- sidecars_or_navigation_used:
- explicit_gaps:
- does_not_establish:
```

Diese Angabe ist eine Selbstauskunft, kein Beweis. Sie hilft Reviewenden, die Kontextaufnahme zu pruefen.

## 7. Stop-Regeln

Das Protokoll wird gekuerzt, wenn:

- die Aenderung trivial ist und keinen starken Claim erzeugt;
- die Dokumentation laenger waere als die Aenderung;
- ein Run nur durch Selbstbericht gruener wirken wuerde;
- das Protokoll selbst die Arbeit blockiert.

## 8. Nicht-Claims

Dieses Protokoll beweist nicht:

- dass ein Agent die Quellen verstanden hat;
- dass alle relevanten Quellen gelesen wurden;
- dass ein PR korrekt ist;
- dass ein Workflow besser ist als ein anderer;
- dass Bureau automatisch priorisieren soll.

## 9. Optimierungsziel

Was: Agentenarbeit konsumierbarer und pruefbarer machen.

Wie: task-profilierte Leseanforderungen statt Universalpflicht.

Wodurch: vorhandene AGENTS-, Roadmap- und Evidence-Flaechen verbinden; prospektive Registrierung nur fuer tatsaechlich geplante Experimente verwenden.

Wirkung: weniger Overclaiming, klarere PR-Bodies, bessere Anschlussfaehigkeit fuer Grabowski, Bureau, Cabinet und Lenskit.

Nebenwirkung: mehr Prozessoberflaeche. Deshalb bleibt die Pflicht an Claim-Staerke gekoppelt.
