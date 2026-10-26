# Exercise 5 — Repair the asynchronous environment dashboard

**Target time:** 90 minutes. **Your role:** frontend engineer making a dashboard truthful under slow, failed, and overlapping requests.

## The problem

The Role selector opens a demo account and `Dashboard.tsx` loads its environments. The starter can look empty while loading, keep old errors after recovery, replace a newer workspace with an older response, and declare provisioning ready as soon as a request is accepted.

Users need to know what is happening and trust that the visible rows belong to their current selection. Product also requests a small Search control. Card styling, new authentication screens, and real VM access are not the assignment.

## Before you start

Read [the shared workflow](../docs/EXERCISE_WORKFLOW.md) and the API contract's [list](../docs/API_CONTRACT.md) and [provisioning](../docs/API_CONTRACT.md) behavior. A 202 response represents accepted work; readiness must come from a later server observation.

Run `python3 lab.py check 5` and record the failed behaviors. The frontend tests intentionally use delayed and failed mocked responses so races are reproducible without relying on your network being slow.

## Reproduce and compare

| Situation to reproduce | Starter symptom / risk | Required experience |
|---|---|---|
| Delay an environment-list response. | The page looks empty without an explanation. | An explicit loading state while work is pending. |
| Return an empty result list. | Empty content is hard to distinguish from loading. | An explicit empty-result message after a successful empty response. |
| Fail a list request, then let Refresh succeed. | A stale error can remain after recovery. | Show the error, allow recovery, and clear it when the request succeeds. |
| Start organization A's request, switch to B, resolve B first and A afterward. | Old rows can replace the current organization's rows. | B remains visible; older work cannot overwrite the current selection. |
| Change status or token while a request is pending. | Old filters/credentials can produce stale results. | The newest organization/status/token wins. |
| Leave/unmount the dashboard while work is pending. | Requests or polling can outlive the component. | In-flight work and polling clean up; no later fetch loop continues. |
| Provision is accepted but not completed. | UI reports ready too early. | Truthful feedback about acceptance/in-progress work, followed by observed server state. |

For manual investigation, browser Network throttling/offline controls can expose loading and recovery. The **Developer · both teams** account lets you change organizations. Use deterministic mocked response ordering in regression tests; manual timing alone is not sufficient race evidence.

## Requested Search feature

Add an accessible text input labeled **Search** that filters environment names on the **currently loaded page**, case-insensitively. For example, loaded names `alpha` and `beta` should show only `beta` after entering `BETA`; clearing the input restores both.

Technical names such as `dev-4-060` remain the underlying environment names even when cards show friendly titles. Support name matching; matching friendly titles as well is optional. This task does not require server-wide search, new pagination, or a backend search endpoint. Preserve the Status control and Refresh behavior.

## Where to investigate

- `frontend/components/Dashboard.tsx`: loading, response ordering, feedback, lifecycle actions, and cleanup.
- `frontend/lib/api.ts`: typed responses and authenticated requests.
- `frontend/tests/dashboard.test.tsx`: deterministic observable behavior cases.
- `EnvironmentCard.tsx` and `app/page.tsx`: understand their presentation/session boundaries without redesigning the app.

The backend is still the authorization authority. Hiding a Provision button is useful UI behavior, but does not replace server permissions.

## Acceptance criteria

- [ ] Distinct accessible loading, error, and empty states; successful refresh clears an earlier error.
- [ ] New organization/status/token takes precedence over late responses.
- [ ] Requests and polling clean up on unmount.
- [ ] Provision acceptance is not reported as completed readiness; a later read reflects the actual server outcome.
- [ ] Refresh/polling eventually observes completion. Use a polling interval of 0.5–2 seconds for deterministic checks.
- [ ] Accessible, case-insensitive Search filters current-page names; Status and Refresh remain usable.
- [ ] Responses remain typed; failures are handled; no component layout or styling convention is required.
- [ ] Regression evidence covers the cases above and a valid provisioning path through the running stack.

## Verification and deliverables

```bash
python3 lab.py check 5
docker compose run --rm web npm run typecheck
python3 lab.py e2e
```

The browser path requires healthy API/Redis/worker/provider services: select a demo role → request provisioning → independently observe server readiness. Keep the deterministic component checks and live-browser evidence separate; do not describe an unexecuted E2E check as passed.

Submit frontend changes, regression evidence, check/typecheck results, actual browser results when executed, and an English [engineering note](../notes/TEMPLATE.md). Record unrelated setup/backend blockers explicitly rather than replacing server truth with an optimistic ready label.
