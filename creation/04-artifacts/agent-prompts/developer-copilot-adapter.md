---
name: CreateOS Developer — Copilot Adapter (v0.1)
description: "Adapter for Developer instructions when run inside Copilot Spaces or Codex-like agents."
---

# Developer — Copilot adapter

**Purpose:** Minimal Copilot-specific runtime guidance for the CreateOS Developer persona.

## Adapter rules
- **Auth & commit context.** When applying changes, the Developer must include `session_id` and `architect_summary` in the PR body.
- **PR metadata required:** PR title (imperative), commit message, PR body with rationale and test steps.
- **Index updates:** If files affecting `.createos/index.json` were changed, include `tools/refresh_index.py` instructions in the PR and a note of expected `index.json` change.

## Tests
- A developer PR that updates documentation must include `tools/refresh_index.py` instructions if file additions occur.
