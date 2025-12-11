# CreateOS Architecture Manual  
## Unified Architecture for V0 (Implemented) and V1 (Design Roadmap)

---

# 1. Introduction

CreateOS is a **Cognitive Creation Environment (CCE)**: a system where a human and multiple AI agents collaborate to build software, systems, content, or other structured Creations through a deterministic, auditable workflow.

This architecture describes:

1. **V0** — the current, implemented CreateOS environment  
2. **V1** — the designed but not-yet-implemented CreateOS-native runtime with Session Manager, persistent memory, and automated lifecycle controls  
3. **The foundational philosophy** that ties both versions together  
4. **How users and AI agents interact with the system**  
5. **How CreateOS persists, reconstructs, and evolves Creations over time**

This manual serves as the authoritative reference for all stakeholders, including architects, developers, maintainers, and operators.

---

# 2. Architectural Philosophy

CreateOS is built around several core principles:

## 2.1. The Creation is the primary unit of work
Instead of thinking in terms of files or chats, CreateOS defines a **Creation** as a durable, evolving object with:

- Intent  
- State  
- Memory  
- Change history  
- Associated tasks  
- Artifacts  
- Agents operating upon it  

A Creation persists independently of any particular ChatGPT session.

## 2.2. The backend is the source of truth
For V0, the backend is GitHub; for V1+, it will expand to include a memory service and session manager.

The core rule:

> **No Creation state lives solely inside ChatGPT.**

Every meaningful project update is written back to the backend.

## 2.3. Stateless AI, stateful Creation
ChatGPT agents (Architect, Developer) are intentionally ephemeral.

The Creation itself is stateful.

This means:

- Chats can be created and deleted freely.  
- System state reconstructions must be reproducible at any time.  
- Memory is append-only and versioned.  

## 2.4. Deterministic workflows
The system must produce the same result given the same inputs. This is enforced through:

- A deterministic boot sequence  
- A deterministic filesystem structure  
- Auditable logs  
- Automation tools (`close_session.py`, `add_memory_entry.py`, etc.)

## 2.5. Human agency and consent
The human:

- Owns all Creations  
- Approves all connector usage (in V0: GitHub attachment; in V1: fully scoped consent UI)  
- Controls when sessions start and end  
- Controls merging PRs  

CreateOS does not autonomously modify the backend without explicit user involvement.

---

# 3. High-Level System Overview

CreateOS is composed of:

- **A backend** (V0 = GitHub; V1 = GitHub + Memory Service + Session Manager)  
- **An Architect agent** (ChatGPT Project)  
- **A Developer agent** (Codex chat with GitHub connector)  
- **Deterministic tools** to manage memory, tasks, indexing, and session closure  
- **A formal boot protocol** to rehydrate Creation state in any new chat  
- **A directory structure** that encodes the Creation’s entire ontology

Below is the conceptual flow:

```
      Human User
          |
          v
+--------------------+
|   Architect Agent  |
| (ChatGPT Project)  |
+--------------------+
          |
  Instruction Packages
          v
+--------------------+
|  Developer Agent   |
|    (Codex)         |
+--------------------+
          |
       GitHub PRs
          v
+--------------------+
|      Backend       |
| GitHub Repository  |
+--------------------+
```

For V1, this expands:

```
      Human User
          |
     Consent UI
          |
          v
+------------------+        +---------------------+
| Session Manager  |------->|  Memory Service     |
+------------------+        +---------------------+
          |                         ^
   Session Tokens                   |
          v                         |
+------------------+         Memory Reads/Writes
| Architect Agent  |----------------------------+
+------------------+                            |
          |                                      |
Instruction Packages                             |
          v                                      |
+------------------+                             |
| Developer Agent  |------------------------------+
+------------------+
          |
       GitHub PRs
```

---

# 4. Core Concepts

## 4.1. Creation
A Creation is the root object of the system. It contains:

- Metadata (`creation.yaml`)
- Tasks (`07-tasks/`)
- Memory (`05-memory/`)
- Artifacts (`04-artifacts/`)
- Decisions (`06-decisions/`)
- Progress logs (`08-progress/`)
- File index (`.createos/index.json`)
- Manifest (`.createos/manifest.json`)

## 4.2. Memory (append-only)
Memory is:

- Versioned  
- Immutable  
- Human-readable  
- Chronologically ordered  
- Written to `creation/05-memory/memory.md`  

## 4.3. Progress Logs & LATEST.json
Progress logs track:

- What happened  
- What tasks moved  
- What comes next  

`LATEST.json` provides a fast path for rehydration.

## 4.4. AI Roles
### Architect (ChatGPT Project)
- Performs reasoning  
- Designs changes  
- Writes architectural notes  
- Issues instructions to Developer  

### Developer (Codex)
- Reads the repo  
- Writes diffs  
- Opens PRs  
- Performs filesystem operations  

### Human
- Approves connector usage  
- Approves merges  
- Provides intent  
- Closes sessions  

---

# 5. V0 Architecture (Implemented Today)

## 5.1. Overview
V0 is the minimal functional implementation of CreateOS, built entirely on top of ChatGPT + GitHub.

It accomplishes:

- Fully deterministic state reconstruction  
- Task graph management  
- Memory updates  
- Progress logs  
- A save/close session lifecycle  
- A dual-chat boot method to work around ChatGPT limitations  
- A simulated runtime via separation of Architect and Developer agents  

## 5.2. The V0 Directory Structure
Authoritative and enforced by `.createos/index.json`.

```
creation/
   01-goals/
   02-roadmap/
   03-v0/
   04-artifacts/
   05-memory/
   06-decisions/
   07-tasks/
   08-progress/
.createos/
   index.json
   manifest.json
tools/
   close_session.py
   add_memory_entry.py
   refresh_index.py
README.md
```

## 5.3. V0 Boot Sequence (Authoritative)
This is the **actual** working boot pattern.

### Step 1 — Human creates a new ChatGPT chat **outside** the Project
Inside the ChatGPT main interface, not the Project interface.

### Step 2 — Human attaches the GitHub repository
Using **Company Knowledge → GitHub → Add Repository**, selecting:

```
SamuelPasquale/createos-bootstrap
```

### Step 3 — Human verifies GitHub attachment
By fetching e.g.:

```
README.md
creation/06-decisions/session-start-protocol.md
```

### Step 4 — Human moves the chat into the CreateOS Project
This preserves connector context.

### Step 5 — Human provides the canonical boot message
```
Latest SHA: <paste main HEAD SHA>
Load the repo.
```

### Step 6 — Architect reconstructs state
- Loads `.createos/index.json`  
- Reads `LATEST.json` fast-path summary  
- Loads memory log  
- Loads tasks  
- Loads last progress log  
- Summarizes status  
- Presents next actions  

### Step 7 — Human begins working
All subsequent reasoning is done in this Architect chat.

### Step 8 — Developer involvement
When modifications are needed:

- Architect produces instruction package  
- Human pastes it into Developer (Codex) chat  
- Codex executes + opens PR  
- Human merges PR  

---

# 5.4. V0 Save / Close Session Lifecycle

V0 uses the script:

```
python tools/close_session.py
```

This script:

- Writes a new `creation/08-progress/YYYY-MM-DD.md` file  
- Updates `creation/08-progress/LATEST.json`  
- Updates tasks  
- Appends memory entry  
- Reports completion  

This is the **V0 "save button"**.

A normal V0 workflow is:

```
Work → Close Session → Delete Architect Chat
```

Then tomorrow:

```
Fresh Chat → GitHub Attach → Move Into Project → Boot
```

This simulates "turning the computer off and on again."

---

# 6. Limitations of V0

- No persistent memory service  
- No session tokens  
- No automated diff execution  
- Requires manual chat handoff  
- No built-in consent UI  
- No automated reconstruction triggers  
- Heavy reliance on human discipline  

These limitations are the motivation for V1.

---

# 7. V1 Architecture (Design Only)

## 7.1. Goals

V1 is the first "real" CreateOS runtime.

It provides:

- Native startup flow  
- Persistent memory service  
- Session Manager issuing signed session tokens  
- Consent UI  
- Automated Developer execution (no copy/paste)  
- Unified multi-agent runtime  
- Single-click “Resume Creation”  
- Real backend independence from ChatGPT ephemeral sessions  

## 7.2. V1 Core Components

### 7.2.1. Session Manager
Responsible for:

- Token issuance  
- Scopes  
- Expiry  
- Repo metadata  
- Audit logs  
- Bootstrap trace ingestion  

### 7.2.2. Persistent Memory Service
A real backend distinct from Git.

Stores:

- Memory entries  
- Compaction entries  
- Session traces  

### 7.2.3. Developer Runtime (Automated)
CreateOS-native Codex-like environment:

- Executes file operations  
- Applies patches  
- Runs migrations  
- Does not require human copy/paste  

### 7.2.4. Consent UI
Human-facing permission surface:

- Shows requested scopes  
- Shows expiry  
- Allows revocation  
- Logs consent  

---

# 8. V1 Save vs. Close Semantics

## 8.1. Save Session
Non-final:

- Persist memory delta  
- Persist progress marker  
- Persist reconstruction snapshot  

Does not terminate the session.

## 8.2. Close Session
Final:

- Writes formal progress log  
- Completes tasks  
- Ends session token validity  
- System becomes read-only until a new session is issued  

---

# 9. Roadmap (V0 → V1 → Beyond)

### V0
- Fully deterministic filesystem  
- Dual-chat boot  
- Script-based save/close  
- Manual developer execution  

### V1
- Session Manager  
- Memory Service  
- Automated Developer  
- Consent UI  

### V2+
- Multi-agent parallelism  
- Distributed Creations  
- Autonomous validation and test harnesses  
- Visual Creation Explorer  

---

# 10. Glossary

- **Creation** — the durable project object  
- **Architect** — reasoning agent  
- **Developer** — code execution agent  
- **Session** — bounded window of work  
- **Memory** — append-only log of durable state changes  
- **Boot** — loading a Creation into a new chat  
- **Close Session** — formal end-of-session record  
- **Save Session** — interim persistence checkpoint  
- **Session Manager** — V1 component issuing tokens and managing scopes  

---

# END OF DOCUMENT
