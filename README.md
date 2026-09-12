# Labor

**Verbrauchergebundener Experiment- und Evidenzraum für überprüfbare Arbeitsweisen.**

Labor hält rohe Beobachtungen fest, registriert begrenzte Vergleiche vor ihrer Ausführung, bindet Ergebnisse an konkrete Evidenz und schließt sie mit einer überprüften Entscheidung ab.

Es ist kein Agentenlaufzeitsystem, Scheduler, Dashboard, zweites Bureau, zweiter Grabowski-Governor oder automatische Lerninstanz. GitHub, CI, Grabowski, RepoGround und Bureau bleiben die jeweiligen Wahrheits- und Entscheidungsorgane.

Die aktuelle Organ-, Repository- und Maschinenidentität ist **Labor** beziehungsweise `labor`. Historische Experiment-IDs, Evidenzreferenzen und stabile Dateinamen mit `vibe-lab` bleiben unverändert, wenn sie Provenienz oder Pfadkompatibilität tragen. Kanonische Steuerungsdateien sind maschinell pflegbar und durchlaufen dieselben Scope-, Review-, CI- und Traceability-Gates wie andere Änderungen.

## Schnellstart

### 💡 Rohe Idee festhalten

Lege eine Markdown-Datei in `raw-vibes/` an:

```bash
echo "# Meine Beobachtung\n\nEin begrenzter Kontext scheint bei dieser Aufgabenklasse weniger Fehlpfade zu erzeugen ..." \
  > raw-vibes/context-observation.md
```

Kein Schema, kein Frontmatter, keine CI-Prüfung. Eine rohe Idee ist noch keine Wirkungsaussage und keine Aufgabe.

### 🧪 Zero-to-Decision

Nur wenn eine reale Entscheidung und ein bestätigter externer Verbraucher benannt sind. Der kanonische Pfad verwendet bestehende Dateien als Wahrheit und erzeugt keine zweite Runtime:

1. **register** — kopiere `experiments/_template/` in einen neuen Ordner und fülle `registration.v2.json` vor der ersten Beobachtung aus. Consumer, Decision-Referenz, Kontrolle, Behandlung, primäre Messgröße, Aufwandseinheit, Ergebnisgrenzen, Surface-Budget, Reviewdatum, Ablauf und Closure-Zuordnung werden prospektiv eingefroren.
2. **activate** — trage das Experiment kohärent in `experiments/active.v1.json` ein und prüfe `python3 scripts/docmeta/validate_active_experiments.py`.
3. **admit** — publiziere jeden natürlichen Fall vor Planung/Ausführung create-only:

   ```bash
   python3 tools/vibe-cli/admit_natural_case.py \
     --registration experiments/<experiment>/registration.v2.json \
     --request <request.json>
   ```

   Ohne `--admissions-dir` schreibt der vorhandene Writer ausschließlich nach `experiments/<experiment>/artifacts/admissions/`.
4. **observe** — binde die vorab definierte Messung mit `tools/vibe-cli/capture_effect_observation.py` an konkrete Evidenz. Die CLI verlangt unter anderem Registration, Observations-Datei, Condition, Aufwand, Evidence-Ref/-Digest, Observer und Decision-Maker; `--help` zeigt den vollständigen Vertrag.
5. **evaluate** — erzeuge die deterministische Auswertung, ohne Policy zu ändern:

   ```bash
   python3 tools/vibe-cli/evaluate_effect.py \
     --registration experiments/<experiment>/registration.v2.json \
     --observations experiments/<experiment>/results/observations.v2.json \
     --output experiments/<experiment>/results/effect-evaluation.v1.json
   ```

6. **decide** — Review schreibt die aktuelle kanonische `results/decision.yml` beziehungsweise bei bereits phasengebundenen Altbeständen die explizit gebundene `pN/decision.yml`.
7. **archive** — nach reviewed Decision den Active-Eintrag entfernen und Evidenz/Decision unter dem registrierten Archive-Pfad durch normalen PR/Review bewahren.

Minimal dauerhaft: eine Registrierung, während der Laufzeit ein Active-Binding, ein Evidence-Stream und eine Decision. Admission-Receipts sind Evidenz, keine zusätzliche State-Schicht. Es gibt bewusst noch keinen `labor start/close`-Orchestrator; ein realer Lauf muss zuerst zeigen, dass dessen dauerhafte Oberfläche weniger kostet als die verbleibende manuelle Zeremonie.

### 📚 Ergebnis übernehmen

Erst wenn ein Experiment belastbare Evidenz und einen benannten externen Verbraucher besitzt:

1. Erstelle einen Pull Request mit dem Template **Promotion**.
2. Alle Pflichtartefakte müssen vollständig sein (`make validate`).
3. Review und Merge dokumentieren die Labor-Entscheidung.
4. Die tatsächliche Übernahme in ein Produktrepo, Bureau oder Grabowski bleibt eine eigene Entscheidung des zuständigen Organs.

## Aktive Experimente

`experiments/active.v1.json` ist die einzige begrenzte Wahrheit über laufende Experimente. Historische Verzeichnisse sind nicht automatisch aktiv. Maximal fünf Experimente dürfen gleichzeitig aktiv sein. Der aktuelle Bestand wird im README bewusst nicht gespiegelt, damit kein zweiter, schnell veraltender Status entsteht.

```bash
python3 scripts/docmeta/validate_active_experiments.py
```

Der Validator bindet jeden aktiven Eintrag entweder an das historische bzw. experimentweite `results/decision.yml` oder, wenn die aktive Phase eine aktuelle Entscheidung benötigt, an ein genau einstufiges numerisches `pN/decision.yml`. Beide Pfade sind kanonische Decision Records und verwenden dasselbe Decision-Schema, dieselbe Taxonomie und dieselbe CI-Validierung. Solange ein Experiment aktiv ist, ist sein `source_ref` in `experiments/active.v1.json` die einzige aktuelle Decision-Bindung; nach Verlassen des Registers gilt das numerisch höchste kanonische `pN/decision.yml`, mit Rückfall auf `results/decision.yml` nur ohne vorhandene `pN`-Decision. Historische frühere Entscheidungen werden nicht umgeschrieben. Bei registrierten Experimenten müssen Verbraucher, Entscheidungsfrage, primäre Messgröße, Reviewdatum und Ablaufdatum exakt mit der Registrierung übereinstimmen. Neue Ordner benötigen unabhängig von ihrem Datumspräfix den aktuellen v2-Vertrag; nur die beim T005-Preimage bereits vorhandenen Experiment-IDs bleiben als geschlossener Altbestand kompatibel.

Neue Experimente verwenden `registration.v2.json`. `tools/vibe-cli/admit_natural_case.py` akzeptiert jeden aktuell gültigen v2-Vertrag, prüft ihn über denselben semantischen Registration-Gate wie Capture/Evaluation und friert natürliche Fälle vor Planung oder Ausführung create-only ein. Enthält die Registrierung den begrenzten `stratified_permuted_blocks.v1`-Assignment-Vertrag, wird die Condition innerhalb der registrierten Vergleichsstrata deterministisch balanciert; andernfalls bleibt eine ausdrücklich vorab belegte Condition nötig. `tools/vibe-cli/capture_effect_observation.py` bindet Beobachtungen an Evidenz und gegebenenfalls den Admission-Beleg; Capture und Evaluation berechnen dessen Registrierungs-, Request-, Assignment- und Review-Bindungen erneut, statt nur dem JSON-Dokument zu vertrauen. `tools/vibe-cli/evaluate_effect.py` verbindet die Vergleichsevidenz deterministisch mit den eingefrorenen Ergebnisgrenzen und der registrierten reviewed Closure-Zuordnung. Diese Werkzeuge sind Review-Werkzeuge und besitzen keine automatische Task-, Policy-, Routing-, Queue-, Merge-, Closure- oder Runtime-Autorität.

### Lokal validieren

```bash
python3 -m pip install -r requirements.txt
make validate
```

## Drei Phasen, aufsteigende Strenge

| Phase | Ort | Anforderung | Charakter |
|-------|-----|-------------|-----------|
| **Roh** | `raw-vibes/` | Keine | Beobachtung oder Idee ohne Wirkungsanspruch |
| **Experiment** | `experiments/` | Verbraucher, Registrierung, Methode, Evidenz, Ablauf | Prospektiv und überprüfbar |
| **Bibliothek** | `catalog/`, `prompts/adopted/` | Vollständige Validierung und realer Verbraucher | Bewusst übernommene Praxis |

**Prinzip:** Leicht am Eingang, hart am Ausgang.

## Projektstruktur

```text
labor/
  raw-vibes/                      # Rohe Ideen, Notizen, Fragmente
  experiments/                    # Registrierte Tests und historisches Archiv
  catalog/                        # Validierte, konsumierte Erkenntnisse
  prompts/                        # Menschenlesbare Bibliotheksartefakte
  benchmarks/                     # Vergleichsaufgaben
  instruction-blocks/             # Portable Denkbausteine
  decisions/                      # Meta- und Abschlussentscheidungen
  docs/                           # Grundlagen, Pläne, Berichte und Playbooks
  contracts/                      # Kanonische und policy-nahe Verträge
  schemas/                        # Validierungsschemas
  scripts/                        # Guard- und Generatorstack
  tests/                          # Fixture- und Contract-Tests
  tools/                          # Begrenzte CLI-Werkzeuge
  exports/                        # Generierte Kompatibilitätsflächen
  .vibe/                          # Repo-operative Verträge
```

## Zuständigkeitsgrenze

Labor darf:

- eine prospektive Vergleichsfrage registrieren;
- Beobachtungen an Evidenz binden;
- Claims, Vergleichbarkeit, Unsicherheit und Nichtaussagen prüfen;
- wiederkehrende Reibung als Vorschlag für das Bureau dokumentieren;
- Experimente fördern, pilotieren, zurückstellen, verwerfen oder archivieren.

Labor darf nicht:

- die nächste Aufgabe auswählen;
- Bureau-Queues verändern;
- Pull Requests mergen oder Dienste deployen;
- GitHub-, CI-, Runtime- oder RepoGround-Wahrheit überschreiben;
- aus einer einzelnen Beobachtung eine allgemeine Regel machen.

## Steuerung und Wahrheitshierarchie

| Dokument | Zweck | Status |
| --- | --- | --- |
| `repo.meta.yaml` | Maschinenlesbare Repo-Verfassung | Kanonisch |
| `AGENTS.md` | Bindende Leseregeln | Kanonisch |
| `agent-policy.yaml` | Operative Agentengrenzen | Kanonisch |
| `.vibe/pr-scope-policy.yml` | PR-Scope- und Artifact-Boundary-Policy | Kanonisch |
| `docs/foundations/vision.md` | Begrenztes Zielbild | Grundlagendokument |
| `docs/foundations/repo-plan.md` | Architektur- und Umsetzungsrahmen | Grundlagendokument |
| `experiments/active.v1.json` | Laufende Experimentwahrheit | Operativ, validiert |

**Wahrheitshierarchie:**

1. kanonische Steuerungsquellen — `repo.meta.yaml`, `AGENTS.md`, `agent-policy.yaml`, `.vibe/pr-scope-policy.yml`, `contracts/*`, `schemas/*`;
2. Grundlagenquellen — `docs/foundations/vision.md`, `docs/foundations/repo-plan.md`;
3. operative Dokumente und aktive Experimentwahrheit;
4. Navigation;
5. generierte Diagnoseflächen.

## Weiterführend

- [Contributing](CONTRIBUTING.md)
- [Vision](docs/foundations/vision.md)
- [Optimierungsplan](docs/plans/vibe-lab-optimization-plan-v1.md)
- [Produktive Zuständigkeitsgrenze](docs/ecosystem/vibe-lab-productive-role.md)
- [Validatorinventar und Survivor-Status](docs/reports/vibe-lab-validator-inventory-v1.md)
- [Dokumentation](docs/index.md)
