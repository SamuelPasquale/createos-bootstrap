# CreateOS Bootstrap (C01)

This repository hosts the first working Creation for CreateOS: **C01 – CreateOS Bootstrap**.

The purpose of this Creation is to:

- Establish a minimal Git-backed filesystem for CreateOS.
- Implement deterministic tools for memory and task management.
- Demonstrate a V0 demo where CreateOS modifies its own artifacts and specifications.

## Structure

- `creation.yaml` – Top-level descriptor for the Creation.
- `creation/` – All state for this Creation.
  - `01-goals/` – High-level goals and intent.
  - `02-roadmap/` – Roadmap documents (V0 → V1 → Platform → Enterprise).
  - `03-v0/` – V0 functional spec, demo script, acceptance criteria.
  - `04-artifacts/` – Generated artifacts (design docs, schemas, etc.).
  - `05-memory/` – Structured memory log (`memory.md`).
  - `06-decisions/` – Architectural decisions and rationale.
  - `07-tasks/` – Task graph (`tasks.json`).
- `tools/` – Scripts and utilities for operating on the Creation.
- `references/` – Strategic and thesis documents used for context.

This repo is intentionally narrow in scope. It exists to **bootstrap** CreateOS itself.


## Working on This Creation (Daily Session Start)

To resume work on CreateOS Bootstrap (C01) in a new ChatGPT session:

1. Open this repo on GitHub (`main` branch) and copy the **latest commit SHA**.
2. Open a new chat in the CreateOS ChatGPT Project.
3. Paste the SHA and say something like:

   > Latest SHA: `<paste here>`  
   > Load the latest progress log and current project state.

Behind the scenes:

- `.createos/index.json` (auto-maintained by GitHub Actions) is used as the
  canonical file index.
- Daily progress logs live under `creation/08-progress/`.
- The assistant uses the index + latest progress log to restore context and
  propose the next action.

For full details, see:
`creation/06-decisions/session-start-protocol.md`.
