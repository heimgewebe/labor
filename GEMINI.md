# GEMINI.md — Anker für Gemini Code Assist

> Dieses Dokument ist ein **Anker für Gemini-Agenten**. Es ist kein
> kanonischer Inhalt. Die kanonische Quelle ist [`AGENTS.md`](AGENTS.md).
> Bei Widersprüchen gilt immer die kanonische Quelle.

## Pflicht-Leseordnung (vor jeder Aktion)

1. [`repo.meta.yaml`](repo.meta.yaml) — Repo-Verfassung
2. [`AGENTS.md`](AGENTS.md) — Bindende Leseregeln
3. [`agent-policy.yaml`](agent-policy.yaml) — Operative Steuerung
4. [`docs/roadmap.md`](docs/roadmap.md) — Strategischer Kontext
5. [`README.md`](README.md), [`docs/index.md`](docs/index.md) — Einstieg und Navigation
6. `contracts/`, `schemas/`, `.vibe/` — Verträge und Restriktionen

Bei Widersprüchen gewinnt die höhere Ebene.

## Kurzregeln

- `repo.meta.yaml`, `AGENTS.md`, `agent-policy.yaml` und
  `.vibe/pr-scope-policy.yml` sind kanonisch und **maschinell pflegbar**.
  Änderungen müssen explizit auslösergebunden, scopesicher und durch die
  normalen Review-, CI- und Traceability-Gates abgesichert sein.
- **Keine direkten Edits** an `docs/_generated/*`, `exports/*`,
  `.cursor/rules/*` (generator-owned; nur über kanonische Generatoren).
- **Keine Status-Änderungen** an Experimenten ohne belegte Grundlage.
- **Keine Promotion** in die Bibliothek ohne Promotion-Gate.
- **Keine erfundenen** Felder oder Konzepte außerhalb der Schemas.

## Eigen-Check

```bash
make agent-check    # schneller Guard gegen direkte Generator-Artefakt-Edits
make validate       # vollständige Validierung
```

## Vollständige Regeln

- [`AGENTS.md`](AGENTS.md) — bindend
- [`docs/policies/agent-compliance.md`](docs/policies/agent-compliance.md) — Compliance-Übersicht