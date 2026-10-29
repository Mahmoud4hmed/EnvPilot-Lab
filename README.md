# EnvPilot Lab

EnvPilot is a fictional service that helps a development team request temporary workspaces and track their setup. For example, a developer requests `payment-test` to try a checkout change; resources are prepared in the background and their status appears on the dashboard. The goal is less manual setup and clear team access.

**This lab simulates that product:** resources are fake and no application is deployed. Repair its management code through **7 exercises + a 3-hour independent mock, within a suggested 14-hour schedule**. Breaks are additional.

Built for **mid-level and senior backend/full-stack engineers** familiar with Python, HTTP/SQL, JavaScript/TypeScript, React, and basic Docker/Linux. Django experience helps. Practice backend correctness, asynchronous reliability, debugging, frontend state, operations, Ansible, and applied AI by repairing intentional defects and explaining your decisions.

## Start here

You need Git, Python 3.10+, and Docker Engine with Compose v2. On Windows, use Docker Desktop with Linux containers and WSL2 integration. Allow about 4 CPUs / 6 GB RAM; the first build needs Internet access. No paid account, cloud credentials, real VM, or GPU is required.

Clone the repository and keep `EnvPilot-Lab/` beside `EnvPilot-Instructor/`. From the checkout root (the directory containing this README):

```powershell
cd EnvPilot-Lab
python lab.py doctor
python lab.py up
python lab.py check smoke
```

Use `python3` in Linux/WSL if needed. `doctor` checks prerequisites; `up` builds services, applies migrations, and adds sample data without resetting existing work/passwords; `check smoke` checks the API, frontend, and actual worker/provider round trip. Application dependencies run inside Docker.

Open the [dashboard](http://localhost:8090) or [lab guide](http://localhost:8090/guide). It opens as **Owner** without a login form. **Role** switches fixed demo accounts; **Organization** selects a team. Both choices are remembered. Owner/Developer can provision; Viewer is read-only. The API remains responsible for authorization. API exercises can use token login with `owner` / `LabPass123!` unless changed.

Detailed setup: [START_HERE.md](EnvPilot-Lab/START_HERE.md). Resolve Docker/build/import/connection failures before training.

## What the application does

A team (**Organization**) owns **Projects**, each containing workspace records (**Environments**). An **Operation** tracks a provisioning request separately from the environment lifecycle; **Events** record its history.

An **Environment** in a real product is a separate, temporary workspace for running and testing a project version with its own settings and test data. Its benefit is a repeatable setup where developers can try changes without affecting the live application or each other's work.

```text
Browser → Nginx → Next.js dashboard / Django REST API → PostgreSQL
Provision → API operation → Redis → Celery worker → fake HTTP provider
          → recorded outcome → later API read / Refresh
```

The API and worker are separate processes sharing backend source; the provider has its own resource ledger. An accepted request is not completed provisioning. The [API contract](EnvPilot-Lab/docs/API_CONTRACT.md) defines intended behavior; the starter deliberately violates some requirements. Investigate API responses and logs rather than trusting a displayed status alone. The AI workflow uses a deterministic local model/retriever; Ansible runs in an isolated fixture container.

**Here, each card is a simulated Environment record: an item with a name, status, project, and team.** You use these records to practice permissions, API requests, and background state changes. They do not run real applications or represent separate Docker containers; the containers run the lab itself. Initial data: 2 teams, 8 projects, 480 environments, and 1,440 events. Cards are application data, not exercise assignments; you do not need to process them all.

| Card / technical value | Meaning |
|---|---|
| **Sample development workspace 60** / `dev-4-060` | Preloaded workspace 60 in sample project 4 within its team. |
| **System check workspace** / `check-…` | Automated diagnostic record; a random suffix prevents duplicate names. |
| Custom name | Displayed as recorded outside those naming conventions. |
| `seed-…` / `vm-…` | Preloaded sample reference / simulated provider reference, not real cloud addresses. |

Cards show purpose, reported status, latest event, UTC timestamps, resource type, and a next step for your role. **Technical details** retains exact generated names, provider IDs, record IDs, and the authenticated API endpoint. Friendly labels do not rename stored records; no public workspace URL is created.

Lifecycle: `pending` (awaiting a request) → `provisioning` (background work) → `ready` or `failed` (reported outcome). Seed history and starter defects mean a label alone does not prove a live operation succeeded.

## Start training

Spend the first 30 minutes on one baseline investigation:

Use [the exercise workflow](EnvPilot-Lab/docs/EXERCISE_WORKFLOW.md) for copyable API setup commands, interpreting failures, and recording evidence. Each exercise includes its own reproduction steps and expected outcomes.

1. Read [Day 1](EnvPilot-Lab/DAY_1.md), the [architecture](EnvPilot-Lab/docs/ARCHITECTURE.md), and [API contract](EnvPilot-Lab/docs/API_CONTRACT.md), or select **Start Day 1** in the dashboard.
2. Copy `notes/TEMPLATE.md` to `notes/day-1.md` inside `EnvPilot-Lab/`; record your smoke result and expected behavior.
3. Inspect one sample workspace and its technical details. Switch to Viewer and back to Owner; compare an API response with the card.
4. Trace that request in the API logs, sketch the services involved, and record your observations.

Then read [Exercise 1](EnvPilot-Lab/issues/01-api.md). From `EnvPilot-Lab/`:

```powershell
docker compose logs --tail=80 api worker provider
python lab.py check 1
```

**Smoke should pass; exercise checks may fail until repaired.** For each exercise: read acceptance criteria → reproduce one failure → form a hypothesis → inspect/edit learner code → rerun its check and add regression evidence → write decisions, tradeoffs, and remaining risks. A passing smoke check alone does not complete an exercise.

| Day | Exercise / focus | Target |
|---|---|---:|
| 1 | [1 — API](EnvPilot-Lab/issues/01-api.md): validation, tenant isolation, related-object access, roles | 90 min |
| 1 | [2 — Database](EnvPilot-Lab/issues/02-database.md): ORM query growth, pagination, query plans | 60 min |
| 1 | [3 — Provisioning](EnvPilot-Lab/issues/03-provisioning.md): idempotency, bounded retries, duplicates, uncertain outcomes | 120 min |
| 1 | [4 — Incidents](EnvPilot-Lab/issues/04-incidents.md): logs, Docker/Linux configuration, durable repairs | 75 min |
| 2 | [5 — Frontend](EnvPilot-Lab/issues/05-frontend.md): loading states, request races, cleanup, truthful status | 90 min |
| 2 | [6 — Ansible](EnvPilot-Lab/issues/06-ansible.md): configuration, permissions, repeatability | 45 min |
| 2 | [7 — Applied AI](EnvPilot-Lab/issues/07-assistant.md): scoped retrieval, output validation, authorized tools, fallbacks | 75 min |

Orientation, notes, reviews, and the final mock complete the schedule. Follow [Day 1](EnvPilot-Lab/DAY_1.md), [Day 2](EnvPilot-Lab/DAY_2.md), and the [rubric](EnvPilot-Lab/RUBRIC.md); timeboxes are advisory. This is independent self-study, not a reproduction of an employer's assessment.

## Where you work

Edit **`EnvPilot-Lab/`**. The adjacent **`EnvPilot-Instructor/`** provides external graders and the independent mock template; the CLI invokes it automatically. Avoid browsing instructor implementations during self-study. Reference solutions, construction-only validation copies, personal notes, and exam submissions are excluded from the public repository.

Paths below are inside `EnvPilot-Lab/`. [Full file-by-file map and exercise reading order →](EnvPilot-Lab/docs/CODE_MAP.md)

| Area | Main files and responsibilities |
|---|---|
| `backend/config/` | `urls.py`: path → view; `settings.py`: Django/DB/auth/broker settings; `celery.py`: worker setup. |
| `backend/lab/` — HTTP/data | `views.py`: request handlers; `serializers.py`: input validation / JSON output; `permissions.py`: organization access; `queries.py`: record selection; `models.py`: schema/relationships. |
| `backend/lab/` — workflows | `services.py`: coordinate provisioning; `tasks.py`: background provider calls/outcomes; `assistant.py`: AI/RAG; `demo.py`: Role selector; `errors.py`: API error format. |
| Backend support | `migrations/`: schema/data history; `management/commands/seed.py`: additive sample data; `profile_queries.py`: query measurements. |
| `frontend/app/` | `page.tsx`: roles/session/organization; `layout.tsx` + `style.css`: shared layout/styles; `guide/`: document index and dynamic `[slug]` pages. |
| `frontend/components/` | `Dashboard.tsx`: requests/filtering/provisioning; `EnvironmentCard.tsx`: one record; `LabOrientation.tsx`: first-task guidance. |
| `frontend/lib/` | `api.ts`: types/authenticated JSON fetch; `guides.ts`: allowed documents and links. |
| Runtime/automation | `compose.yaml`: service wiring; `infra/nginx.conf`: page/API routing; `infra/incidents/`: opt-in incidents; `provider/server.py`: HTTP simulator; `ansible/`: playbook/template/verification. |
| Checks | `backend/tests/`: smoke/demo regressions; `frontend/tests/`: smoke/card checks and Exercise 5's `dashboard.test.tsx`; `frontend/e2e/`: browser scenarios. These are not the whole grading suite. |
| Training/support | `issues/`: assignments; `docs/`: contracts/reference; `hints/`: optional levels; `notes/`: your evidence; `.lab/`: reset snapshot, reports, backups/state. |

Read a list request as `Dashboard.load()` → `lib/api.ts` → Nginx → `config/urls.py` → `environments()` (GET) → queries/models → serializer → card. Provisioning instead reaches `provision()` → `start_provision()` → Redis → `tasks.provision()` → provider. For Exercise 1, locate one failing endpoint, read its view/serializers/models/access helper, and compare behavior with the contract before editing.

`lab.py` is the host training CLI; `backend/manage.py` is Django's management entry point. Edit source, not `node_modules/`, `.next/`, `__pycache__/`, reports, or the reset baseline. File responsibilities do not imply correct starter behavior.

## Everyday commands and assessment

Run from `EnvPilot-Lab/` (use `python3` in WSL when needed):

```powershell
python lab.py check 1       # replace 1 with the exercise number, or smoke
python lab.py hint 1 1      # Exercise 1, hint level 1; three optional levels
python lab.py down         # stop and keep data
python lab.py up           # resume, preserving learner work
python lab.py exam status  # inspect mock status without starting its clock
```

Checks assess behavior and do not install solutions. After practice, read the [mock rules](EnvPilot-Lab/MOCK.md), then run `python lab.py exam start` only when ready. This creates adjacent `EnvPilot-Mock/` with separate source, data, Compose project, and port 8091. Its advisory 3-hour timer survives terminal/browser closure; expiration preserves work. Normal lab startup does not start it.

Setup: [START_HERE](EnvPilot-Lab/START_HERE.md) · Check evidence and limits: [VERIFICATION](EnvPilot-Lab/VERIFICATION.md).
