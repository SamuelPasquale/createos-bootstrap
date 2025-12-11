# Session Start Protocol — C01: CreateOS Bootstrap

**Status:**  
- **V0 protocol: Implemented and operational (canonical today).**  
- **CreateOS-native protocol (Session Manager): Design only — not implemented.**

This document defines how to start and close a CreateOS Architect session in V0, using current ChatGPT and GitHub platform constraints, and records the *planned* CreateOS-native session startup design as an appendix.

---

## 1. Purpose

Provide a **single, deterministic way** to:

1. Start an Architect session that has read access to the repository and can reconstruct Creation state from Git-backed artifacts.
2. Close a working session in a way that updates progress logs, tasks, and memory so the next session can **warm-start** from the backend alone (even if chats are deleted).
3. Document the **future** CreateOS-native session startup (Session Manager + Consent + Persistent Memory) as **design-only** for v1 and beyond.

---

## 2. Roles (V0)

- **Architect** — ChatGPT Project session (cognitive layer).  
  Reads the repo, reconstructs state, provides reasoning, and produces structured instructions.

- **Developer (Codex)** — ChatGPT Codex chat with GitHub enabled (developer layer).  
  Applies changes to the repo, opens PRs, and runs operational tooling.

- **GitHub Repo** — System of record.  
  Stores all state necessary to reconstruct the Creation between sessions.

---

## 3. Preconditions (V0)

- Repository: `SamuelPasquale/createos-bootstrap` (branch: `main`).
- `.createos/index.json` exists and is maintained by CI.
- A chat can **only** attach GitHub when **outside** a Project.
- Therefore, the Architect session must be created by:
  1. Opening a chat **outside** the CreateOS Project.  
  2. Attaching GitHub via Company Knowledge → GitHub.  
  3. **Moving** that chat into the Project (retaining GitHub access).

---

## 4. Canonical V0 Session Start Protocol (Dual-Chat Boot)

This is the **only supported, working session startup protocol** today.

### 4.1 Step 1 — Create a repo-enabled chat outside the Project

1. Open a brand-new chat **outside** the CreateOS Project.  
2. Use **Company knowledge → GitHub** to attach the repository:  
   `SamuelPasquale/createos-bootstrap`
3. Confirm GitHub access by fetching any file (e.g. `README.md`).

If GitHub attachment fails, **stop**. The Architect cannot proceed.

---

### 4.2 Step 2 — Move the chat into the CreateOS Project

1. Move the GitHub-enabled chat into the CreateOS Project.  
2. The chat **retains** its GitHub connector and becomes the:

   **Architect + Repo Access Session (V0)**

All Architect work **must occur in this chat**.

---

### 4.3 Step 3 — Human issues the canonical boot message

1. Human obtains latest SHA of `main` using:  
   `git rev-parse HEAD`
2. Human posts the canonical boot command:

```
Latest SHA: <paste HEAD SHA>
Load the repo.
```

This message is the explicit **boot trigger**.

---

### 4.4 Step 4 — Architect deterministic reconstruction (V0)

Upon receiving the boot message, the Architect must:

1. **Validate repository attachment**  
   Confirm GitHub is attached and `repo_full_name = SamuelPasquale/createos-bootstrap`.

2. **Validate the commit SHA**  
   - Fetch commit metadata.  
   - If invalid, request corrected SHA from the human.

3. **Load `.createos/index.json`**  
   - If load fails, request the human to paste the file.  
   - The pasted index is **authoritative for this session**.

4. **Enumerate and load core Creation state** using the index:
   - `creation.yaml`
   - Specs in `creation/03-v0/`
   - Memory in `creation/05-memory/memory.md`
   - Decisions in `creation/06-decisions/`
   - Tasks in `creation/07-tasks/tasks.json`
   - Progress logs in `creation/08-progress/`

5. **Fast path: Load `creation/08-progress/LATEST.json` if present**
   - Treat it as the authoritative summary of the previous session:
     - `date`
     - `file`
     - `sha`
     - `summary`
     - `next_steps`
   - If missing/invalid, fall back to the most recent dated log by filename.

6. **Reconstruct cognitive state**
   - Goals & roadmap
   - Latest progress summary
   - Open & completed tasks
   - Decisions
   - Memory entries relevant to recent changes

7. **Declare readiness** with:
   1. Confirmation of the SHA in use  
   2. Summary of last progress (from `LATEST.json` or latest dated log)  
   3. List of open tasks / next steps  
   4. Proposed action plan for the current session

Only after this step is the session considered **booted**.

---

## 5. V0 Session Close Protocol (End-of-Day Save)

The canonical end-of-session workflow in V0 is performed by:

**`tools/close_session.py`**

This script is the V0 equivalent of a **Save & Close** operation.

Example:

```
python tools/close_session.py \
  --summary "Implemented progress logs and session protocol" \
  --completed T004 \
  --next T005,T006 \
  --sha <HEAD_SHA>
```

### 5.1 What `close_session.py` does

1. **Writes a dated progress log**  
   - `creation/08-progress/YYYY-MM-DD.md`

2. **Updates LATEST.json**  
   - File: `creation/08-progress/LATEST.json`  
   - Contains:  
     - date  
     - file  
     - sha  
     - summary  
     - next_steps  
     - generated_at

3. **Updates tasks**  
   - Marks any tasks listed via `--completed` as `"complete"` in `creation/07-tasks/tasks.json`.

4. **Appends to memory**  
   - Writes a structured memory entry (`event: session_close`) to `creation/05-memory/memory.md`.

After this script is run and committed, **all session state is preserved in Git** and the chat may be safely deleted.

---

## 6. Error Handling (V0)

**No GitHub attachment**  
Architect responds:  
> No GitHub repository is attached. Please attach `SamuelPasquale/createos-bootstrap` via the GitHub integration in a new chat *outside* the Project, then move the chat into the Project.

**Invalid SHA**  
- Request new SHA via `git rev-parse HEAD`.

**Cannot fetch `.createos/index.json`**  
- Architect requests a pasted copy.  
- Pasted copy becomes authoritative for the session.

**Missing required files**  
- Architect identifies missing components.  
- If critical (e.g. `creation.yaml`), halt and request fix.  
- If non-critical, may continue in *read-only degraded mode*.

**close_session failure**  
- Architect warns user and requests manual intervention or file repair.

---

## 7. CreateOS-Native Session Startup (Design Only — Not Implemented)

**Do not treat any portion of this section as V0 behavior.  
This is the v1 architecture target.**

### 7.1 Intent

Replace the V0 dual-chat hack with:

- A **Session Manager** service
- A **Consent UI**
- A **Persistent Memory Service**
- A one-click **Resume Creation** UX

The design is detailed in:

- `creation/04-artifacts/session-manager-mvp.md`
- Architecture docs in `creation/04-artifacts/`

---

### 7.2 Planned (non-functional) V1 flow

1. Architect requests session from Session Manager with desired scopes.
2. Human approves scopes via Consent UI.
3. Session Manager issues:
   - signed session token  
   - connector handle  
   - repo metadata  
   - memory endpoint

4. Architect validates token, mounts repo & memory, loads index, rehydrates memory.
5. Architect registers a bootstrap trace with Session Manager.
6. Developer tags all PRs/commits with `session_id`.
7. `close_session` becomes a durable API call to the Session Manager.
8. Human can revoke sessions at any time.

---

### 7.3 Transitional Guidance

- **V0 dual-chat protocol remains mandatory** until the Session Manager exists.
- The native protocol should be considered **roadmap documentation only**.
- When v1 is implemented, this file will be updated accordingly.

---

(End of protocol)
