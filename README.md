# CreateOS Bootstrap (C01)

**CreateOS — Cognitive Creation Environment (CCE).**
This repository holds **C01 — CreateOS Bootstrap**: the minimal, Git-backed prototype that proves the CreateOS abstractions (Creations, memory, deterministic tools, and agentic execution).

---

## Purpose

C01 demonstrates a working V0 of the CreateOS model:

- A Git-backed artifact graph for a single **Creation**.
- Deterministic tooling for memory and task management.
- A V0 runtime where an Architect (ChatGPT Project) and a Developer (Codex) collaborate to read, design, and modify the backend repo.

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

This workflow is the **official, working** way to start deterministic CreateOS sessions for C01 *today* (V0), using the platform constraints we validated. **Do not replace these instructions** — they are the authoritative daily process until the CreateOS-native runtime is implemented.

**Roles**
- **Architect (this ChatGPT Project)** — cognitive, long-horizon reasoning: designs creation intents, session protocols, and briefs Codex.
- **Developer (Codex / GitHub-enabled chat)** — reads the live repo, generates diffs, and opens PRs.

**Bootstrapping steps (V0)**
1. **Create a repo-enabled chat outside the CreateOS Project**
   - Open a new ChatGPT chat (not in the Project).
   - Use **Company knowledge → GitHub** to attach `SamuelPasquale/createos-bootstrap`. Confirm read access by fetching `README.md` or `creation/06-decisions/session-start-protocol.md`.
2. **Move the repo-enabled chat into the CreateOS Project**
   - After moving, this chat retains the GitHub source and becomes the persistent **Architect + Repo Access** session. This session is the canonical Architect workspace for V0.
3. **Human: Provide the minimal bootstrap**
   - Copy the latest `main` commit SHA and paste the canonical boot message into the Architect chat:
     ```
     Latest SHA: <paste HEAD SHA>
     Load the repo.
     ```
4. **Assistant: Deterministic reconstruction**
   - Validate repository attachment and confirm `repo_full_name = SamuelPasquale/createos-bootstrap`.
   - Fetch the provided commit metadata and confirm SHA validity.
   - Load `.createos/index.json` (fetch or request a pasted index if needed).
   - Using the index, enumerate and load:
     - `creation.yaml`
     - V0 specs (`creation/03-v0/*`)
     - Memory (`creation/05-memory/memory.md`)
     - Decisions (`creation/06-decisions/*`)
     - Tasks (`creation/07-tasks/tasks.json`)
     - Progress logs (`creation/08-progress/*.md`) — choose most recent or use `creation/08-progress/LATEST.json`
   - Reconstruct cognitive state (goals, progress, outstanding tasks, decisions).
   - Declare readiness with:
     1. Confirmation of SHA
     2. Summary of last progress log
     3. List of open tasks
     4. Proposed next actions
5. **Developer flow (Codex)**
   - Architect produces a precise, self-contained instruction package for Codex describing what to change and why.
   - Codex reads the live repo, shows per-file diffs, opens branch and PR for review.
6. **Review & merge**
   - Architect reviews the PR, requests changes if needed, and merges when ready. CI updates `.createos/index.json` accordingly.

**Notes & fallbacks**
- If the GitHub connector cannot be attached, the fallback is to paste `.createos/index.json` into the Architect chat; the pasted index is authoritative for the session.
- `tools/close_session.py` and `creation/08-progress/LATEST.json` provide a warm-start fast path for daily sessions; consult `creation/06-decisions/session-start-protocol.md` for protocol details.

---

## Planned CreateOS-Native Session Startup (Design only — not implemented)

**Status & scope (Design only)** — This project *documents* a CreateOS-native session startup design (Session Manager, Consent UI, and Persistent Memory) but **the Session Manager and runtime services are not implemented** at this time. The design is captured in `creation/04-artifacts/session-manager-mvp.md` and tracked by the `v1-session-bootstrap` milestone and child issues. Until those services are delivered, the canonical V0 workflow above is the working process to be used today.

**High-level intent**
- Session Manager: issue short-lived per-session tokens, provide repo metadata, and record bootstrap traces.
- Consent UI: human consent flow for least-privilege connector authorization and revocation.
- Persistent Memory Service: append-only, versioned Creation memory with read/write APIs.
- Resume Creation UX: single-click flow that validates index and rehydrates memory.

**Where to read the design**
- Session Manager MVP blueprint: `creation/04-artifacts/session-manager-mvp.md`  
- Session start protocol and v1 tasks: `creation/06-decisions/session-start-protocol.md` and the v1 milestone

**Key note**: This is a design and roadmap entry. Do not rely on the native session startup as being functional until T005–T007 are implemented and the Session Manager is deployed.

---

## Quick commands

- Refresh the canonical index (if you modify repo files): `python tools/refresh_index.py`
- Copy the HEAD SHA of `main`: `git rev-parse HEAD`

---

## Where to find authoritative docs

- Session protocol (native MVP): `creation/06-decisions/session-start-protocol.md`
- Session Manager + Memory blueprint: `creation/04-artifacts/session-manager-mvp.md`
- Memory model: `creation/05-memory/memory.md`
- Tools & scripts: `tools/refresh_index.py`, `tools/add_memory_entry.py`

---

## Philosophy

CreateOS is a **Cognitive Creation Environment (CCE)**: we work on *Creations*, not files. This repo is a narrow bootstrap proving the architecture for long-term, human+AI co-creation.

**Ritual**: Once a session is loaded and online, the Architect starts with:

> “Let’s build.”

---

(End of README)
