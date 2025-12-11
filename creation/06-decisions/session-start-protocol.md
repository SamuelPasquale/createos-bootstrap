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
  - Reads the repo via GitHub connector.
  - Reconstructs state from `.createos/index.json`, progress logs, tasks, memory, and decisions.
  - Produces structured instructions for the Developer.

- **Developer (Codex)** — ChatGPT / Codex chat with GitHub enabled (developer layer).
  - Reads the live repo.
  - Applies changes, generates diffs, and opens PRs.
  - Runs tools like `tools/refresh_index.py` and `tools/close_session.py`.

---

## 3. Preconditions (V0)

- Repository: `SamuelPasquale/createos-bootstrap` (branch: `main`).
- The repository is reachable via the **GitHub connector** in ChatGPT.
- `.createos/index.json` exists and is the canonical file index (CI generated).
- Session is being run inside the **CreateOS Project**, but the **GitHub connector must be attached *before*** the chat is moved into the Project (due to platform constraints).

---

## 4. Canonical V0 Session Start Protocol (Dual-Chat Boot)

This is the **only supported, working startup sequence today**. All sessions must follow this.

### 4.1 Step 1 — Create a repo-enabled chat outside the Project

1. In ChatGPT, create a **new chat outside** the CreateOS Project.
2. Use **Company knowledge → GitHub** to attach the repo:  
   `SamuelPasquale/createos-bootstrap`
3. Verify access by fetching at least one file (e.g. `README.md` or `creation/06-decisions/session-start-protocol.md`).

If this step fails, **do not** proceed. The Architect requires direct GitHub access.

---

### 4.2 Step 2 — Move the chat into the CreateOS Project

1. Once the chat has GitHub attached and verified, **move this chat into the CreateOS Project**.
2. The moved chat **retains the GitHub source**.  
   This chat now becomes the persistent:

> **Architect + Repo Access session (V0)**

All Architect work for C01 should occur in this chat (until V1’s Session Manager exists).

---

### 4.3 Step 3 — Human issues the canonical boot message

In the Architect + Repo Access chat (now inside the Project):

1. The human runs (locally or via GitHub UI/CI) `git rev-parse HEAD` on `main` to obtain the **latest commit SHA**.
2. The human posts the canonical boot message:

```text
Latest SHA: <paste HEAD SHA>
Load the repo.
