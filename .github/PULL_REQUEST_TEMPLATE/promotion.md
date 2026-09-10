## Promotion — Aufnahme in die Bibliothek

### Ziel
- [ ] **Catalog Entry** in `catalog/`
- [ ] **Combo** in `catalog/combos/`
- [ ] **Prompt** in `prompts/adopted/`

### Referenzen
- **Experiment:** `experiments/<name>/`
- **Issue:** #<!-- Nr -->
- **Evidenz:** `experiments/<name>/results/evidence.jsonl`
- **Consumer:** <!-- Konkreter realer Verbraucher, z. B. owner/repo:surface -->
- **Decision Target:** <!-- Welche konkrete Entscheidung oder Arbeitsaktion soll die Promotion beeinflussen? -->

### Promotion-Gate Checkliste

- [ ] Experiment ist vollständig durchgeführt
- [ ] `CONTEXT.md` und `INITIAL.md` sind vorhanden und vollständig
- [ ] `evidence.jsonl` enthält mindestens einen maschinenlesbaren Eintrag
- [ ] `decision.yml` enthält `decision_type: adoption_assessment` und `verdict: adopt` (Decision-Type-Separation gem. `execution-bound-epistemics.md §10.1`; impliziert `execution_status ∈ {executed, replicated}` — durch `validate_schema.py` cross-file erzwungen)
- [ ] Begriffsabgrenzung ist konsistent: `adopt` ist der Decision-Verdict-Wert; `adopted` ist der daraus folgende Status/Lifecycle-Zustand
- [ ] Manifest enthält `adoption_basis`: `executed` oder `replicated` bei neuen Promotions. `reconstructed` ist **nur für Altbestand** mit expliziter Legacy-Begründung zulässig (siehe `docs/blueprints/blueprint-v2.md` → Übergangsregel)
- [ ] Falls `execution_status ∈ {executed, replicated}`: `artifacts/<run-id>/run_meta.json` vorhanden und schema-valide; `test_output_file` existiert
- [ ] Schema- und Execution-Proof-Validierung bestanden (`make validate`)
- [ ] Katalogeintrag / Prompt / Combo liegt im korrekten Zielordner
- [ ] Ein konkreter realer Consumer und ein konkretes Decision Target sind benannt
- [ ] Für `prompts/adopted/`: Frontmatter enthält nicht-leere `consumer`- und `decision_target`-Felder sowie eine `validated_by`-Relation auf bestehende Evidenz unter `experiments/**/results/`
- [ ] Frontmatter entspricht dem jeweiligen Schema (`catalog.entry.schema.json` / `combo.schema.json` / `docmeta.schema.json` für Prompts)
- [ ] Keine manuellen Edits an generierten Artefakten

### Evidenz-Zusammenfassung
<!-- Kurze Zusammenfassung: Warum ist diese Praxis promotionswürdig? Belege aus evidence.jsonl. -->

### Aufwertungsbegründung

- **Grundlage:** <!-- Worauf stützt sich die Aufwertung? (Experiment, Evidenz, Replikation) -->
- **Unsicher bleibt:** <!-- Was bleibt offen, ungetestet oder kontextschmal? -->
- **Warum jetzt trotzdem:** <!-- Warum reicht die Grundlage für diesen Geltungssprung jetzt aus? -->
- **Alternative Lesart (optional):** <!-- Plausible alternative Deutung bei hoher Tragweite -->

### Reviewer-Hinweise
<!-- Besonderheiten, Einschränkungen, bekannte Limitationen -->
