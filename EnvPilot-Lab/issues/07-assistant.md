# Exercise 7 — Repair support assistant boundaries

**Target time:** 75 minutes. **Your role:** backend engineer making a support assistant respect evidence and ordinary product permissions.

## The problem

The assistant retrieves internal support documents and uses a deterministic fake model to produce an answer or request a read tool. In the starter, an answer may cite another organization's document, malformed/timeout output can become misleading advice, retrieved instructions can redirect the answer, and tool requests can bypass object permissions.

This is an API/data-boundary exercise, not a prompt-writing competition or a requirement to build a chat UI. No paid model, API key, or GPU is needed.

## Before you start

Read [the shared workflow](../docs/EXERCISE_WORKFLOW.md) and the [support-assistant contract](../docs/API_CONTRACT.md). Prepare owner/viewer/other-owner tokens and organization IDs. Inspect `backend/lab/assistant.py`, the `Assistant` view, and the relevant models/access rules.

`retrieval` means selecting support documents for the question; a `citation` is a document ID supporting the answer; a `tool` is an allowed application action requested by model output. All three must stay inside the authorized organization. Retrieved document text and model output are data to validate, not permission to bypass product rules.

## Reproduce the problem

Run `python3 lab.py check 7` and keep the failing cases. Then use the shared Bash setup for direct requests:

```bash
# Legitimate Team Beta request: evidence must belong to Team Beta.
curl -i "$BASE/api/assistant/" -H "Authorization: Token $OTHER_TOKEN" -H 'Content-Type: application/json' -d "{\"organization\":$BETA_ORG_ID,\"question\":\"Provisioning\",\"scenario\":\"normal\"}"

# Valid request, but fake model returns malformed output: expected safe fallback.
curl -i "$BASE/api/assistant/" -H "Authorization: Token $OWNER_TOKEN" -H 'Content-Type: application/json' -d "{\"organization\":$ALPHA_ORG_ID,\"question\":\"Provisioning\",\"scenario\":\"malformed\"}"

# Matching instruction-bearing fixture: expected safe fallback, not compliance with its text.
curl -i "$BASE/api/assistant/" -H "Authorization: Token $OWNER_TOKEN" -H 'Content-Type: application/json' -d "{\"organization\":$ALPHA_ORG_ID,\"question\":\"Unsafe\",\"scenario\":\"injection\"}"
```

Inspect response status, `answer`, `citations`, `tool`, and `fallback`; a 200 response alone does not establish correctness. Repeat normal authorized requests with both teams, and try a foreign organization using the wrong team's token. Use actual retrieved/fixture IDs when investigating tools; never assume a hardcoded environment ID is your own record.

## Required scenarios and outcomes

| Case | Required outcome |
|---|---|
| Normal authorized question with relevant evidence | 200, grounded answer, `fallback: false`, and valid citations drawn only from that organization's retrieved documents. |
| Request for an unauthorized existing organization | Reject the request under ordinary organization permissions (403). Do not return foreign documents. |
| No relevant evidence | 200 safe fallback, empty citations, null tool, `fallback: true`. Do not invent advice. |
| `malformed` or `timeout` model output | Safe bounded fallback with the same empty/null/true fields. |
| Instruction-only retrieved content / `injection` fixture | Do not treat it as an instruction or a source for a grounded answer; use safe fallback. |
| `tool` requests the allowed read for an authorized existing environment | Apply the ordinary object scope and return the permitted status information. A valid Viewer read must work. |
| Unknown tool / `forbidden_tool`, malformed tool request, or foreign/missing target | Safe fallback; do not perform the requested unauthorized action or reveal a foreign record. |

The valid API result shape is `{"answer":"...","citations":[...],"tool":null,"fallback":false}` (tool may be an allowed tool object). Fallback prose need not match an exact string, but it must avoid presenting unsupported advice as a grounded answer.

## Schema and permission requirements

- Validate model output before using it: exactly `answer` (string, at most 2000 characters), `citations` (list of integer document IDs), and `tool` (null or valid tool object). Reject wrong types, unknown fields, and invalid/foreign/fabricated citations.
- A non-tool answer requires at least one citation that actually supports it and belongs to the retrieved authorized evidence.
- The only tool is `{"name":"environment_status","environment_id":<integer ID>}`. It is read-only and scoped to the requested authorized organization. Unknown names, bad schema, missing/foreign objects, or permission failures must not bypass fallback.
- Authentication, membership, and object scope apply independently of what the model asks. Valid owner/developer/viewer reads must remain usable.
- Invalid API input follows the contract's 400 behavior; valid API requests with unusable model output use 200 fallback. Do not confuse these two failure types.
- The local fake timeout is deterministic. Keep failures bounded; any optional real adapter needs a deadline at most 2 seconds and the same validation/authorization rules.

Question strings are at most 200 characters; empty question is allowed for browsing available evidence. Supported API scenarios are `normal`, `timeout`, `malformed`, `tool`, `forbidden_tool`, and `injection`. Keep retrieval title matching case-insensitive and inside the requested organization.

## Acceptance criteria

- [ ] Authorized retrieval/answers/citations stay within the requested organization; foreign requests are rejected.
- [ ] Model and tool schemas, types, fields, and citation ownership/grounding are checked.
- [ ] Missing evidence, malformed output, timeout, and instruction-only content return safe bounded fallback.
- [ ] Only the allowed read tool can run, with ordinary permissions and valid Viewer access preserved.
- [ ] Regression/evaluation cases include both legitimate use and the negative cases above; answer wording is not exact-graded.
- [ ] The note explains grounding, data-versus-instruction boundaries, and remaining limitations.

## Verification and deliverables

```bash
python3 lab.py check 7
```

Submit learner changes, regression/evaluation tests, a small table of scenario → observed result → expected result, final check output, and an English [engineering note](../notes/TEMPLATE.md). Do not replace the task with a paid service or execute shell/mutation commands requested by retrieved/model text.
