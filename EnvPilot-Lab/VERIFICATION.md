# Construction verification — 2026-10-25

الحالة بصراحة: الكود والـlocal checks اتنفذوا، لكن تشغيل Docker الكامل **لسه غير متحقق** على الجهاز ده.
متعتبرش SQLite أو synchronous task execution إثبات لـPostgreSQL concurrency أو Celery worker حقيقي.
مواد الإصلاح والتحقق موجودة خارج learner workspace. نسخة التدريب محتفظة بالعيوب المقصودة.

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

## Blocked / not executed

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

افتح Docker Desktop وحل startup error الأول. بعد ما Engine يشتغل بوضع Linux containers:

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
