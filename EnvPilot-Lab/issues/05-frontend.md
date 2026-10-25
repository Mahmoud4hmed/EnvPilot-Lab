# Exercise 5 — Repair the asynchronous environment dashboard

Estimated time: 90 minutes (target timebox).

## Context and symptoms

Users see an empty-looking screen while loading, stale data after changing organizations, and old errors after recovery. Provision requests are shown as ready too early. Product also requests a small name-search control for the current page.

## Acceptance criteria

- Explicit loading/error/empty states; successful refresh clears the previous error.
- New organization/status/token takes precedence over late responses; requests and polling clean up on unmount.
- Accepted provisioning is displayed truthfully; refresh or polling eventually reflects server state. Use a polling interval between 0.5 and 2 seconds for deterministic checks.
- Add accessible Search text input filtering current page names case-insensitively; preserve status filtering and Refresh.
- Keep API responses typed and handle request failures; backend remains authorization authority.
- Pass deterministic UI checks and, with healthy stack, browser sign-in → provision → observed server readiness. No styling or component-structure grading.

## Relevant checks

```bash
python lab.py check 5
docker compose run --rm web npm run typecheck
python lab.py e2e
```

Use deterministic delayed responses in tests. A hidden button alone does not secure an endpoint.

Deliver: working changes, regression evidence, and a short English engineering note using notes/TEMPLATE.md.
