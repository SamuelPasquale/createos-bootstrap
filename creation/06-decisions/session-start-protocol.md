# Session Start Protocol – C01: CreateOS Bootstrap (v0.2)

This protocol defines the authoritative, deterministic workflow for starting a new work session with **CreateOS Bootstrap (C01)** using ChatGPT + GitHub.

It ensures that every session reconstructs project state from the same sources of truth, with no reliance on memory, guesswork, or manual navigation of the repository.

---

## 0. Repository Attachment (Required)

Before any session can begin, the assistant must be attached to the correct GitHub repository:

> **Active repo:** `SamuelPasquale/createos-bootstrap`

If the repository is not attached, the assistant must not attempt state reconstruction and must instead instruct the user to connect the repo through the GitHub integration.

This step is mandatory because ChatGPT sessions do not persist repository attachments across chats.

---

## 1. Preconditions

- Repository: `SamuelPasquale/createos-bootstrap`
- Branch: `main` (unless otherwise specified)
- The index file `.createos/index.json` is generated and maintained by CI.
- All Creation state lives under the `creation/` directory.
- All progress logs live under: `creation/08-progress/`.

---

## 2. Human Steps at the Start of Each Session

These steps are minimal and must be performed for every new session.

### **Step 1 — Get the latest commit SHA**

From GitHub or local git:

- Navigate to the `main` branch  
- Copy the HEAD SHA (full is preferred; short SHA acceptable)

### **Step 2 — Open a new ChatGPT session in the CreateOS project**

Ensure you are inside the same ChatGPT “CreateOS Project” environment so memory + repo tooling behaves consistently.

### **Step 3 — Provide the minimal boot message**

Paste:

> Latest SHA: `<paste here>`  
> Load the repo.

This is the canonical invocation.

Nothing more is required.

---

## 3. Expected Assistant Behavior

Once the assistant receives the repo identifier and the SHA, it must perform the following steps:

### **Step 3.1 — Validate repository attachment**

Assistant confirms:

- The GitHub integration is active  
- Repo access is available  
- `repo_full_name = SamuelPasquale/createos-bootstrap`  

If not attached, the assistant must immediately halt and instruct the user to connect the repo.

### **Step 3.2 — Load the commit**

Using GitHub’s `fetch_commit` capability:

- Retrieve commit metadata  
- Confirm SHA validity  
- Confirm which files were modified (diff)

### **Step 3.3 — Load `.createos/index.json`**

Using `fetch_file` (if supported by the GitHub connector) or failing that, request the user to paste the index.

The index provides:

- The canonical file list  
- Repository structure  
- Deterministic path resolution for all Creation artifacts  

If live retrieval fails due to connector limitations, the assistant must:

- Ask the user for a pasted copy of the index  
- Treat the pasted index as authoritative for the session

### **Step 3.4 — Enumerate and load key project artifacts**

Using the index, the assistant identifies and reconstructs state from:

- `creation.yaml`  
- V0 specs:
  - `creation/03-v0/v0-functional-spec.md`
  - `creation/03-v0/v0-demo-criteria.md`
- Memory:
  - `creation/05-memory/memory.md`
- Decisions:
  - `creation/06-decisions/*.md`
- Tasks:
  - `creation/07-tasks/tasks.json`
- Progress logs:
  - `creation/08-progress/*.md`  
  - Select the most recent by filename date ordering

### **Step 3.5 — Restore cognitive state**

The assistant reconstructs:

- Current goals and intent  
- Progress-to-date  
- Outstanding tasks and bottlenecks  
- Last session’s decisions  
- Expected next steps  

### **Step 3.6 — Declare readiness**

Assistant responds with:

1. Confirmation of the SHA being used  
2. Summary of last progress log  
3. List of open tasks  
4. Proposed next actions  

Once this message is delivered, the session is “online.”

---

## 4. Error Handling Rules

### **4.1 Missing repository attachment**

Assistant must refuse to proceed and respond:

> No active GitHub repository attached.  
> Please attach `SamuelPasquale/createos-bootstrap` via the GitHub integration.

### **4.2 Invalid or unreachable SHA**

Assistant must ask the user to:

> Reconfirm the SHA via `git rev-parse HEAD` or GitHub UI.

### **4.3 Failure to load `.createos/index.json`**

If direct GitHub file load fails:

- Assistant requests:  
  > “Please paste `.createos/index.json` into the chat.”

- User paste becomes the canonical index for the session.

### **4.4 Missing required files**

Assistant states explicitly which files are absent and continues in degraded mode (or halts if the missing file is critical for reconstruction).

---

## 5. Notes and Future Automation

- This protocol is designed for **V0**, recognizing current GitHub tool constraints.
- Future versions of CreateOS may:
  - Fetch `.createos/index.json` directly without fallback  
  - Auto-detect the active repo  
  - Attach the repo automatically on session open  
  - Eliminate the SHA step via automatic HEAD tracking  

At present, this document represents the only **deterministic**, **auditable**, and **repeatable** boot sequence for working on CreateOS Bootstrap (C01).

---

## 6. Summary

To start any session:

1. Attach repo → `SamuelPasquale/createos-bootstrap`  
2. Get latest SHA  
3. Paste:  
   > Latest SHA: `<sha>`  
   > Load the repo.  
4. Assistant reconstructs full state  
5. Assistant proposes next steps  

This is the canonical Session Start Protocol for C01.
