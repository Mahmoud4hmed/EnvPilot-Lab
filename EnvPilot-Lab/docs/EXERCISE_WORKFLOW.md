# How to work on an exercise

An exercise is a product issue to investigate and repair in source code. Environment cards are records you can use as evidence; they are not assignments to complete one by one. Each exercise page explains its problem, reproduction steps, expected behavior, and deliverables.

## Before you start

Run commands from `EnvPilot-Lab/`. Use `python3` instead of `python` in WSL/Linux if needed.

```bash
python3 lab.py doctor
python3 lab.py check smoke
```

If the stack is stopped, run `python3 lab.py up` first. Smoke should pass on healthy infrastructure. A Docker connection, import, build, or test-collection failure is a setup problem; a failed assertion about product behavior is normally part of the exercise. Do not reset your source or database to make a check pass.

## The investigation loop

1. Read one issue page and the relevant [API contract](API_CONTRACT.md) section.
2. Run `python3 lab.py check NUMBER` to collect baseline evidence. Start with one failed behavior, not the whole failure list.
3. Reproduce that behavior and record the account, organization, input, expected result, and actual result.
4. Trace the request through the listed learner files. Write a hypothesis before editing.
5. Make your repair, add appropriate regression tests, and rerun the exercise check. Preserve valid behavior as well as rejecting invalid requests.
6. Compare every acceptance criterion with your evidence and write a short English note using [the template](../notes/TEMPLATE.md).

The checks create test databases and, where documented, diagnostic live records or fixture files. They do not install repairs. Some grader users/data differ from the interactive seed: permissions depend on the account's membership in the relevant organization, not on a special username or a fixed numeric ID.

## Prepare API requests

The following examples use **Bash in WSL/Linux**, `curl`, and Python's standard library. On PowerShell, use an API client or adapt the shell variable syntax and use `curl.exe`. This setup only obtains demo tokens and reads IDs; it does not create environments.

Copy this block into the same terminal where you will run the request examples:

```bash
BASE=http://localhost:8090
OWNER_TOKEN=$(curl -fsS "$BASE/api/demo-session/" -H 'Content-Type: application/json' -d '{"role":"owner"}' | python3 -c 'import json,sys; print(json.load(sys.stdin)["token"])')
VIEWER_TOKEN=$(curl -fsS "$BASE/api/demo-session/" -H 'Content-Type: application/json' -d '{"role":"viewer"}' | python3 -c 'import json,sys; print(json.load(sys.stdin)["token"])')
OTHER_TOKEN=$(curl -fsS "$BASE/api/demo-session/" -H 'Content-Type: application/json' -d '{"role":"other_owner"}' | python3 -c 'import json,sys; print(json.load(sys.stdin)["token"])')
ALPHA_ORG_ID=$(curl -fsS "$BASE/api/me/" -H "Authorization: Token $OWNER_TOKEN" | python3 -c 'import json,sys; print(json.load(sys.stdin)["memberships"][0]["organization"])')
BETA_ORG_ID=$(curl -fsS "$BASE/api/me/" -H "Authorization: Token $OTHER_TOKEN" | python3 -c 'import json,sys; print(json.load(sys.stdin)["memberships"][0]["organization"])')
ALPHA_PROJECT_ID=$(curl -fsS "$BASE/api/projects/?organization=$ALPHA_ORG_ID" -H "Authorization: Token $OWNER_TOKEN" | python3 -c 'import json,sys; print(json.load(sys.stdin)[0]["id"])')
BETA_PROJECT_ID=$(curl -fsS "$BASE/api/projects/?organization=$BETA_ORG_ID" -H "Authorization: Token $OTHER_TOKEN" | python3 -c 'import json,sys; print(json.load(sys.stdin)[0]["id"])')
BETA_ENV_ID=$(curl -fsS "$BASE/api/environments/?organization=$BETA_ORG_ID" -H "Authorization: Token $OTHER_TOKEN" | python3 -c 'import json,sys; print(json.load(sys.stdin)["results"][0]["id"])')
```

`OWNER_TOKEN` and `VIEWER_TOKEN` belong to Team Alpha accounts. `OTHER_TOKEN` belongs to Team Beta's owner. The ID variables come from each account's own authorized responses; do not assume seed IDs are always 1 or 2. If this block fails, inspect the failing HTTP response and check the running stack before continuing.

For example, this reads Team Alpha's environments as its owner:

```bash
curl -i "$BASE/api/environments/?organization=$ALPHA_ORG_ID" -H "Authorization: Token $OWNER_TOKEN"
```

`-i` displays the HTTP status and headers as well as JSON. For POST requests, include `Content-Type: application/json`. Values such as `ENV_ID` or `OPERATION_ID` in an issue must be set from the response you just received; fixture IDs printed by a grader are not necessarily live database IDs. The account's API token, not the Role dropdown alone, determines the identity of a direct request.

## Read a failed assertion

`assert 200 == 403` means the observed response was 200 but the test required 403. It is evidence of the wrong behavior, not an instruction to change the test.

| Status | Meaning |
|---|---|
| 200 | A read or replay succeeded; inspect the response content too. |
| 201 | A new record was created. |
| 202 | Background work was accepted, not necessarily completed. |
| 400 | Invalid input. |
| 401 | Authentication is missing or invalid. |
| 403 | Access is forbidden. |
| 404 | Missing object, or an object deliberately concealed outside the caller's scope. |
| 409 | A lifecycle or idempotency conflict. |

Use the contract for endpoint-specific distinctions. For example, a foreign collection and a foreign object detail intentionally do not return the same status.

## What to submit

- Your learner source/configuration changes and appropriate regression tests.
- Before/after commands or requests, expected/actual results, and final check output.
- An English engineering note: diagnosis, decisions, tradeoffs, and remaining risks. [The rubric](../RUBRIC.md) also assesses this explanation; passing automatic checks alone is not the whole deliverable.

Use the [code map](CODE_MAP.md) to navigate files. Optional hints are requested explicitly with `python3 lab.py hint NUMBER LEVEL`; do not open higher levels unless you want them. Incident activation and the independent mock are separate deliberate actions, not baseline setup steps.
