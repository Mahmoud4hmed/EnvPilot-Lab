# Independent mock — 180 minutes, 100 points

These are fictional EnvPilot requirements, not an employer's assessment questions. Timeboxes: inspect/baseline 15 min, API 60 min, UI 45 min, incident 35 min, tests/notes/submission 25 min. Prioritize a working, explained result.

Start: http://localhost:8091, mahmoud / LabPass123!. Also viewer (Nile viewer), nora (Delta owner); same password. This is an independent DB and codebase. Source reload: `docker compose restart api worker`; frontend hot reloads.

## Task A — Archive environment handover memos

Add `POST /api/memos/{id}/archive/`. Only the owning team's owner may archive a memo. Unauthenticated 401; viewer of same team 403; missing/foreign object 404. Success 200 returns `{id,title,archived_at}` with non-null server UTC timestamp.
First archive creates exactly one Audit(action='archived'). Replays, including concurrent calls, return same timestamp and do not add audits. A transaction must cover the transition and audit. Do not change ordinary GET/PATCH behavior.
Provide tests for valid request, anonymous/viewer/foreign access, missing record and replay. IDs are obtained from GET /api/memos/. Body is empty; unknown body fields may be ignored.

## Task B — Reliable memo title saving

The editor loses unsaved text after a failed save and displays a change before confirmation. Two fast clicks can submit overlapping saves.
Keep draft and last confirmed heading when save fails; show useful error. While a save is pending, allow only one request and prevent a second submission (disable Save and guard the handler). Commit the heading only after server success, then re-enable Save. Preserve draft semantics if the input is edited; disabling the input while saving is acceptable. Tests must use deterministic delayed/rejected responses; no CSS preference grading.
PATCH /api/memos/{id}/ already works: owner only; title is a nonblank string ≤60 chars; valid 200 row, invalid 400, viewer 403, foreign/missing 404.

## Task C — Restore the memo service path

Login and /health/ work, but the memo list through the local gateway returns 502. Diagnose with curl, logs, port/config evidence. Apply a durable config repair. Verify after `docker compose up -d --force-recreate proxy`; do not modify host services. Record root cause, evidence, repair and verification in NOTES.md.

## Checks and submission

From the original lab: `python lab.py exam status` / `python lab.py exam submit`.
From this workspace, `python mock.py check` runs external behavioral checks, UI tests and service recreation. These tests are the acceptance checks; you may add your own.
Timer is advisory; work remains intact at expiration. Closing a terminal does not pause the clock. Re-running start resumes the same workspace and start time.

## Scoring (separate 100)

API functional correctness incl. replay/concurrency 25; authorization 15; UI behavior 20; durable incident verification 15; your meaningful tests 10; evidence-based diagnosis 10; engineering explanation/tradeoffs 5. Automatic maximum 75; remaining 25 require manual review. Partial credit by independent passed behavior criteria. Infrastructure failures remain ungraded.
NOTES.md must explain root cause, tests run, tradeoffs, and remaining risks. Submission writes automatic evidence, a provisional score /100 with manual points pending, and three prioritized improvement actions. No solution is shown.
