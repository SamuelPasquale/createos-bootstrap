# Session Start Protocol — C01: CreateOS Bootstrap (V0)

**Status:** V0 (temporary). This protocol documents the deterministic, auditable boot sequence required for CreateOS Bootstrap given current platform constraints. It will be replaced by a CreateOS-native startup sequence in v1.

## Purpose

Provide a single, deterministic way to start a CreateOS Architect session that has read access to the repository and can reconstruct Creation state.

## Roles

- **Architect** — ChatGPT Project (cognitive layer).  
- **Developer** — Codex (developer layer, repo write/PR executor).

## Preconditions

- Repository: `SamuelPasquale/createos-bootstrap` (branch: `main`).  
- `.createos/index.json` is maintained by CI and available in the repo.  
- The repository is reachable via the GitHub connector.

## Canonical V0 Steps

1. **Create a repo-enabled chat outside the CreateOS Project**  
   - Attach GitHub via Company knowledge and confirm `SamuelPasquale/createos-bootstrap`.  
   - Verify: fetch `README.md` and `.createos/index.json`.

2. **Move the repo-enabled chat into the CreateOS Project**  
   - After moving, this chat serves as the persistent **Architect + Repo Access** session. It must validate repository access before proceeding.

3. **Human: Provide the minimal bootstrap**  
   - Provide the latest commit SHA from `main` and paste the canonical boot message:
     ```
     Latest SHA: <paste HEAD SHA>
     Load the repo.
     ```

4. **Assistant: Deterministic reconstruction**  
   Once the boot message is received, the Architect assistant must:
   - Validate repository attachment and confirm `repo_full_name = SamuelPasquale/createos-bootstrap`.
   - Fetch commit metadata for the provided SHA and confirm SHA validity.
   - Load `.createos/index.json` (via fetch_file) or request a pasted index if fetch fails.
   - Using the index, enumerate and load:
     - `creation.yaml`
     - V0 specs (`creation/03-v0/*`)
     - Memory (`creation/05-memory/memory.md`)
     - Decisions (`creation/06-decisions/*`)
     - Tasks (`creation/07-tasks/tasks.json`)
     - Progress logs (`creation/08-progress/*.md`) — choose most recent
   - Reconstruct cognitive state (goals, progress, open tasks, decisions).
   - Declare readiness with:
     1. Confirmation of SHA
     2. Summary of last progress log
     3. List of open tasks
     4. Proposed next actions

5. **Developer flow (Codex)**  
   - For file changes, the Architect produces a self-contained instruction package.  
   - The Developer (Codex) reads the live repo, shows diffs, opens a branch and PR for review.

## Error handling

- **No active GitHub attachment**: refuse and respond:
  > No active GitHub repository attached. Please attach `SamuelPasquale/createos-bootstrap` via the GitHub integration.

- **Invalid or unreachable SHA**: ask human to reconfirm via `git rev-parse HEAD`.

- **Failure to fetch `.createos/index.json`**: ask the human to paste the index and treat the pasted copy as authoritative.

- **Missing required files**: list missing files and either continue in degraded mode or halt if critical.

## V0 → Future

This protocol is intentionally conservative; it prioritizes determinism and auditability. It is a temporary bootstrapping pattern that must be replaced in v1 by an integrated CreateOS startup sequence with persistent, first-class memory and direct backend mounting.

(End of protocol)
