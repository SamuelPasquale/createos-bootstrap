# Decision: File Placement Conventions

**Status**: Accepted  
**Date**: 2025-12-12  
**Context**: Establish canonical rules for what belongs in each directory under `creation/` to maintain consistency and clarity as the repository evolves.

---

## Problem

As the CreateOS Bootstrap repository grows, we need explicit conventions for where to place different types of artifacts, documentation, and state. Without clear rules, contributors may be uncertain about file placement, leading to inconsistency and harder navigation.

---

## Decision

We adopt the following canonical file placement conventions for all directories under `creation/`:

### 1. `creation/01-goals/`

**Purpose**: High-level strategic goals, constraints, and intent for the Creation.

**What belongs here**:
- Vision statements and mission
- Success criteria and non-goals
- Principles and philosophical foundations
- Long-term objectives (e.g., "What does CreateOS aim to achieve?")

**What does NOT belong here**:
- Tactical roadmaps (use `02-roadmap/`)
- Implementation details (use `04-artifacts/`)
- Decisions (use `06-decisions/`)

---

### 2. `creation/02-roadmap/`

**Purpose**: Versioned progression plans (V0 → V1 → Platform).

**What belongs here**:
- Milestone definitions (e.g., V0 scope, V1 scope)
- Sequencing and phasing plans
- Dependency graphs between major features
- Timeline estimates (if applicable)

**What does NOT belong here**:
- Individual task details (use `07-tasks/`)
- Session logs (use `08-progress/`)
- Design specifications (use `04-artifacts/`)

---

### 3. `creation/03-v0/`

**Purpose**: V0 functional specifications, demo scripts, and acceptance criteria.

**What belongs here**:
- V0 functional spec document
- V0 demo script and acceptance tests
- V0 troubleshooting and fallback runbooks
- V0-specific design notes

**What does NOT belong here**:
- V0.5 or V1 specifications (use `04-artifacts/` for versioned designs)
- General architecture (use `04-artifacts/createos-architecture.md`)

**Note**: As of 2025-12-12, V0 is in **maintenance mode**. This directory is retained for fallback documentation only.

---

### 4. `creation/04-artifacts/`

**Purpose**: Generated or versioned artifacts, specifications, schemas, and agent prompts.

**What belongs here**:
- Architecture documents (e.g., `createos-architecture.md`)
- Service blueprints (e.g., `session-manager-mvp.md`)
- Agent prompts (subdirectory: `agent-prompts/`)
- Boot reports (subdirectory: `boot/`)
- Runtime scope documents (e.g., `v0.5-runtime-scope.md`)
- Schemas and API contracts
- Generated reports or analysis outputs

**What does NOT belong here**:
- Decisions (use `06-decisions/`)
- Session logs (use `08-progress/`)
- Task tracking (use `07-tasks/`)

**Subdirectories**:
- `agent-prompts/` — Architect and Developer prompts for different runtimes
- `boot/` — Session bootstrap JSON reports (e.g., `LATEST.json`)
- `archive/` — Deprecated or superseded artifacts

---

### 5. `creation/05-memory/`

**Purpose**: Append-only, structured memory log (`memory.md`).

**What belongs here**:
- Timestamped memory entries (events, decisions, commits, sessions)
- References to external resources (with context)
- Cognitive state checkpoints

**What does NOT belong here**:
- Session logs (use `08-progress/`)
- Tasks (use `07-tasks/`)
- Decisions (use `06-decisions/` for formal decisions; memory is for raw events)

**Format**: See `memory.md` for schema (YAML frontmatter + markdown body).

---

### 6. `creation/06-decisions/`

**Purpose**: Architectural decision records (ADRs) and protocol definitions.

**What belongs here**:
- Formal decision documents (e.g., "Why did we choose X over Y?")
- Protocol specifications (e.g., `session-start-protocol.md`)
- Policy documents (e.g., `github-write-policy.md`)
- File placement conventions (this document)

**What does NOT belong here**:
- Implementation artifacts (use `04-artifacts/`)
- Task tracking (use `07-tasks/`)
- Session logs (use `08-progress/`)

**Format**: Each decision should include:
- **Status**: Proposed / Accepted / Deprecated / Superseded
- **Date**: When the decision was made
- **Context**: Why was this decision needed?
- **Decision**: What was decided?
- **Consequences**: What are the implications?

---

### 7. `creation/07-tasks/`

**Purpose**: Task graph (`tasks.json`) tracking all work items.

**What belongs here**:
- `tasks.json` — Canonical list of tasks with IDs, descriptions, statuses, dependencies, and notes
- Task-related metadata (e.g., future enhancements might include task templates or workflow definitions)

**What does NOT belong here**:
- Session logs (use `08-progress/`)
- Roadmaps (use `02-roadmap/`)
- Individual task work artifacts (use `04-artifacts/` or `08-progress/`)

**Task schema** (JSON):
```json
{
  "id": "T001",
  "description": "Short task description",
  "status": "pending | in-progress | complete | superseded",
  "dependencies": ["T000"],
  "mode": "optional; e.g., 'maintenance'",
  "notes": "Optional context, references, or constraints"
}
```

---

### 8. `creation/08-progress/`

**Purpose**: Dated session logs and progress reports.

**What belongs here**:
- `YYYY-MM-DD.md` — Dated session logs (one per day, or one per session)
- `LATEST.json` — Pointer to most recent progress log (future warm-start feature)
- Summary of completed work, next steps, and session metadata

**What does NOT belong here**:
- Tasks (use `07-tasks/`)
- Memory entries (use `05-memory/`)
- Architectural decisions (use `06-decisions/`)

**Format**: Each progress log should include:
- **Summary**: What was the focus of this session?
- **Completed Tasks**: List of tasks completed (reference task IDs from `tasks.json`)
- **Next Steps**: What should happen next?
- **Session Metadata**: Date, branch, commit SHA, session type

---

## Additional Conventions

### Top-level files

- `creation.yaml` — Creation descriptor (metadata, owners, status)
- `.createos/index.json` — Canonical file index (CI-generated)
- `.createos/manifest.json` — Lightweight manifest describing repo metadata (future)

### Tools directory (`tools/`)

**Purpose**: Operational scripts and utilities.

**What belongs here**:
- `refresh_index.py` — Regenerate `.createos/index.json`
- `close_session.py` — Close session and update progress logs
- `add_memory_entry.py` — Append memory entries
- `start_session.py` — Generate session bootstrap JSON

**What does NOT belong here**:
- Documentation (use `creation/04-artifacts/` or `README.md`)
- Agent prompts (use `creation/04-artifacts/agent-prompts/`)

---

## Cross-References

- **README.md**: Repository structure overview
- **creation/04-artifacts/v0.5-runtime-scope.md**: V0.5 runtime details
- **creation/06-decisions/session-start-protocol.md**: Session bootstrap protocol
- **creation/07-tasks/tasks.json**: Task T008 (this decision)

---

## Consequences

1. **Consistency**: All contributors follow the same placement rules, reducing confusion.
2. **Discoverability**: Files are easier to find and navigate.
3. **Tooling simplicity**: Scripts like `refresh_index.py` can make assumptions about file locations.
4. **Scalability**: As the repository grows, clear conventions prevent sprawl.

---

## Changelog

- **2025-12-12**: Initial file placement conventions established (T008).
