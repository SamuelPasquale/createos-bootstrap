# V0 – Demo Script & Acceptance Criteria  
C01 – CreateOS Bootstrap

## 1. Demo Purpose
Demonstrate that CreateOS V0 implements:

- persistence  
- determinism  
- structured memory  
- artifact creation + evolution  
- task graph maintenance  
- self-modifying (“self-bootstrap”) behavior  

---

## 2. Demo Script

### Step 1 — Retrieve Creation State
**User:** “Show the current state of the Creation.”

**System must:**
- read `creation.yaml`  
- summarize goals, paths, tasks, memory entries  
- write memory entry: “Retrieved Creation state.”  

---

### Step 2 — Create an Artifact
**User:** “Create a new artifact named `system-architecture-v0.md` describing the V0 architecture.”

**System must:**
- create file in `creation/04-artifacts/`  
- populate with architecture content  
- write memory entry  
- add task “Refine system architecture”  

Acceptance: artifact appears in directory and is readable.

---

### Step 3 — Update Artifact
**User:** “Add a section describing the deterministic action pipeline.”

**System must:**
- read the artifact  
- update content without overwriting structure  
- write structured memory entry  
- update related task  

Acceptance: update is coherent and incremental.

---

### Step 4 — Update Task Graph
**User:** “Mark the refinement task complete and add a new task to define the file interface.”

Acceptance: `tasks.json` reflects the update with correct dependency handling.

---

### Step 5 — Demonstrate Self-Modification
**User:** “Improve the V1 Roadmap section based on V0 progress.”

**System must:**
- read roadmap  
- identify missing or weak areas  
- propose improvements  
- apply those improvements  
- write memory entry  

Acceptance: system successfully edits its own spec documents.

---

### Step 6 — End-of-Session Summary
**User:** “Summarize today’s changes.”

**System must:**
- read recent memory entries  
- list artifact changes  
- list task updates  
- provide coherent narrative summary  

Acceptance: summary accurately reflects actions taken.

---

## 3. Acceptance Criteria (Formal)

### A. Persistence
All state (artifacts, tasks, memory, specs) must persist in Git.

### B. Determinism
No changes occur without explicit system reasoning and memory logs.

### C. Artifact Operations
System can:
- create files  
- update files  
- preserve structure  
- record changes  

### D. Memory Behavior
Every meaningful action writes a log entry with:
- event  
- reasoning  
- changes  

### E. Task Graph Integrity
Tasks must be addable, updatable, and preserved in dependency order.

### F. Self-Bootstrapping
System must coherently modify:
- roadmap  
- specs  
- artifacts  

### G. Demo Completeness
All script steps execute coherently and consistently.

---

# End of V0 Demo Script & Acceptance Criteria
