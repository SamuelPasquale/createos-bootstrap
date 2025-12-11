# Agent Prompts — Governance & Versioning

This directory holds canonical runtime prompts and small adapters for CreateOS agents.

## Files
- `architect-prompt.md` — Canonical CreateOS Architect prompt (Project). **Source of truth for chat-based Architect.**
- `architect-copilot-adapter.md` — Minimal Copilot adapter for Architect usage inside Copilot Spaces.
- `developer-prompt.md` — Canonical CreateOS Developer prompt (Codex / Developer).
- `developer-copilot-adapter.md` — Minimal Copilot adapter for Developer (optional).
- `README.md` — this file.

## Versioning policy
- Prompts must include a top-line version number: `vX.Y` in their header.
- All prompt changes MUST be made via PR to `main` and reference one acceptance test run.

## Update process
1. Create a branch: `prompts/canonicalize-v1` or `prompts/<issue>-v1`.
2. Update the prompt file(s).
3. Add a short `creation/04-artifacts/agent-prompts/CHANGELOG.md` entry describing changes.
4. Open a PR with a description and acceptance test plan.
5. Run the acceptance tests (see below) and report results in PR.

## Acceptance tests (minimum)
- Parity: Project Architect prompt and `architect-prompt.md` are identical in substance (adapter files allowed).
- Copilot boot test: Architect in Copilot must produce the canonical readiness summary on boot.
- Developer smoke PR: Developer agent creates a small doc-fix PR; PR metadata includes `session_id` and `architect_summary`.

