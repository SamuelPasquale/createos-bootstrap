# CreateOS Bootstrap (C01)

**CreateOS — Cognitive Creation Environment (CCE).**  
This repository holds **C01 — CreateOS Bootstrap**: the minimal, Git-backed prototype that proves the CreateOS abstractions (Creations, memory, deterministic tools, and agentic execution).

---

## Purpose

C01 demonstrates a working V0 of the CreateOS model:

- A Git-backed artifact graph for a single **Creation**.  
- Deterministic tooling for memory and task management.  
- A V0 runtime where an Architect (ChatGPT Project) and a Developer (Codex) collaborate to read, design, and modify the backend repo.  

> **Important (V0)** — The session bootstrap workflow documented below is a temporary, platform-driven workaround needed to bootstrap V0. We will replace this with a proprietary CreateOS startup sequence in early v1 once the runtime and persistent memory layers are implemented.

---

## Repository structure (authoritative)

- `creation.yaml` — Creation descriptor (metadata, owners, status).  
- `creation/` — All project state:
  - `01-goals/` — high-level goals and intent.
  - `02-roadmap/` — roadmap (V0 → V1 → platform).
  - `03-v0/` — V0 functional spec and demo criteria.
  - `04-artifacts/` — generated artifacts and specs.
  - `05-memory/` — structured, append-only memory (`memory.md`).
  - `06-decisions/` — architectural decisions and protocols.
  - `07-tasks/` — task graph (`tasks.json`).
  - `08-progress/` — dated session logs.
- `tools/` — operational scripts (index refresh, helpers).
- `.createos/index.json` — canonical file index (CI generated).
- `.createos/manifest.json` — **(new)** lightweight manifest describing repo metadata and V0 workflow (created by this PR).

---

## Canonical V0 Bootstrapping Workflow (Architect + Codex)

This workflow is intentionally **temporary** and designed to work with current ChatGPT / Codex platform constraints. It is the official way to start deterministic CreateOS sessions for C01 until we ship a CreateOS-native startup flow.

**Roles**
- **Architect (this ChatGPT Project)** — cognitive, long-horizon reasoning: designs creation intents, session protocols, and briefs Codex.  
- **Developer (Codex / GitHub-enabled chat)** — reads the live repo, generates diffs, and opens PRs.

**Bootstrapping steps (V0)**

1. **Create a repo-enabled chat outside the CreateOS Project**  
   - Open a new ChatGPT chat (not the Project).  
   - Use **Company knowledge → GitHub** to attach `SamuelPasquale/createos-bootstrap`. Confirm read access (e.g., fetch `README.md`).  
2. **Prepare the Architect session**  
   - Once the external chat has GitHub attached, **move the chat into the CreateOS Project**. The moved chat retains the GitHub source and becomes the persistent **Architect + Repo Access** session.  
   - This session is the canonical Architect workspace for V0. It runs the session-start protocol (below) to declare readiness.  
3. **Architect designs & instructs Codex**  
   - Architect produces a precise, self-contained instruction package for Codex describing what files to change and why.  
4. **Codex executes**  
   - In a Codex-enabled developer chat (which has continuous GitHub access), paste the Architect’s instruction package. Codex will read the live repo, produce per-file diffs, open a branch, and create a PR for review.  
5. **Review & merge**  
   - The Architect reviews the PR, requests changes if needed, and merges when ready. CI (if present) updates `.createos/index.json` automatically.

**Notes & fallbacks**
- If the GitHub connector cannot be attached, the fallback is to paste `.createos/index.json` (the CI-generated index) into the Architect chat and continue. The pasted index becomes the canonical index for that session.  
- This V0 process is explicitly temporary. One of the early v1 deliverables is to design a **CreateOS-native session bootstrap** that provides persistent memory, an embedded startup protocol, and direct mounting of the backend without this dual-chat workaround.

**Quick commands**
- Refresh the canonical index (if you modify repo files): `python tools/refresh_index.py`
- Copy the HEAD SHA of `main`: `git rev-parse HEAD`

---

## Where to find authoritative docs

- Session protocol (V0): `creation/06-decisions/session-start-protocol.md`  
- Memory model: `creation/05-memory/memory.md`  
- Tools & scripts: `tools/refresh_index.py`, `tools/add_memory_entry.py`

---

## Philosophy

CreateOS is a **Cognitive Creation Environment (CCE)**: we work on *Creations*, not files. This repo is a narrow bootstrap proving the architecture for long-term, human+AI co-creation.

**Ritual**: Once a session is loaded and online, the Architect starts with:

> “Let’s build.”

---

(End of README)
