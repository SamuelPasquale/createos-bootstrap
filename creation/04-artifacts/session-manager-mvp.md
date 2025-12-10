# Session Manager & Persistent Memory — MVP Blueprint (C01)

## Intent
Replace the V0 dual-chat workaround with a CreateOS-native session startup that delivers first-class memory, secure backend mounting, and auditable boot traces for the Architect + Codex workflow.

## Objectives
- Deterministic session boots with signed tokens and repo metadata from a Session Manager.
- Explicit, revocable consent for connector scopes (repo + storage).
- Append-only, versioned Creation memory accessible across sessions.
- Single-click "Resume Creation" UX that rehydrates memory and validates indexes without manual chat moving.

## Components

### Session Manager (service)
- Issues short-lived JWT session tokens (session_id, Creation ID, scopes, expiry, issued_at, nonce).
- Publishes repo metadata: repo name, default branch, latest indexed commit SHA, `.createos/index.json` checksum.
- Provides connector authorization handle for repo/storage mounts after consent.
- Records audit events: issuance, consent grant, revocation, bootstrap trace uploads.

### Consent UI (human UX)
- Surfaces requested scopes, duration, and connector targets.
- Requires explicit human approval per session; persists audit log (actor, scopes, expiry, timestamp, session_id).
- Supports immediate revocation; emits revocation event consumed by Session Manager.

### Persistent Memory Service
- Append-only log keyed by (Creation ID, session_id, memory_version).
- Entry envelope: {session_id, commit_sha?, timestamp, change_set, checksum, previous_version}.
- Supports read (latest or by version) and append; manual compaction allowed by writing a summarized entry.
- Exposes audit feed for all writes and revocations.

### Repo + Storage Mounts
- Repo mount uses connector handle scoped to repo and branch from Session Manager metadata.
- Optional storage mount for artifact blobs; scope-limited and tied to session token.

## Session startup flow (CreateOS-native)
1. Architect requests session with scopes (repo r/w, memory r/w, storage optional).
2. Session Manager returns JWT, session_id, repo metadata, memory endpoint, and awaits consent.
3. Human reviews scopes in Consent UI; on approval, Session Manager issues connector handle and records grant.
4. Architect validates JWT, mounts repo/storage, loads `.createos/index.json`, rehydrates memory from latest version.
5. Architect records bootstrap trace back to Session Manager (session_id, commit SHA, index checksum, memory version, timestamp).
6. Codex receives session token + instructions; attaches session_id to commits/PR notes for audit.
7. Human can revoke session; Session Manager invalidates token and handle; Architect halts writes and requests new session.

## Persistent memory API (MVP)
- `POST /memory/{creation_id}/entries`: append entry; requires session token with `memory:write`.
- `GET /memory/{creation_id}/entries?limit=n&cursor=version`: read latest or paginated history.
- `GET /memory/{creation_id}/entries/{version}`: fetch specific version.
- `POST /memory/{creation_id}/compactions`: append summarized entry referencing previous_version list.
- Entries are immutable; compaction writes a new summarized entry rather than rewriting history.

## Resume Creation UX (single-click)
- Architect selects Creation → invokes Session Manager with `resume=true` and last-known session trace (optional).
- Session Manager pre-populates repo metadata and last known memory version; prompts human for consent.
- After mount, Architect verifies index checksum and memory version; any mismatch triggers a blocking warning and offers a safe re-sync path (pull latest index, reload memory, re-run bootstrap trace).
- UI surfaces bootstrap trace (session_id, commit SHA, memory version, scopes) for audit.

## Tests & acceptance (MVP)
- **End-to-end bootstrap test**: start session, validate index checksum, mount repo, rehydrate memory, record trace.
- **Security/consent test**: revoke session; confirm connector handle is invalidated and memory writes are rejected.
- **Durability test**: append memory entry in session A; start session B and confirm the entry is available with matching checksum.
- **Audit test**: verify audit log includes issuance, consent grant, bootstrap trace, revocation, and memory writes with session IDs.

## Open questions / risks
- Key management for Session Manager signing keys (rotation schedule, storage).
- Where to host audit logs for tamper resistance (e.g., append-only storage or external ledger).
- Handling offline consent or degraded mode when Consent UI is unreachable (likely block writes/read-only fallback).
