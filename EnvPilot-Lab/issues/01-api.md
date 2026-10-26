# Exercise 1 — Repair API correctness and tenant isolation

**Target time:** 90 minutes. **Your role:** backend engineer repairing an API reported by QA. Start with one failing request; you do not need to understand every service first.

## The problem

An Environment is a workspace record owned by a project and its organization. A Team Alpha account should not gain access to Team Beta's records by changing an ID in a request. A Viewer should be able to read its team's records, but not create new ones.

The starter accepts some of these forbidden requests and some invalid names. The risk is unauthorized data access or creation, even if the dashboard hides a button. This exercise repairs server behavior, not card styling or real VM creation.

## Before you start

Read [the shared workflow](../docs/EXERCISE_WORKFLOW.md), including **Prepare API requests**, and the contract's [authentication/roles](../docs/API_CONTRACT.md) and [projects/environments](../docs/API_CONTRACT.md) sections. Use the discovered IDs and tokens from the shared setup, not IDs copied from grader output.

Run `python3 lab.py check 1` and keep the baseline output. An assertion such as `200 == 403` means a forbidden request was accepted. The initial pass/fail count is not a requirement; focus on the individual behaviors.

## Reproduce the problem

After running the shared Bash setup, try these independently and record their actual status/body:

```bash
# Team Alpha owner requests Team Beta's collection: expected 403.
curl -i "$BASE/api/environments/?organization=$BETA_ORG_ID" -H "Authorization: Token $OWNER_TOKEN"

# The same owner requests a Team Beta record: expected 404.
curl -i "$BASE/api/environments/$BETA_ENV_ID/" -H "Authorization: Token $OWNER_TOKEN"

# Team Alpha Viewer creates a record in its own project: expected 403.
curl -i "$BASE/api/environments/" -H "Authorization: Token $VIEWER_TOKEN" -H 'Content-Type: application/json' -d "{\"project\":$ALPHA_PROJECT_ID,\"name\":\"viewer-example\"}"

# Owner submits an invalid name: expected 400.
curl -i "$BASE/api/environments/" -H "Authorization: Token $OWNER_TOKEN" -H 'Content-Type: application/json' -d "{\"project\":$ALPHA_PROJECT_ID,\"name\":\"bad name\"}"
```

`POST /api/environments/` creates a database record; it is different from the **Provision** action. There is no create-record form required in this exercise, so use direct API requests. On the broken starter, a forbidden POST may actually create a record; record that side effect as evidence rather than repeatedly submitting it.

Also send a legitimate owner/developer request with a name such as `api-review-1`; it must return 201, `status: pending`, and a blank `provider_id`. Repairs must preserve this valid case.

## Required behavior

Use otherwise-valid inputs when testing access rules so validation errors do not obscure permission failures.

| Request / condition | Required outcome |
|---|---|
| Any protected product request without valid authentication | 401. |
| Owner, Developer, or Viewer reads its own organization's environments | 200, containing only that organization's records. |
| A collection is requested without membership in that existing organization | 403. A nonexistent organization is 404. |
| Detail belongs to another organization, or the environment does not exist | 404; do not reveal a foreign object by returning its data. |
| Owner/Developer creates in an authorized project | 201 with pending status and no provider resource. |
| Viewer creates in its own project | 403, with no record created. |
| Creation references a foreign or missing project | 404, with no record created. Outsiders must not be able to write. |
| Required fields are missing, or name/ID types and values are invalid | The contract's 400 response; no partial write. A valid positive but missing project ID is 404. |

Names must be 1–64 characters, start with an ASCII letter/digit, and contain only ASCII letters/digits, `_`, or `-` afterward. Reject empty strings, spaces, `bad name`, `../escape`, newline suffixes, and overlong names. Do not silently trim whitespace into a valid name. Duplicate names are allowed. Clients cannot set lifecycle/provider IDs through this create endpoint; unknown fields may be ignored.

Keep the documented JSON error envelope. Roles belong to memberships in a particular organization; never treat a familiar username or a role in another team as global authorization.

## Where to investigate

Read `backend/config/urls.py` → the relevant method in `backend/lab/views.py` → its serializers, access helper, and related models. `backend/lab/queries.py` builds the list queryset. The [code map](../docs/CODE_MAP.md) explains these responsibilities. Identify current behavior before deciding how to change it; this page does not prescribe a repair implementation.

## Acceptance criteria

- [ ] Every access/creation case in the table matches the API contract.
- [ ] Invalid input and denied requests do not create records.
- [ ] Legitimate reads and owner/developer creation still work.
- [ ] Regression tests cover valid access, foreign list/detail/project IDs, nonwriters, and name/input failures.
- [ ] Your note distinguishes authentication (identity), membership (team access), object scope (which record), and role (allowed action).

## Verification and deliverables

```bash
python3 lab.py check 1
```

Submit learner changes, regression tests, before/after request evidence, and an English note using [notes/TEMPLATE.md](../notes/TEMPLATE.md). The check uses isolated test data; IDs and memberships may differ from your interactive demo accounts. A final pass is necessary evidence, but your explanation is also assessed by [the rubric](../RUBRIC.md).
