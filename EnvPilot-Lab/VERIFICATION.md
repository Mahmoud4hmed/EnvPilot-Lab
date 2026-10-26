# Construction verification — 2026-10-25

This file preserves the original construction record and subsequent runtime verification. The latest update below supersedes the earlier Docker availability blocker for the checks explicitly listed.

## Latest documentation update — explicit exercise briefs (2026-10-26)

All seven learner issue pages now explain context, reproduction, expected behavior, investigation entry points, acceptance criteria, and deliverables. A shared exercise workflow provides Bash/WSL API session/ID discovery, failure interpretation, and evidence guidance. Both the workflow and detailed code map are registered in the browser guide; exercise links resolve to allowed learner documents.

Verification: 17 existing frontend smoke tests and the Next.js production build/TypeScript validation passed. Static checks validated local links, English content, balanced fences, and all 23 Bash blocks with `bash -n`; the shared API setup block was executed successfully from WSL and discovered real organization/project/environment IDs without creating product records. Manual browser review confirmed that all seven expanded pages and the shared workflow render, and their 30 relative document links map to registered guide pages. All 14 exercise/reset source files remain identical to the starter archive/manifest.

Exercise grading, incident activation, Ansible fixture runs, the mock, and full browser E2E scenarios were not executed for this documentation update. The request examples describe learner actions; only the read/session-setup block was run during verification. No exercise solutions were installed.

## Latest runtime update — readable workspace names and training instructions

Generated names now have readable card titles: `dev-4-060` displays as "Sample development workspace 60" with its sample project explained, and `check-<32 hex characters>` displays as "System check workspace" with its diagnostic purpose explained. Generated names and provider resource IDs remain available in Technical details; stored names, API values, and provisioning callback records are unchanged. Custom names outside these conventions are displayed as recorded. Resource references are described as sample or simulated resources in the main card.

The README now explains the fictional product, intended request/worker flow, terminology, card types, startup commands, the first 30 minutes, the exercise workflow, source layout, and the distinction between smoke checks and exercise completion. START_HERE and the in-app glossary use the same terminology.

Verification: 17 frontend smoke tests passed locally and inside Docker; the Next.js production build and its TypeScript check passed; `python lab.py check smoke` passed its PostgreSQL API smoke, frontend tests, and actual worker/provider operation. README relative links resolve, updated content is English, and all 14 exercise/reset files still match the unchanged snapshot/manifest. Manual browser review confirmed readable titles on real records, exact generated names in the expanded details, and no horizontal overflow at a 390px viewport; the viewport was restored. Browser E2E selectors were updated to trace the stored name independently of its display title, but that E2E suite was not executed for this update. No exercise repairs, resets, or incidents were applied.

## Latest runtime update — informative environment cards

Cards now label project/organization, explain the API-reported lifecycle, show the latest event, provider resource, and UTC timestamps, and provide status/role-specific next steps. Expandable technical details include record IDs and the authenticated API endpoint. Missing evidence is explicit; no VM address, resource health, or operation result is invented.

Twelve frontend smoke tests passed using the bundled Node runtime with the threads pool (six existing role/onboarding cases and six card cases). TypeScript validation and the Next.js production build passed. Browser review of a static preview rendered from the actual card component verified the four lifecycle layouts and the expandable details; its data was explicitly labeled as sample data. The default host Node test runner timed out starting workers, so it is not reported as passing.

Docker was initially unavailable (`doctor` timed out and Desktop displayed "Starting the Docker Engine"), then recovered. The updated web/backend images were built and the stack reached healthy status. Existing PostgreSQL migrations were already applied; no reset or reseed was needed. `python lab.py check smoke` passed: one PostgreSQL API/seed smoke test, all 12 frontend smoke tests inside Docker, and an actual Celery/provider success operation. These diagnostics can add their normal check records; existing learner records and notes were preserved.

Manual browser verification against the live lab confirmed real card metadata, expandable IDs/API endpoint, read-only viewer guidance with no Provision buttons, and no horizontal page overflow at a 390px viewport. The viewport was restored afterward. The full browser E2E suite and exercise checks were not run for this presentation update. No incidents were activated.

Only the dashboard presentation changed within the exercise reset scope; its loading/provisioning logic and the other 13 exercise source files are unchanged. The dashboard's reset archive and manifest were updated together so resetting Exercise 5 preserves the informative cards.

## Latest runtime update — generic identities and onboarding

### Persistent demo role selector

The dashboard now opens directly with a Role dropdown instead of a login form. It remembers role and organization preferences across remounts/reloads and reacquires a token for the selected fixed demo account. The local-only endpoint is explicitly enabled by Compose; ordinary product API permissions and the intentional exercise defects remain unchanged.

Verification executed for this update: nine PostgreSQL-backed demo-role tests passed (fixed account mapping, default-disabled endpoint, invalid selectors, unchanged viewer authorization, and password-independent switching); six frontend smoke tests passed (default owner, persistence, stale-response isolation, retry, outsider state, and glossary); TypeScript validation and the Next.js production build passed. Live HTTP checks confirmed owner/viewer/outsider sessions and the rendered Role dropdown without a password form. Browser-controlled manual verification was unavailable because local browser use was disabled in Work settings; the updated browser E2E cases were authored but not executed for this update.

`python lab.py check smoke` also passed after deployment, including its PostgreSQL API/seed check, the six frontend smoke checks inside Docker, and a real Celery/provider success operation.

Docker is now available and the existing local stack is running. The following were executed successfully on 2026-10-25:

- The identity migration passed its PostgreSQL regression test, including preservation of user/project/environment IDs, passwords, tokens, memberships, events, and operations. Repeated seeding preserved existing work.
- The migration was applied to the running lab. Before/after record counts and hashes of environment, operation, event, and membership data matched. Accounts are now `owner` and `other_owner`; organizations are Team Alpha and Team Beta.
- `python lab.py check smoke` passed: PostgreSQL-backed API/login/seed checks, three frontend smoke checks, and an actual Redis/Celery/fake-provider success round trip.
- The Next.js production build and its TypeScript validation passed. The updated web image was built and deployed with read-only learner-document mounts.
- Browser verification passed for `owner` login, the neutral organization label, Day 1 navigation, and the Exercise 1 acceptance-criteria page.
- All 14 exercise/reset source files still match their original starter snapshot. No learner exercise solutions were installed.

The dashboard now links to `/guide`, with the checklist, issue cards, API contract, commands, and glossary. Reference solutions and mock task cards are not exposed through this guide.

This update does not claim completion of the learner exercises, the independent mock, Ansible checks, incident repairs, or PostgreSQL concurrency grading. The original construction-only checks and limitations remain recorded below.

## Original construction record

The original local checks ran while Docker was unavailable. SQLite and synchronous tasks were not treated as evidence of PostgreSQL concurrency or a real worker. Reference repairs remain outside the learner workspace, and the starter retains its intentional defects.

## Executed and passed

| Check | Evidence / scope |
|---|---|
| Dependency installation | Exact Python dependencies installed into sibling instructor venv; npm install succeeded with zero reported vulnerabilities |
| Linux dependency compatibility | pip resolver dry-run against CPython 3.13 Linux wheel platforms succeeded; this is metadata validation, not a container build |
| Image tags | Explicit Python/PostgreSQL/Redis/Nginx image tags verified against Docker Hub metadata |
| Compose configuration | Base, both incident overlays, and independent mock parsed successfully with Compose v2.40.3 |
| Django schema | System check, migrations applied to local SQLite, no pending generated migrations in training or mock |
| Starter API smoke | Login credentials, authenticated navigation, missing record, and two additive seed runs passed (SQLite test DB) |
| Frontend | Training and mock production Next.js builds completed; TypeScript checks passed |
| Provider simulator | Real HTTP server tests passed: eight parallel provider requests, key conflict/scope, pre-creation transient failure, permanent rejection, created-then-timeout reconciliation |
| Training grader validation | Broken starter rejected on intended assertions; instructor reference accepted. Backend includes real HTTP calls with synchronous task execution; no actual broker/worker claim |
| UI grader validation | Broken starter rejected; reference UI accepted, including deferred-response, error recovery, token change and cleanup checks |
| Mock grader validation | Independent broken API/UI rejected; separate reference API/UI accepted on local checks. PostgreSQL parallel archive case excluded |
| CLI/exam safety | Seven harness tests passed: explicit reset flag, backup, note preservation, incident toggles, independent copy, timer resume/expiration and submission snapshot/report persistence |

Exact per-test evidence and counts are recorded locally in sibling `EnvPilot-Instructor/validation/local-results.json`, XML reports and logs. Those construction materials and reference solutions are excluded from the public repository; they are not required for learner checks or the mock.

## Original blockers / checks not executed at construction time

Docker CLI and Compose are installed. Docker Desktop was started, but its backend reported:

```text
starting services: initializing Inference manager:
listening on unix://<HOME>\AppData\Local\Docker\run\dockerInference:
The file cannot be accessed by the system.
(listener: The filename, directory name, or volume label syntax is incorrect.)
```

`docker info` did not complete; `python lab.py doctor` reported that the Engine failed to answer within 20 seconds. WSL2 Ubuntu is installed. No factory reset, host service changes, or Docker data deletion was performed.

Consequently these remain **unverified**, not passed:

- Clean Docker image build/start, container health and documented login through Nginx.
- Real PostgreSQL migrations/query plans and eight concurrent API requests; mock concurrent archive.
- Actual Redis/Celery worker/provider round trips, retries and parallel redelivery.
- Activation/repair/recreation of proxy and queue incidents.
- Ansible execution inside its isolated container, unchanged second run and changed-input verification.
- Browser end-to-end path through the full stack.
- Full independent mock container startup and service grading. Timer/isolation/submission logic was unit-tested separately.

## Next concrete commands

Ensure Docker Engine is running in Linux containers mode, then run these commands from the repository root:

```powershell
cd EnvPilot-Lab
python lab.py doctor
python lab.py up
python lab.py check smoke
```

Smoke must pass. Exercise checks are expected to fail until you complete each exercise. Setup failures are not training failures.

For an instructor using the original authoring installation (with local reference materials), the following completes construction verification without touching learner source or starting the learner's exam clock. This construction-only script and its reference copies are excluded from the public repository:

```powershell
cd 'D:\Code\EnvPilot-Training'
python EnvPilot-Instructor/validate_docker.py
```

That script uses separate Compose projects and ports 18090–18093 for starter/reference integration checks and mock copies. It preserves diagnostic volumes. It checks PostgreSQL parallel requests, actual worker scenarios, Ansible behavior, and independent mock API/UI/proxy behavior. Incident and browser checks can then be run in the instructor reference copy; no solutions need to be copied into the learner workspace.

First learner action: follow DAY_1.md's 30-minute baseline investigation, then open issues/01-api.md. Start the real independent mock later with `python lab.py exam start`.
