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

## Daily Start Sequence (CreateOS)

CreateOS is a stateful environment. Each session must anchor itself to a specific Git commit and the current index.

### Troubleshooting: ChatGPT cannot read the repository

If a standard ChatGPT conversation cannot see files ("I can't access your repository"), follow these steps:

1. Use a **ChatGPT Project** instead of a plain chat so the GitHub connector can mount the repo.
2. In the Project sidebar, verify the **Active repository** is `SamuelPasquale/createos-bootstrap`. If not, attach it and reload the chat.
3. Ask the assistant to list the root files (e.g., `ls`) to confirm access before giving work instructions.
4. If access is still blocked, start a new Project chat and re-attach the repository; ChatGPT-only conversations without a Project cannot read repo files.

### 0. Attach the GitHub repository

Ensure the GitHub integration is active for this ChatGPT project and that the correct repository is selected as the active Creation:

> Active repo: `SamuelPasquale/createos-bootstrap`

Without an attached repository, CreateOS cannot read `.createos/index.json` or any Creation files and cannot reconstruct state.

### 1. Refresh the index

```bash
python tools/refresh_index.py
```

This regenerates `.createos/index.json`, the canonical map of the Creation.

### 2. Capture the current commit SHA

```bash
git rev-parse HEAD
```

Copy this SHA. It identifies the exact state of the system.

### 3. Start a CreateOS session

Provide to the system:

- The latest SHA  
- A request to load the current project state  

Example:

> Latest SHA: `<sha>`.  
> Load the latest progress log and current project state.

### 4. What CreateOS reconstructs

Using `.createos/index.json`, the system loads:

- Creation definition (`creation.yaml`)
- V0 specs (`creation/03-v0/*.md`)
- Memory (`creation/05-memory/memory.md`)
- Decisions (`creation/06-decisions/*.md`)
- Tasks (`creation/07-tasks/tasks.json`)
- Progress logs (`creation/08-progress/*.md`)

### 5. Begin work

Once the environment is loaded:

> "Let's build."

For the full detailed protocol, see  
`creation/06-decisions/session-start-protocol.md`.

