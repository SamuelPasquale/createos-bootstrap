# CreateOS Bootstrap (C01)

**CreateOS — Cognitive Creation Environment (CCE).**
This repository holds **C01 — CreateOS Bootstrap**: the minimal, Git-backed prototype that proves the CreateOS abstractions (Creations, memory, deterministic tools, and agentic execution).

---

## Purpose

C01 demonstrates a working CreateOS model:

- A Git-backed artifact graph for a single **Creation**.
- Deterministic tooling for memory and task management.
- Dual runtime modes: V0.5 (primary) and V0 (fallback) for resilient, auditable agentic execution.

---

## Runtime Mode

CreateOS Bootstrap supports **two runtime modes** to ensure both operational excellence and resilience:

### Primary Runtime: V0.5 (GitHub Copilot)

**Status**: Implemented and operational (primary as of 2025-12-12)

V0.5 uses GitHub Copilot Spaces and Agents for streamlined, single-phrase session bootstrap:

- **Architect** (Copilot Space) — Cognitive reasoning layer; rehydrates Creation state, produces work packages
- **Developer** (Copilot Agent) — Execution layer; implements PRs with explicit diffs and tests

**Session bootstrap**: Type `start createOS` in Architect Space → run GitHub Action → get readiness summary

**Key references**:
- Architect prompt: [`creation/04-artifacts/agent-prompts/architect-prompt.md`](creation/04-artifacts/agent-prompts/architect-prompt.md)
- Developer prompt: [`creation/04-artifacts/agent-prompts/developer-prompt.md`](creation/04-artifacts/agent-prompts/developer-prompt.md)
- Runtime scope: [`creation/04-artifacts/v0.5-runtime-scope.md`](creation/04-artifacts/v0.5-runtime-scope.md)
- GitHub Action: [`.github/workflows/start-session.yml`](.github/workflows/start-session.yml)

### Fallback Runtime: V0 (Dual-Chat + Git-Backed Tools)

**Status**: Maintenance mode (retained for fallback and troubleshooting)

V0 uses a dual-chat pattern with manual Git-backed tooling:

- **Architect** (ChatGPT Project with GitHub connector) — Cognitive reasoning layer
- **Developer** (Codex with GitHub access) — Execution layer

**Session bootstrap**: Attach GitHub connector → move chat to Project → paste SHA → load index/memory

**Key references**:
- Session protocol: [`creation/06-decisions/session-start-protocol.md`](creation/06-decisions/session-start-protocol.md)
- Close session tool: [`tools/close_session.py`](tools/close_session.py)
- Warm-start via: `creation/08-progress/LATEST.json` (future)

**V0 policy**: No new features; maintenance-only for reliable fallback.

**When to use V0**:
- GitHub Copilot unavailable or degraded
- Emergency troubleshooting requiring manual control
- Historical reference for V0 design patterns

---

## Repository structure (authoritative)

- `creation.yaml` — Creation descriptor (metadata, owners, status).  
- `creation/` — All project state:
  - `01-goals/` — high-level goals and intent.
  - `02-roadmap/` — roadmap (V0 → V1 → platform).
  - `03-v0/` — V0 functional spec and demo criteria (maintenance mode).
  - `04-artifacts/` — generated artifacts, specs, and agent prompts.
  - `05-memory/` — structured, append-only memory (`memory.md`).
  - `06-decisions/` — architectural decisions and protocols.
  - `07-tasks/` — task graph (`tasks.json`).
  - `08-progress/` — dated session logs.
- `tools/` — operational scripts (index refresh, session management).
- `.createos/index.json` — canonical file index (CI generated).

For detailed file placement conventions, see: [`creation/06-decisions/file-placement-conventions.md`](creation/06-decisions/file-placement-conventions.md)

---

## V0 Bootstrapping Workflow (Fallback Mode)

This workflow describes the **V0 dual-chat bootstrap** process, retained as a fallback when V0.5 (Copilot) is unavailable. For primary runtime, see **Runtime Mode** section above.

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

## Session Manager Design (Superseded by V0.5)

**Status**: Design only — superseded by V0.5 runtime (T009)

This project previously documented a Session Manager service design for CreateOS-native session startup, captured in `creation/04-artifacts/session-manager-mvp.md`. That design has been **superseded** by the V0.5 Copilot runtime implementation, which achieves session bootstrap via GitHub Actions and agent prompts.

**Original intent** (now superseded):
- Session Manager: issue short-lived per-session tokens, provide repo metadata, and record bootstrap traces
- Consent UI: human consent flow for least-privilege connector authorization and revocation
- Persistent Memory Service: append-only, versioned Creation memory with read/write APIs
- Resume Creation UX: single-click flow that validates index and rehydrates memory

**Current approach** (V0.5):
- Session bootstrap via GitHub Action (`.github/workflows/start-session.yml`)
- Boot JSON auto-committed to `creation/04-artifacts/boot/LATEST.json`
- Architect reads boot report and emits readiness summary
- Git-backed memory and progress logs (no separate service required)

**Historical reference**: See `creation/04-artifacts/session-manager-mvp.md` for the original design. Task T005 is marked as `superseded` in `creation/07-tasks/tasks.json`.

---

## Quick commands

- Refresh the canonical index (if you modify repo files): `python tools/refresh_index.py`
- Copy the HEAD SHA of `main`: `git rev-parse HEAD`

---

## Where to find authoritative docs

**V0.5 Runtime (Primary)**:
- V0.5 runtime scope: `creation/04-artifacts/v0.5-runtime-scope.md`
- Architect prompt: `creation/04-artifacts/agent-prompts/architect-prompt.md`
- Developer prompt: `creation/04-artifacts/agent-prompts/developer-prompt.md`
- GitHub Action: `.github/workflows/start-session.yml`

**V0 Runtime (Fallback)**:
- Session protocol: `creation/06-decisions/session-start-protocol.md`
- Close session tool: `tools/close_session.py`

**General**:
- File placement conventions: `creation/06-decisions/file-placement-conventions.md`
- Memory model: `creation/05-memory/memory.md`
- Task graph: `creation/07-tasks/tasks.json`
- Tools & scripts: `tools/refresh_index.py`, `tools/add_memory_entry.py`, `tools/start_session.py`

---

## Philosophy

CreateOS is a **Cognitive Creation Environment (CCE)**: we work on *Creations*, not files. This repo is a narrow bootstrap proving the architecture for long-term, human+AI co-creation.

**Ritual**: Once a session is loaded and online, the Architect starts with:

> “Let’s build.”

---

(End of README)
