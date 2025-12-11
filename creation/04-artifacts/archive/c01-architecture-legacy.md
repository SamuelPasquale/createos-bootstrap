---

Final V0 → V1 Architecture Document (Draft for Repo Commit)

Below is the complete, polished document.
After review, tomorrow we’ll package this into a Codex PR instruction.


---

C01 Architecture Overview — V0 System (Implemented) and V1 Design (Planned)

CreateOS — Cognitive Creation Environment (CCE)
File: creation/04-artifacts/c01-architecture.md
Status: Authoritative V0 documentation, plus V1 design plan


---

1. Introduction

CreateOS (C01) is a minimal, bootstrapped prototype of a Cognitive Creation Environment. It exists to demonstrate how a human, a cognitive AI (Architect), and a developer AI (Codex) can collaboratively build and maintain a Creation using deterministic, Git-backed state.

C01 is intentionally small: it focuses on one workflow only — building itself — to validate the core abstractions:

Git-backed artifact graph

Deterministic session boot

Append-only memory

Task graph

Human + AI collaboration patterns


C01 is the scaffolding for the full CreateOS runtime that will arrive in V1.


---

2. System Overview

CreateOS is architected around three conceptual layers:

2.1 Human

Provides intent, review, governance, approval, and long-horizon direction.

2.2 Architect (ChatGPT within a Project)

A cognitive agent that reads the repo, reconstructs Creation state, and plans work.
In V0, the Architect must be manually bootstrapped by the human.

2.3 Developer (Codex-enabled GitHub chat)

A deterministic agent that executes file modifications and PR creation.
All repo writes occur through Codex.


---

3. V0 Architecture — The System That Exists Today

V0 is the minimal working system where:

ChatGPT Project = Architect

Codex Repo-enabled Chat = Developer

GitHub Repository = Backend / Persistence Layer

Manual Chat Workflow = Session Manager substitute


V0’s purpose is not elegance — it is functional validation of the CreateOS model.


---

3.1 V0 Components

3.1.1 GitHub Repository (Backend)

Stores:

Creation descriptor (creation.yaml)

Artifacts

Decisions

Task graph (tasks.json)

Memory log (append-only markdown)

Progress logs

CI-generated file index (.createos/index.json)

Session-close logic (tools/close_session.py)


The repo is the single source of truth.


---

3.1.2 ChatGPT Architect (Cognitive Layer)

The Architect:

Reads the repo via GitHub connector

Loads .createos/index.json

Reconstructs memory, tasks, decisions, and progress

Provides project continuity

Creates precise developer instructions


It is stateful only within the limits of the chat window.
All true state lives in GitHub.


---

3.1.3 Codex Developer (Execution Layer)

Codex:

Reads files

Computes diffs

Commits changes

Creates pull requests


It executes all mutations to the system.


---

3.2 V0 Session Workflow (Implemented Today)

The V0 system depends on a dual-chat workflow to simulate login, boot, and runtime:

Step 1 — Human creates a repo-enabled chat outside the Project

This chat becomes the Developer session.

Step 2 — Human moves the chat into the Project

It becomes the Architect session.

Step 3 — Human provides bootstrap information

The Architect requires:

Latest SHA: <HEAD SHA>
Load the repo.

Step 4 — Architect reconstructs state

Steps:

Confirm GitHub connector

Load .createos/index.json

Read all directories per index

Load memory and progress logs (preferring LATEST.json)

Build cognitive state

Report next actions


Step 5 — Architect → Developer workflow

Architect produces deterministic instructions

Human copies these into Codex

Codex produces PRs

Architect reviews



---

3.3 V0 State Persistence

V0 provides three persistence primitives:

1. Progress logs

creation/08-progress/YYYY-MM-DD.md
Every working block generates a log.

2. LATEST.json

A snapshot of:

Date

Summary

Next steps

SHA
Used during boot for fast session restoration.


3. Memory log

An append-only ledger of system events.

Tools

tools/close_session.py writes:

Progress log

LATEST.json

Memory entry

Task updates


This is V0’s manual Save button.


---

3.4 V0 Limitations

V0 works, but with constraints:

Requires manual dual-chat boot

Requires manually copying instructions into Codex

Requires manual close_session execution

No automatic autosave

No concept of revocation or scoped consent

Chat context is fragile and ephemeral


These limitations directly motivate V1.


---

4. V1 Architecture — Planned Native Runtime

V1 replaces all manual scaffolding with a real runtime, consisting of:

Session Manager

Consent UI

Persistent Memory API

Automatic repo + storage mounting

Autosave + close session

Architect & Developer as first-class system agents


V1 is non-functional today; what follows is a design blueprint only.


---

4.1 Session Manager (Core of V1 Runtime)

The Session Manager:

Issues signed session tokens

Provides repo metadata

Manages scoped connector handles

Handles revocation

Stores bootstrap traces

Provides autosave endpoints


It replaces the manual boot procedure entirely.


---

4.2 Consent UI

Human sees a clear consent prompt:

Requested scopes:

repo read/write

memory read/write

artifact storage


Human approves or rejects.

Revocation is immediate.


---

4.3 Autosave Architecture (V1 Feature)

V1 introduces two persistence primitives:

4.3.1 Autosave (lightweight, frequent)

Triggered every N minutes or after major events:

Write memory entry

Update LATEST.json

Update lightweight task deltas


Autosave does not generate a full progress log.

4.3.2 Close session (explicit)

End of a working block:

Generate full progress log

Update memory

Finalize tasks

Refresh index

Close session token


Close session is equivalent to a “safe shutdown.”


---

4.4 Developer Integration (V1)

Architect and Developer become tightly linked:

Architect issues commands

Session Manager routes them to Developer

Developer executes changes deterministically


Manual copy–paste is eliminated.


---

4.5 Boot Flow (V1)

In V1:

1. Human opens CreateOS


2. Presses “Resume Creation”


3. Session Manager provides a token


4. Architect loads repo and memory automatically


5. Human starts working



The system behaves like a real OS session.


---

5. Philosophy

CreateOS is not a tool; it is a metasystem, enabling cognitive work at scale.

V0 proves:

A Creation can live entirely in Git

AI can manage long-term state via deterministic reconstruction

Human supervises while AI executes


V1 generalizes:

Any human can open a Creation

Any Creation can run arbitrary agent workflows

The system becomes a persistent machine for thought



---

6. Roadmap Snapshot

V0 Completion Targets

Accurate session-start protocol for V0

Architecture doc (this file)

README consistency

Consolidate project files into repo

Smooth session save/close workflows

Store system prompts in repo


V1 Targets

Session Manager service

Consent UI

Persistent Memory API

Autosave + Close Session

Integrated Architect ↔ Developer agent pipeline

Resume Creation UX

Formalized system prompts



---

7. Glossary

Creation: The project the system manages
Architect: Cognitive agent providing design and reasoning
Developer: Deterministic agent applying diffs
Session Manager: V1 runtime coordinator
Memory: Append-only system state
Task graph: Directed list of tasks and dependencies
Progress log: Human-readable session summary


---

End of Document


---
