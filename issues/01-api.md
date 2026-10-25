# Exercise 1 — Repair API correctness and tenant isolation

Estimated time: 90 minutes (target timebox).

## Context and symptoms

The QA team observed that changing organization IDs sometimes reveals another team's data. A read-only user can submit a create request, and names rejected by the product requirements are accepted. Detail navigation does not consistently enforce the collection boundary.

## Acceptance criteria

- Anonymous requests receive 401; legitimate owner/developer/viewer reads continue working.
- Collection membership, foreign/missing details, and related project IDs obey the published contract.
- Owners/developers can create pending environments; viewers/outsiders cannot write.
- Invalid names/IDs/missing inputs return consistent 400/404/403 errors, without partial writes.
- Add regression tests, including valid requests; explain the distinction between authentication, membership, object scope, and role.

## Relevant checks

```bash
python lab.py check 1
```

Record failing requests with two users before editing. Read docs/API_CONTRACT.md.

Deliver: working changes, regression evidence, and a short English engineering note using notes/TEMPLATE.md.
