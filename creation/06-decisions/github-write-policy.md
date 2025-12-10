# GitHub Write Policy – C01: CreateOS Bootstrap

## Purpose
This document defines how any automated or AI-driven system is allowed to write to
the `createos-bootstrap` repository. It is designed to prevent accidental overwrites
of newer commits and to keep all changes explicit, auditable, and deterministic.

This policy applies to any future CreateOS agent or integration with write access.

---

## Core Invariant

**No commit may be created or pushed without using a verified parent commit SHA
for the target branch (e.g., `main`).**

The system must never assume HEAD. It must always operate on an explicitly
confirmed parent SHA.

---

## Required Workflow for Automated Writes

1. **Read phase (agent):**
   - Agent reads the repository state and determines which files it intends to modify.
   - Agent constructs a proposed set of changes (diff) and a candidate commit message.

2. **Parent SHA confirmation (human or higher-privilege process):**
   - A human or privileged process obtains the latest commit SHA for the target branch
     from GitHub’s UI or a trusted API.
   - That SHA is explicitly supplied to the agent as the `parent_sha` to use.
   - No commit is created without this explicit SHA.

3. **Commit construction (agent):**
   - Agent applies the proposed changes to the tree based on the confirmed `parent_sha`.
   - Agent creates a new commit object with:
     - `parent_sha` = confirmed SHA
     - `tree_sha` = tree including the changes
     - `message` = structured, descriptive commit message

4. **Ref update (agent or privileged process):**
   - Branch ref (e.g., `refs/heads/main`) is updated to point to the new commit.
   - If the update fails due to a non-fast-forward condition, the operation aborts
     and must be retried with a new `parent_sha`.

5. **Post-commit verification:**
   - Agent reads the new HEAD commit and verifies that:
     - The intended changes are present.
     - No unintended files were modified or removed.

---

## Human-in-the-Loop Guarantee (V0–V1)

For the V0 and early V1 phases:

- A human (the creator/owner) **must**:
  - Confirm the latest SHA before each automated commit.
  - Approve the diff proposed by the agent.

The agent is not allowed to silently push changes.

---

## Future Automation (Beyond V1)

Once CreateOS has its own orchestrator and higher-level safety mechanisms:

- A dedicated, privileged service (not the LLM directly) may:
  - Handle parent SHA retrieval
  - Perform git operations using the official GitHub API
  - Enforce this policy as code

Even then, this document remains the canonical specification of allowed behavior.

---

## Current Environment Note (ChatGPT Project)

In the current ChatGPT environment:

- The GitHub integration is effectively **read-only** for the LLM.
- The LLM cannot directly:
  - create or delete files,
  - modify existing files,
  - or push commits.

Therefore, this policy is **forward-looking** and describes how future
CreateOS agents or services with write access must behave.

All write operations at this stage are performed manually by the human,
following LLM-generated instructions or diffs.
