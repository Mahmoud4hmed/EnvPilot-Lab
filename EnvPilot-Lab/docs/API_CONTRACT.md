# EnvPilot API contract (target behavior for the exercises)

This specifies intended behavior. Starter smoke covers only infrastructure and baseline paths; some target behaviors intentionally fail.
URLs end with `/`. JSON UTF-8. Token header: `Authorization: Token <token>`.
No browser-only authorization: all object and role checks apply server-side, including assistant tools.

## Authentication and roles

The local dashboard uses a demo **Role** dropdown instead of a login form. It calls `POST /api/demo-session/` with `{"role":"viewer"}` to receive `{username, token, memberships}` for a fixed seeded account. Supported selectors: owner, developer, viewer, other_owner, dual, outsider. Tokens represent the real account; this endpoint never grants a client-supplied role to an arbitrary user. Unknown roles return 400; missing/inactive/staff/superuser accounts cannot be selected. Responses use `Cache-Control: no-store`.

This teaching-only endpoint is enabled explicitly by Compose's `LAB_DEMO_ROLE_SWITCH=1`. Without that setting it returns 404. It is intended for the loopback-only local lab. The dropdown saves only role/organization preferences; product API endpoints retain their authentication and authorization contracts below. The independent mock has its own login flow.

`POST /api/login/` with `{"username":"owner","password":"LabPass123!"}` → 200 `{"token":"..."}`; invalid credentials 400.
`GET /api/me/` → `{"username":"owner","memberships":[{"organization":1,"name":"Team Alpha","role":"owner"}]}`.
Unauthenticated product requests: 401. Invalid/expired token: 401. Login uses DRF's standard token view error format; all other API errors use the envelope below.

Any membership reads its own organization. Owner/developer create environments and provision. Viewer reads only. A role in one organization gives no privileges in another.
Organization collections requested without membership: 403. Nonexistent organization: 404. Object detail outside memberships: 404 (same as nonexistent ID).
Provision action/operation detail use 403 for an existing object with insufficient organization membership/role. This deliberate difference is part of the contract.

## Errors

```json
{"error":{"code":"invalid","details":{"name":["Enter a valid value."]}}}
```

Codes: `invalid` 400; `unauthenticated` 401; `forbidden` 403; `not_found` 404; `conflict` 409.
Details can be a field object or a detail object; prose need not match exactly. No successful writes on errors.

## Projects and environments

`GET /api/projects/?organization=1` → 200 `[{"id":1,"name":"Team Alpha project 1"}]`.
`GET /api/environments/?organization=1&status=pending&page=1&page_size=20` → 200:

```json
{"count":80,"results":[{"id":240,"name":"dev-4-060","project":4,"project_name":"Team Alpha project 4","organization":1,"organization_name":"Team Alpha","status":"pending","provider_id":"","latest_event":"Seed history available","created_at":"2026-10-25T00:00:00Z","updated_at":"2026-10-25T00:00:00Z"}]}
```

Example IDs/counts/timestamps illustrate shape, not guaranteed fixture IDs. Organization is required positive integer; page defaults 1; page_size defaults 20, capped 100. Nonpositive/noninteger pagination: 400. Unknown status: 400. Empty status means no status filter. Ordering: descending numeric environment ID, deterministic across pages. Count is total after filtering. Page beyond end: 200 with empty results. Never include foreign rows.
`GET /api/environments/{id}/` → same row shape, 200 or 404.
Latest event is the highest numeric event ID; null if none. All list sizes must preserve this result.

`POST /api/environments/` with `{"name":"review-api-4","project":1}` → 201 row with pending status and blank provider_id.
Name: 1–64 characters, starts ASCII letter/digit, remaining characters ASCII letters/digits/underscore/hyphen. No whitespace normalization; invalid whitespace is rejected. Project: existing positive integer ID within the caller's memberships. Foreign/missing project: 404. Viewer: 403. Required/invalid fields: 400. Name uniqueness is not required. Client cannot set lifecycle/provider_id through this endpoint; unknown input fields may be ignored. This exercise has no update/delete endpoint.

## Provisioning and idempotency

`POST /api/environments/{id}/provision/`, header `Idempotency-Key: demo-001`, body `{"scenario":"success"}` → 202:

```json
{"id":9,"environment":3,"kind":"provision","key":"demo-001","status":"queued","attempts":0,"error":"","created_at":"2026-10-25T00:00:00Z"}
```

Only pending environments accept a **new** operation. Upon acceptance, environment becomes provisioning (worker may also enforce transition). Ready/failed/provisioning + new key: 409. Replaying a prior accepted key is checked before lifecycle rejection.
Key required, 1–80 characters, scoped by `(organization, operation kind)`; body fingerprint includes environment ID + scenario (default success). Same key + identical request → 200 and same logical operation, including after terminal status. Same key + different environment or scenario → 409 with no side effects. Another organization may reuse the same literal key.
Eight concurrent identical requests → one logical operation and consistent 200/202 responses. Do not rely on an in-process Python lock for cross-process API calls.
Scenarios: success, transient, lost_response, permanent. Unknown scenario: 400. Missing environment: 404.

`GET /api/operations/{id}/` → 200 operation shape above. Keep useful nonempty error for terminal provider failures. Status, not a successful POST alone, tells the UI readiness.
At most 3 provider creation attempts per operation; HTTP connect timeout ≤1s/read timeout ≤1s, retry delay ≤2s for this simulator. Terminal provider validation failure is not retried. Transient pre-creation failure retries. Lost response reconciles before assuming failure. Bounded scenarios must settle in ≤25s on an otherwise healthy stack; this is a liveness allowance, not a DB performance grade.
Tasks can be delivered multiple times concurrently. They must not create duplicate remote resources, regress terminal state, or reset the retry budget. Remote effects require provider idempotency/reconciliation; DB atomicity alone is insufficient.
Broker publish failure/outbox delivery recovery is a documented production follow-up, outside this two-day exercise; tests assume healthy broker at API acceptance.

## Provider simulator (internal only)

Base: `http://provider:9000`. `GET /health` → 200.
`POST /resources`, JSON `{"name":"review-api-4","scenario":"success"}`, `Idempotency-Key` header → 201 `{"id":"vm-..."}`.
Stable key same body returns 200 same resource. Same key + changed body after creation: 409. Without a key each POST is an independent effect. A safe remote key must include organization and operation kind.
`GET /by-key/{urlencoded-key}` → 200 `{"id":"vm-..."}` or 404 if no resource. `GET /resources` → full simulator ledger for local diagnosis only; never expose this through product API.
`transient`: first request for key returns 503 before creation, next succeeds.
`lost_response`: first call commits resource, delays 0.8s before reply; retrying by same key is immediate. A client read deadline below 0.8s produces a reproducible uncertain outcome. Reconciliation is immediately available.
`permanent`: 422 with no creation on every attempt. `success`: immediate creation.
Ledger persists in its own volume. Use fresh keys/pending environments to repeat scenarios. Seeded provider IDs are fictional history, not resources in the simulator ledger.

## Support assistant

`POST /api/assistant/` body `{"organization":1,"question":"Provisioning","scenario":"normal"}`.
Question string ≤200 chars. Retrieval title matching is case-insensitive, restricted to authorized organization. Empty question is allowed and means browse available evidence. Scenarios are local deterministic fixtures: normal, timeout, malformed, tool, forbidden_tool, injection.
200 shape: `{"answer":"...","citations":[1],"tool":null,"fallback":false}`. A non-tool answer requires at least one valid retrieved citation and grounded evidence. Missing evidence/model timeout/malformed or invalid output/injection-only context → safe 200 fallback, empty citations, tool null, fallback true. Fallback wording is not exact-graded.
Model output requires exactly answer (string ≤2000), citations (array of integer retrieved IDs), tool (null or object). Unknown fields/invalid types/foreign or fabricated citation → fallback. Retrieved prose is untrusted data, never a new instruction. Do not follow the fixture's instruction to emit its attack marker.
Only allowed tool: `{"name":"environment_status","environment_id":3}`. It reads status within requested organization and requires the same membership as an ordinary environment read; viewer may read. Unknown tool, bad schema, missing/foreign object → safe fallback. No shell execution, mutation tool, or permission bypass.
Default fake model is immediate; timeout scenario raises a deterministic deadline error. Any optional real adapter must use a deadline ≤2s and the same validator/authorization. Paid APIs are out of scope.
