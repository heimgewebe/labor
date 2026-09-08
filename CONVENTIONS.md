# CONVENTIONS.md — Anker für Aider und ähnliche Agenten

> Dieses Dokument ist ein **Anker für Aider-Agenten**. Es ist kein
> kanonischer Inhalt. Die kanonische Quelle ist [`AGENTS.md`](AGENTS.md).

## Pflicht-Leseordnung

1. [`repo.meta.yaml`](repo.meta.yaml)
2. [`AGENTS.md`](AGENTS.md)
3. [`agent-policy.yaml`](agent-policy.yaml)
4. [`docs/roadmap.md`](docs/roadmap.md)
5. [`README.md`](README.md), [`docs/index.md`](docs/index.md)
6. `contracts/`, `schemas/`, `.vibe/`

## Leitplanken

- `repo.meta.yaml`, `AGENTS.md`, `agent-policy.yaml` und
  `.vibe/pr-scope-policy.yml` sind kanonisch und **maschinell pflegbar**.
  Änderungen müssen explizit auslösergebunden, scopesicher und durch die
  normalen Review-, CI- und Traceability-Gates abgesichert sein.
- **Keine direkten Edits** an generator-owned Artefakten:
  `docs/_generated/*`, `exports/*`, `.cursor/rules/*`; Änderungen erfolgen
  ausschließlich über die kanonischen Generatoren.
- **Keine Status-Umdeutung** ohne Belege.
- **Keine Promotion** ohne Gate.

## Workflow

1. Vor Aktionen: kanonische Quellen lesen (siehe oben).
2. Vor Commit: `make agent-check` für den schnellen Generator-Artefakt-Guard, `make validate` für das volle Gate.
3. Bei Konflikten: Stopp und Meldung — nicht raten.

## Vollständige Regeln

- Bindend: [`AGENTS.md`](AGENTS.md)
- Compliance-Policy: [`docs/policies/agent-compliance.md`](docs/policies/agent-compliance.md)
- Operative Constraints: [`.vibe/constraints.yml`](.vibe/constraints.yml)