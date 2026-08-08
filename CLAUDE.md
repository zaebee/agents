# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Two related bodies of work live side by side, with no build system, package manager, or test suite:

1. **ElizaOS character configs** (`*.json` at the repo root) — declarative agent definitions consumed by the [ElizaOS](https://eliza.how/docs) framework.
2. **"The Hive"** — an architecture specification written as a fable, plus a bash scaffolding CLI and empty component skeletons that demonstrate it.

Nothing here compiles or runs as an application. The Python files under `hive/components/` are **intentionally empty placeholders** produced by the scaffolder — do not treat them as broken or fill them in unless asked.

## Commands

```bash
# Scaffold a new Hive component ("hatch a codon"). Must be run from the repo root —
# HIVE_ROOT is the relative path "hive/components".
./genesis-engine/hive-cli hatch command <name>   # C -> A -> G  (connector, command, aggregate, event)
./genesis-engine/hive-cli hatch query   <name>   # C -> T -> C  (connector, query, transformer, dto)
./genesis-engine/hive-cli hatch event   <name>   # G -> C -> A -> G (listening_connector, command, aggregate, new_event)

# Formatting — Markdown/HTML/JSON are kept prettier-formatted (see "chore: run prettier" commits).
npx prettier --write <files>

# Render a Mermaid block to SVG (cover.md documents this workflow)
mmdc -i cover.md -o cover.svg
```

There is no test runner. `static.yml` publishes the repository to GitHub Pages on every push to `main`, **minus a short deny list** — currently `drafts/`, `CLAUDE.md`, `.github/` and `.git`. Anything else you add, at the root or in a subdirectory, goes public on merge. Adding something private means adding it to that list in the same commit.

Note the deploy does **not** run Jekyll: `upload-pages-artifact` tars the staged tree verbatim, so YAML front matter is served as literal text and `_config.yml` would do nothing. `jekyll-docker.yml` builds a Jekyll site but never deploys it.

## The Hive architecture (what you need to hold in your head)

The whole spec is one metaphor consistently applied. Read `dna-core/PATTERNS.md` first — it is the technical, non-fable statement of everything below.

**ATCG primitives** — the four building blocks every component decomposes into:

| Letter | Primitive | Role |
| --- | --- | --- |
| **A** | Aggregate | Consistency boundary; owns invariants. State changes only via `apply(event)`. |
| **T** | Transformation | Pure, stateless function/domain service. No side effects. |
| **C** | Connector | Hexagonal-architecture adapter (REST, DB, queue). Translates outside ↔ domain. |
| **G** | Genesis Event | Immutable past-tense record of what happened. |

**Codons** — the three legal compositions of those primitives. Each `hive-cli hatch` type maps to exactly one:

- `C -> A -> G` **Handle Command** — the *only* pattern permitted to mutate state.
- `C -> T -> C` **Query Data** — reads and projects; never emits events.
- `G -> C -> A -> G` **React to Event** — cross-cell choreography.

**Pollen Protocol** (`dna-core/pollen_protocol.proto`) — the required envelope for every Genesis Event crossing a cell boundary: `event_id`, `event_type`, `event_version`, `timestamp`, `aggregate_id`, `payload`. Any new event schema must fit this envelope.

**Manifests** — a component's `manifest.yaml` (see `hive/components/TestBee/manifest.yaml`, `test-bee.yaml`) is treated as an *ontological declaration*, not config: identity (`name`), purpose (`description`), and relationships (`listens_to`, `produces`, `connectors`). It is the source of truth for a component's role.

Two rules from `CONTRIBUTING.md` that constrain implementation work:

- Write **Codeons** — small, named, pure-where-possible functions composed into larger logic, never monolithic functions.
- The environment (env vars, flags) may act as a **switch** selecting which code paths express, but must **never be the source** of logic. No `eval()` on environment input.

## Document map and how the docs relate

- `HIVE_CONSTITUTION.md` — canonical architecture doc, written as the fable "The Tale of the Enchanted Apiary".
- `article.md` / `article.ru.md` — the same fable as a publishable article (Russian translation included). **`article.md` and `HIVE_CONSTITUTION.md` have drifted apart** — each contains sections the other lacks. When editing shared prose, decide deliberately which is authoritative rather than assuming they are copies.
- `article.html` / `article.ru.html` — hand-styled HTML renderings (honey palette CSS, Mermaid loaded from CDN). They are not generated from the `.md` files by any script; changes must be mirrored by hand.
- `GRIMOIRE.md` — the seven zoom levels (Organism → Cell → Codon → ATCG → Codeon → Physics → Intent).
- `codons.md` — the three codons with Mermaid diagrams.
- `MCP_DRAFT.md` — the Multi-Agent Communication Protocol draft (FIPA-ACL-inspired: `performative`, `sender`, `receiver`, `in_reply_to`, `ontology`, `payload`).
- `gardener.md` — v2.0.0 system prompt for the "Hive Gardener" persona; adds homeostasis metrics (τ tension, Σ attention budget, mutation costs per ATCG type).
- `journey-diagram.md`, `cover.md`, `genesis-animation.html` — standalone visual assets.

Prose in this repo is deliberately metaphorical. Match that register when editing the fable documents; use plain technical language in `dna-core/`, `CONTRIBUTING.md`, and code.

## Agent character files

`Eddy.json` (ElizaOS developer support), `Jules.json` (software engineer), `Eliza.json` (general persona), `Beekeeper.json` (name: "Hive Gardener", the architecture agent). Shared shape: `name`, `system`, `bio`, `lore`, `messageExamples`, `style`, `topics`, `plugins`, `clients`, `modelProvider`, and for some, `actions`.

**Gotcha: `Eddy.json` and `Jules.json` are not strict JSON.** They contain `//` line comments inside `messageExamples` (e.g. `Eddy.json:226`, `Jules.json:74`) and will fail `json.load` / `JSON.parse`. `Eliza.json` and `Beekeeper.json` parse fine. Do not "fix" the comments away without checking the intent — they annotate the MCP proof-of-concept payloads. Use a JSONC-tolerant parser when you need to read them programmatically.

The MCP work is a **simulation**: agent actions (`DELEGATE_CODING_TASK_TO_JULES` in Eddy, `EXECUTE_DELEGATED_CODING_TASK` in Jules, `EXECUTE_SYSTEM_HEALTH_CHECK` in Beekeeper) *log* the MCP messages they would send rather than using any real transport. Keep that convention when extending the PoC.
