# CreateOS Bootstrap (C01)

This repository hosts the first working Creation for CreateOS: **C01 – CreateOS Bootstrap**.

The purpose of this Creation is to:

- Establish a minimal Git-backed filesystem for CreateOS.
- Implement deterministic tools for memory and task management.
- Demonstrate a V0 demo where CreateOS modifies its own artifacts and specifications.

## Structure

- `creation.yaml` – Top-level descriptor for the Creation.
- `creation/` – All state for this Creation.
  - `01-goals/` – High-level goals and intent.
  - `02-roadmap/` – Roadmap documents (V0 → V1 → Platform → Enterprise).
  - `03-v0/` – V0 functional spec, demo script, acceptance criteria.
  - `04-artifacts/` – Generated artifacts (design docs, schemas, etc.).
  - `05-memory/` – Structured memory log (`memory.md`).
  - `06-decisions/` – Architectural decisions and rationale.
  - `07-tasks/` – Task graph (`tasks.json`).
- `tools/` – Scripts and utilities for operating on the Creation.
- `references/` – Strategic and thesis documents used for context.

This repo is intentionally narrow in scope. It exists to **bootstrap** CreateOS itself.
