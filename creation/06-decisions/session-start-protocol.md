# Session Start Protocol — C01: CreateOS Bootstrap (CreateOS-Native)

**Status:** Transition to CreateOS-native startup. This protocol replaces the dual-chat V0 workaround with a deterministic, auditable session bootstrap backed by a Session Manager, scoped credentials, and first-class Creation memory.

## Purpose

Provide a one-click, CreateOS-native way to start or resume an Architect session with:

- Persistent project memory across sessions
- Direct mounting of backend artifacts (repo + storage) with explicit authorization
- Deterministic, auditable session traces (index validation, commit SHA, memory snapshot)
- Revocable, least-privilege connector consent

## Roles

- **Architect** — ChatGPT Project (cognitive layer).
- **Developer** — Codex (developer layer, repo write/PR executor).
- **Session Manager** — Small CreateOS service issuing per-session tokens and exposing mount metadata.
- **Consent UI** — Human-facing, auditable consent surface for connector scopes.

## Preconditions

- Repository: `SamuelPasquale/createos-bootstrap` (branch: `main`).
- Session Manager reachable and configured with:
  - Signing key for short-lived session tokens
  - Repo metadata (repo name, default branch, allowed connectors)
  - Memory backend endpoint (append-only store)
- Consent UI wired to Session Manager for human approval and revocation.

## Canonical CreateOS-Native Steps

1. **Request session (Architect → Session Manager)**
   - Input: Creation ID (`C01`), requested scopes (repo read/write, memory read/write), optional storage mounts.
   - Output: Signed session token (JWT), session ID, repo metadata (repo URL, default branch, last indexed commit), memory endpoint URL.

2. **Consent & least-privilege grant (Human → Consent UI)**
   - Human is shown requested scopes, duration, and connector targets.
   - Human approves or rejects. On approval, Session Manager records an auditable grant (session ID, scopes, expiry, actor) and returns a connector authorization handle.

3. **Deterministic bootstrap (Architect)**
   - Validate token signature, expiry, and scopes.
   - Fetch repo metadata from Session Manager; confirm branch and latest indexed commit SHA.
   - Mount repo using the provided connector handle; mount memory endpoint read/write.
   - Load `.createos/index.json` (via mounted repo). On failure, request an index from Session Manager.
   - Enumerate required files via index (creation.yaml, specs, memory, decisions, tasks, progress) and rehydrate cognitive state.
   - Capture a bootstrap trace: session ID, commit SHA, index checksum, memory snapshot version, timestamp.

### Step 3.x — Fast path: LATEST.json
If present, **creation/08-progress/LATEST.json** is the fast-path for reconstructing the previous session. The Architect must load this file first and treat it as the canonical, human-approved summary of the last session (including `date`, `file`, `sha`, `summary`, and `next_steps`). If `LATEST.json` is missing or invalid, fall back to selecting the most recent dated file under `creation/08-progress/` by filename ordering.

4. **Developer flow (Codex)**
   - Receives the Architect’s instruction package plus session token for scoped repo/memory access.
   - Performs changes, commits, and returns PR. The session ID is attached to commit metadata for audit.

5. **Revocation & rotation**
   - Human can revoke the session via Consent UI; Session Manager invalidates the token and connector handle.
   - Architect handles revocation errors by halting mutations and requesting a new session.

## Error handling

- **Token validation failure**: abort bootstrap; request a fresh session from Session Manager.
- **Consent not granted**: surface the missing scopes; do not proceed.
- **Index unavailable**: request an authoritative index snapshot from Session Manager; log degraded mode.
- **Memory endpoint unavailable**: continue in read-only mode with explicit warning; block writes until restored.

## Auditability requirements

- Every session stores a bootstrap trace containing session ID, issued-at, commit SHA, index checksum, memory version, and approved scopes.
- Connector grants include actor, timestamp, scope list, and expiry; revocations are recorded with reason.
- Memory writes are versioned and append-only; each write links to session ID and commit SHA (if present).

## Transitional guidance

- The V0 dual-chat pattern is deprecated. All new work should use the CreateOS-native flow above.
- If Session Manager is unavailable, fall back to V0 only to unblock critical fixes; record the fallback in the progress log.

(End of protocol)
