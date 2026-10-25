Act as a senior software engineer, technical interviewer, and hands-on lab designer. BUILD a complete, runnable training repository called EnvPilot Lab in a new directory. Do the implementation now; do not stop at a plan or a list of exercises.

The learner is an experienced software engineer/architect with a background in Python, Django/DRF, Flask, React/Next.js, PostgreSQL/MySQL, Redis, Linux, Docker, Nginx, multi-tenant SaaS, deployments, and applied LLM/RAG integration. This lab provides focused practice before a self-paced, three-hour Senior Software Engineer assessment.

The public role emphasizes Django REST APIs, Next.js/TypeScript, Celery, Linux/networking, cloud/VM lifecycle operations, Ansible, and applied AI:
https://easyenv.io/careers/senior-software-engineer
Use that as context, not as evidence of the actual interview questions. Do not claim to reproduce EasyEnv's assessment.

## 1. The learning outcome

Create approximately 14 hours of focused training over TWO days, followed according to the schedule below. The final three-hour mock is INCLUDED in those 14 hours.

I must do meaningful engineering work myself: investigate an unfamiliar repository, reproduce defects, implement changes, run tests, diagnose services, and explain tradeoffs. Supply a functional starter application containing deliberately incomplete features and reproducible defects. Do not solve the learner exercises in the delivered starter.

Keep the scope realistic for two days. Prioritize backend correctness, asynchronous reliability, and debugging. Supply enough working scaffolding that I spend my time engineering rather than creating boilerplate. Do not build a course platform, LMS, or elaborate grading website.

Use clear English throughout the lab: UI text, orientation, conceptual explanations, hints, issue cards, API contracts, and interview-style deliverables.

## 2. The product and local stack

The fictional product manages temporary development environments for software teams.

Use:
- Django + Django REST Framework.
- PostgreSQL.
- Redis + a real Celery worker.
- Next.js + React + TypeScript.
- Nginx as the local reverse proxy.
- A small deterministic fake cloud-provider HTTP service.
- A small Ansible exercise running inside an isolated container.

Use currently supported, mutually compatible stable versions. Verify compatibility using official documentation and pin dependencies. Prefer familiar, maintainable choices over extra infrastructure.

Everything must work locally with Docker Compose. Support Linux/WSL2; document Windows Docker Desktop setup through WSL2. Keep laptop resource consumption reasonable. Do not require a paid account, API key, cloud subscription, real VM, Kubernetes cluster, or GPU. Do not mount the host Docker socket, change host services, or deploy publicly.

Seed two fictional organizations, several users with different memberships, projects, environments, operation records, and useful event history. Provide documented login credentials. Include enough repeatable data to expose inefficient database access.

Implement the minimal domain:
- Organizations, users/memberships, projects.
- Environments with an explicit lifecycle.
- Provisioning operations and audit/events.
- A fake provider resource identifier.

Authentication, seed/reset infrastructure, migrations, and basic navigation must work. The learner should not need to invent the product contract.

Publish an API contract with request/response examples, permissions, validation rules, status codes, and lifecycle behavior. Specify ambiguous edge cases before grading them. Keep most internals for the learner to discover by reading code.

## 3. Two-day schedule and seven main exercises

DAY 1 — 7 focused hours:
- Orientation and baseline investigation: 30 minutes.
- Exercise 1, API correctness and tenant isolation: 90 minutes.
- Exercise 2, PostgreSQL/ORM performance: 60 minutes.
- Exercise 3, reliable asynchronous provisioning: 120 minutes.
- Exercise 4, Linux/Docker operational incidents: 75 minutes.
- Review, engineering notes, and remaining small fixes: 45 minutes.

DAY 2 — 7 focused hours:
- Exercise 5, React/Next.js/TypeScript: 90 minutes.
- Exercise 6, Ansible automation: 45 minutes.
- Exercise 7, applied AI/RAG integration: 75 minutes.
- Independent timed mock assessment: 180 minutes.
- Review and improvement plan: 30 minutes.

Breaks are additional. State that these are target timeboxes, not guaranteed completion times.

### Exercise 1 — Repair API behavior and tenant isolation

Provide realistic defects across listing, detail access, and a write path. The learner must enforce organization membership and role rules, validate inputs, return consistent errors, and protect related-object lookups.

Make the acceptance criteria behavior-based. Cover unauthorized access, cross-organization IDs, invalid input, missing records, and valid requests. Include tests that ensure legitimate access still works.

Describe observable symptoms in the issue card. Do not identify the exact faulty line or provide the repair.

### Exercise 2 — Diagnose and improve database access

Provide a list/detail screen with an inefficient ORM access pattern and a reproducible seeded dataset. Supply a way to inspect query counts and query plans.

Require the learner to preserve filtering, ordering, pagination, and tenant boundaries while improving performance. Include an indexing or query-plan decision that they must explain.

Grade the absence of query growth with result count and correctness under realistic data. Avoid brittle wall-clock thresholds and a requirement to reproduce one exact implementation.

### Exercise 3 — Reliable asynchronous environment provisioning

Provide working Celery/provider scaffolding with deliberately flawed failure handling.

The provider simulator must offer deterministic scenarios:
- A successful request.
- A transient failure before resource creation.
- A resource created successfully followed by a timeout/lost response.
- Duplicate delivery of the same provisioning request.

The learner must implement the documented state transitions, bounded retries/timeouts, useful errors, and safe reconciliation of uncertain provider outcomes.

Specify the idempotency contract:
- The key is scoped to organization and operation.
- Replaying the same request returns the same logical operation.
- Reusing the key with a different request returns a documented conflict.
- Parallel duplicate API calls must not create duplicate logical operations.
- Redelivery/retry of a task must not create duplicate provider resources.

Give the provider a documented idempotency/reconciliation API so this is solvable. Do not pretend that a database transaction alone guarantees exactly-once remote effects.

Verify concurrency using real PostgreSQL and meaningful parallel execution. Verify at least one end-to-end path through an actual worker; eager-only Celery tests are insufficient. Keep all failure scenarios repeatable and bounded.

### Exercise 4 — Linux/Docker incident investigation

Provide two small, independently activated incidents, such as:
- An API request returning 502 due to a service/proxy configuration problem.
- Accepted background jobs that are not being processed.

The normal startup must be healthy; incidents begin only when I activate their scenario.

Supply symptoms, expected service behavior, and access to logs. Let me use curl, process/port inspection, Docker logs/exec, and service configuration to find the cause. Include concise systemd/journalctl reference material and sample logs where host systemd is unavailable.

Require a durable configuration fix and a short incident note: evidence, root cause, repair, and verification. Do not require me to modify my host OS.

### Exercise 5 — React/Next.js/TypeScript behavior

Supply a usable but flawed environment dashboard.

Require me to fix realistic asynchronous UI behavior: loading/error/empty states, polling or refresh, stale responses, request cleanup, and truthful provisioning status. Include a small missing user-facing feature and typed API responses.

Provide deterministic tests for the important behavior. Include an end-to-end happy path where practical. Do not grade styling preferences, pixel perfection, or a specific component structure.

Ensure authorization remains server-side; a hidden button is not permission enforcement.

### Exercise 6 — Ansible automation

Supply a small incomplete playbook that configures a fixture environment inside a container: directories, a templated configuration, and appropriate file permissions.

Require repeatable execution and meaningful idempotence: a second unchanged run should report no unnecessary changes. Include a check that changed input updates the intended output.

Use localhost/container targets without SSH credentials, privileged host access, or real cloud provisioning. Give the learner the product requirement, not a completed playbook.

### Exercise 7 — Applied AI/RAG integration

Provide a small support assistant for the fictional environment-management product. Use a deterministic fake model/retriever by default; an optional real-provider adapter must not be required for training or grading.

Require me to repair:
- Organization-scoped retrieval.
- Structured model/tool output validation.
- Appropriate behavior for model timeouts and malformed responses.
- A small, explicit tool allowlist and ordinary application authorization.

Tool requests must go through the same permissions as normal API requests. Do not execute arbitrary shell commands produced by the model.

Include a compact evaluation dataset: a normal grounded answer, missing evidence, a cross-tenant request, malicious instructions inside retrieved content, malformed output, and a timeout. Grade observable grounding, isolation, validation, and fallback behavior rather than exact answer wording.

## 4. The learner experience

Create:
- START_HERE.md with exact startup commands and the first action.
- A DAY_1.md and DAY_2.md checklist with the timeboxes above.
- One issue card per exercise, with context, symptoms/request, acceptance criteria, estimated time, and how to run relevant checks.
- A concise architecture diagram and repository map, without locating the intentional bugs.
- A generic command/reference cheat sheet and a small number of official documentation links.
- A notes template for hypotheses, commands/evidence, decisions, tests, and remaining risks.

Provide a simple CLI or scripts for:
- doctor: check prerequisites and report actionable setup problems.
- up/down: start and stop the local lab.
- seed: create repeatable fictional data.
- check <exercise>: run relevant checks without repairing code.
- hint <exercise> <level>: reveal one explicitly requested hint.
- incident start/stop <scenario>: activate or remove a scoped incident.
- reset <exercise>: reset only the selected exercise after explicit confirmation/flag.

Document commands that actually exist. Keep learner work and notes safe during ordinary startup, reseeding, and incident changes. Explain reset scope before any destructive reset and offer a backup/snapshot.

Create three progressive hints per exercise: diagnostic direction, relevant concept, then a more specific approach. Do not print hints or solutions automatically. Keep solution code out of learner documentation.

At the end of construction, create an AGENTS.md establishing COACH MODE for future Codex sessions:
- Do not automatically fix intentional exercise defects.
- When I ask for a hint, give only the requested level.
- When I ask for checks/review, report evidence and feedback without changing my code.
- Do not reveal solutions unless I explicitly ask to see them.
- Fix genuine setup/harness failures when requested, distinguishing them from learner tasks.

## 5. Assessment and grading

Separate learner-facing smoke tests from the grader/instructor materials. Keep grader details and any reference repairs in a sibling instructor directory, outside the learner workspace, to avoid accidental spoilers. This is separation for self-study, not a tamper-proof security boundary.

Starter smoke checks must pass. Exercise checks should fail only for the intentionally unfinished behavior. Clearly distinguish EXPECTED training failures from infrastructure failures.

Provide meaningful behavior tests, including negative cases, tenant boundaries, retries, and concurrency where relevant. Do not grade by searching for keywords, comparing source code, or checking implementation details.

Publish a rubric and weights for each exercise. Report passed/failed criteria and evidence, not just a percentage. Include partial credit and prioritize working, maintainable solutions with clear tests.

Validate that the grader accepts a sensible correct implementation and rejects the seeded defects. You may temporarily repair exercises in an instructor-only validation copy, then restore the intended broken starter. Do not leave completed solutions in the learner checkout or expose them in your final response.

## 6. Independent three-hour mock

Create a separate, ready-to-start mock with its own clean snapshot/data. It must not depend on whether I completed the seven training exercises.

Limit it to three achievable tasks:
- One Django/API behavior change.
- One React asynchronous-state defect.
- One service/configuration incident.

Use the same technologies and skills practiced earlier, but different defects/requirements. Supply fair acceptance criteria when the mock starts. Avoid surprising new frameworks or an oversized project.

Provide exam start/status/submit commands. Record the actual start time; elapsed time continues if the terminal/browser closes. The timer is advisory: preserve my work at expiration. Starting again must not silently reset the clock or erase code.

Keep the exact mock issue cards and hints out of the normal onboarding walkthrough. Use clear file separation; do not build elaborate secrecy/encryption infrastructure. Do not reveal the mock solution.

Score the mock separately out of 100 using functional correctness, authorization, tests, diagnosis, and engineering explanation. After submission, produce a concise feedback report with the top three improvement priorities.

## 7. Build and verification requirements

Inspect the working directory first and create this lab separately from unrelated files. Choose sensible defaults and continue without clarification questions.

Build the entire runnable repository, migrations, seed data, fixtures, defects, frontend, provider simulator, exercises, checks, hints, incident controls, and mock. No placeholder-only core flows.

Verify what you build:
1. Clean startup and documented credentials.
2. Migrations, deterministic seed/reset, and passing starter smoke tests.
3. Expected exercise failures with no accidental unrelated failures.
4. Reference repairs passing meaningful grader checks.
5. A real Celery/provider round trip and the concurrency cases.
6. Ansible running twice with the expected idempotence.
7. Mock startup, isolation, timer persistence, and submission.

Use official documentation when necessary. If Docker or another essential capability is unavailable, report exactly what could not run and provide the next concrete command. Never claim a check passed without executing it.

Prefer a coherent, small codebase over a large collection of loosely connected demos. Stop after building and validating the training setup; leave the actual learner tasks for me.

Your final response should be brief and in English:
- What was built and its directory.
- Exact startup command, local URL, and demo credentials.
- Whether setup verification passed and which exercise failures are intentional.
- The first Day 1 task.
- Where to start the independent mock later.

Do not include solutions, spoiler diffs, or a long implementation walkthrough.
