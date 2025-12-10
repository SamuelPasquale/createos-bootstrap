# Session Start Protocol – C01: CreateOS Bootstrap

## Purpose

This document defines the standard procedure for starting a new work session
with CreateOS Bootstrap (C01) using ChatGPT + GitHub as the primary interface.

The goal is to ensure that every session:

- Resumes from an authoritative project state,
- Uses the same workflow consistently,
- Does not rely on the human remembering file paths or structure.

---

## Preconditions

- Repository: `SamuelPasquale/createos-bootstrap`
- Branch: `main`
- `.createos/index.json` is maintained automatically by GitHub Actions.
- Daily progress logs are stored under: `creation/08-progress/`.

---

## Human Steps at the Start of Each Session

1. **Get the latest commit SHA**
   - Open the `createos-bootstrap` repo on GitHub.
   - Ensure you are on the `main` branch.
   - Copy the latest commit SHA (short or full is fine).

2. **Open a new ChatGPT session in the CreateOS project**
   - Start a new chat inside the same ChatGPT Project used for CreateOS.

3. **Provide the minimal boot context**
   - Paste the latest SHA and issue a simple instruction, for example:

     > Latest SHA: `<paste here>`  
     > Load the latest progress log and current project state.

That is the entire human-side startup procedure.

---

## Expected ChatGPT / Agent Behavior

When given the latest SHA, the assistant should:

1. **Load the repo index**
   - Fetch `.createos/index.json` at the provided SHA.
   - Use it as the canonical list of files and directory structure.

2. **Locate the latest progress log**
   - Find all files under `creation/08-progress/`.
   - Select the most recent log file (by date in filename or by index ordering).
   - Load and summarize the log.

3. **Reconstruct current project state**
   - Use the progress log + index to re-establish context:
     - Overall goals,
     - Current V0 status,
     - Open tasks,
     - Agreed next steps.

4. **Confirm starting point**
   - Reply with a brief summary of:
     - What was last accomplished,
     - What remains open,
     - A proposed next action for this session.

---

## Notes and Future Automation

- This protocol is intentionally minimal: it requires only a SHA paste and one
  instruction from the human.
- In future versions of CreateOS, a CLI or service may:
  - Provide the latest SHA automatically,
  - Or even call the assistant with the SHA as part of a higher-level workflow.
- Until then, this protocol is the canonical, deterministic way to resume work
  on C01 across multiple sessions and devices.
