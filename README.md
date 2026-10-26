# EnvPilot Lab

A local, two-day engineering lab for a fictional product that manages temporary development environments. The 14-hour schedule includes seven exercises and an independent three-hour mock assessment.

The repository is a running application with realistic demo data, deliberately incomplete features, reproducible defects, and issue cards with clear acceptance criteria. You investigate the code and behavior, implement repairs, run checks, and explain your engineering decisions.

## What is the product you are working on?

Imagine a team that needs a temporary development workspace for a project. A developer asks EnvPilot to create one, the request runs in the background, and the team checks its progress in a dashboard.

The lab simulates that workflow with a local fake provider. You can investigate requests, stored records, worker jobs, failures, and permissions without a cloud account. No real VM or public workspace URL is created.

Your training assignment is to make the application behave correctly according to the exercise cards. You edit code and configuration, run tests, and explain your decisions. Clicking through every environment card does not complete the lab.

## How the application works

The intended provisioning flow is:

1. A team has projects; each project contains environment records. An environment represents one temporary development workspace.
2. An Owner or Developer selects **Provision** on a pending environment. The dashboard sends an authenticated request through Nginx to the Django API.
3. The API records an operation and sends background work through Redis to Celery. An accepted request is not the same as completed provisioning.
4. A Celery worker calls the local fake provider, then records the outcome, resource reference, and events in PostgreSQL.
5. The dashboard reads the API to display the recorded result. **Refresh** requests newer data.

This describes the product's intended behavior. The starter deliberately contains defects, including cases where displayed state or request behavior is wrong. Use the exercise acceptance criteria and server evidence as the basis for your investigation.

| Term | Meaning in this lab |
|---|---|
| Organization | A fictional team, such as Team Alpha. Teams should be isolated from each other. |
| Project | A group of related environments belonging to one organization. |
| Environment / workspace | A database record representing a temporary development workspace. |
| Provider resource | A simulated resource reference associated with an environment, not a real cloud VM. |
| Operation | A provisioning request tracked separately from the environment's lifecycle. |
| Event | A recorded message about an environment's history. |
| Role | The selected account's permissions: Owner, Developer, or Viewer within a team. |

## Who this lab is for

The lab is designed for mid-level and senior backend or full-stack engineers preparing for practical engineering assessments, interviews, or broader ownership of production systems.

You should already be comfortable with Python, web APIs, SQL, JavaScript or TypeScript, React fundamentals, and basic Linux/Docker commands. Familiarity with Django is useful. The scaffolding lets you focus on investigation, implementation, and tradeoffs.

It is also useful for developers who want to connect API correctness, database access, asynchronous jobs, frontend state, and operational configuration within one coherent product.

## What the lab focuses on

The main priorities are **backend correctness, asynchronous reliability, and evidence-based debugging**. Frontend behavior, automation, and applied AI extend the same product across the stack.

| Exercise | Focus | Target time |
|---|---|---:|
| 1 | API validation, tenant isolation, related-object access, and role permissions | 90 min |
| 2 | PostgreSQL/ORM query growth, pagination, and query-plan decisions | 60 min |
| 3 | Celery provisioning, idempotency, bounded retries, duplicate delivery, and uncertain remote outcomes | 120 min |
| 4 | Linux/Docker investigation, logs, service configuration, and durable repairs | 75 min |
| 5 | React/Next.js/TypeScript loading states, request races, cleanup, and truthful status | 90 min |
| 6 | Ansible configuration, file permissions, repeatable execution, and idempotence | 45 min |
| 7 | Organization-scoped retrieval, model-output validation, authorized tools, and safe AI fallbacks | 75 min |

Orientation, engineering notes, reviews, and the final mock complete the two-day schedule. See the [Day 1 checklist](EnvPilot-Lab/DAY_1.md) and [Day 2 checklist](EnvPilot-Lab/DAY_2.md). These are target timeboxes; breaks are additional.

## How you use it

1. Read the current issue card and its acceptance criteria.
2. Reproduce the behavior using the dashboard, API, logs, or command line.
3. Investigate the code and data, form a hypothesis, and implement your repair.
4. Run the relevant checks and add meaningful regression tests.
5. Write an engineering note explaining your evidence, decisions, tradeoffs, and remaining risks.

The dashboard is the product you investigate. Environment cards show sample application data; the lab guide explains your assignments. Implementation work happens in the repository and your editor.

Each card explains its reported status, labels the project and organization, shows the latest event, provider resource, and UTC timestamps, and suggests a next step for your role. Expand **Technical details** to find record IDs and the authenticated API endpoint for investigation.

### Understand the cards

The initial data contains 2 teams, 8 projects, 480 environments, and 1,440 events. There are many more environment cards than exercises; you do not need to process them all.

| Card title or technical value | What it means |
|---|---|
| **Sample development workspace 60** | Preloaded practice data. For example, `dev-4-060` means development workspace 60 in sample project 4 within its team. The project and organization labels identify its context. |
| **System check workspace** | A diagnostic record created by an automated lab check to verify provisioning. It is not an exercise you need to complete. The technical name starts with `check-`, followed by a random suffix to keep names unique. |
| A custom workspace name | A record with a name outside those sample/diagnostic conventions. Its name is displayed as recorded. |
| `seed-…` resource ID | A reference included with the preloaded practice data; it does not prove a live resource exists. |
| Other provider resource IDs, such as `vm-…` | References used by the local fake provider, not real cloud addresses. |

Cards use readable titles and resource descriptions. Expand **Technical details** for the exact generated environment name, provider resource ID, record IDs, and authenticated API endpoint. Use those exact values when investigating API requests and logs. Friendly labels do not rename the stored records.

The lifecycle values are `pending` (waiting for a provisioning request), `provisioning` (background work in progress), `ready` (the API reports readiness), and `failed` (the API reports a failure). Seeded history and starter defects mean that the label alone is not proof of a successful live operation.

## Local stack

Django and Django REST Framework provide the API, PostgreSQL stores application data, Redis and a real Celery worker process jobs, and Next.js/React/TypeScript provide the dashboard behind Nginx. A deterministic HTTP provider simulates remote resource creation. Ansible runs in an isolated fixture container, and the AI exercise uses a deterministic local model/retriever.

No paid account, cloud subscription, API key, real VM, or GPU is required. All accounts, organizations, and product data are fictional.

## Repository layout

- `EnvPilot-Lab/`: the learner repository, exercises, notes, and startup guide.
- `EnvPilot-Instructor/`: behavioral graders, harness tests, and the independent mock template. Keep this folder adjacent to the learner directory; avoid browsing instructor materials during training.

Keep the learner and instructor directories adjacent so the CLI can run checks and prepare the mock.

## Getting started

Start with [EnvPilot-Lab/START_HERE.md](EnvPilot-Lab/START_HERE.md).

In the running app, use **Start Day 1** or open http://localhost:8090/guide for the exercise cards and a dashboard glossary. The dashboard opens as **Owner** with no login form. Use the **Role** dropdown to switch demo accounts; the browser remembers your role and organization. Demo organizations are Team Alpha and Team Beta. API exercises can still use token login (`owner` / `LabPass123!`).

Clone this repository using GitHub's **Code** button, then run the lab from its checkout:

Start in the checkout root: the directory containing this README and both supplied directories. The following `cd` enters the learner directory inside it.

```powershell
cd EnvPilot-Lab
python lab.py doctor
python lab.py up
python lab.py check smoke
```

On Linux/WSL2, use `python3` instead of `python` if needed. Docker Engine with Compose v2 is required. Everything runs locally; no paid services or cloud credentials are required.

Use Python 3.10+ for the CLI. On Windows, use Docker Desktop with Linux containers and WSL2 integration. The first build requires Internet access.

Allow approximately 4 CPUs and 6 GB RAM for Docker. Python is needed on the host for the CLI; application dependencies run inside Docker.

- `doctor` checks the prerequisites and whether Docker Engine responds.
- `up` builds and starts the services, applies migrations, and adds initial sample data. Running it again preserves existing records, passwords, and learner work.
- `check smoke` verifies the training infrastructure, including the API, frontend smoke tests, and an actual worker/provider round trip.

When smoke passes, open the dashboard and select **Start Day 1**. If Docker is still starting or smoke reports connection/build/import failures, resolve the setup problem before beginning an exercise.

## Your first 30 minutes

Do this baseline investigation before attempting repairs:

1. **Minutes 0–5: read the brief.** Open [Day 1](EnvPilot-Lab/DAY_1.md), the [architecture](EnvPilot-Lab/docs/ARCHITECTURE.md), and the [API contract](EnvPilot-Lab/docs/API_CONTRACT.md). In the browser, use **Start Day 1**.
2. **Minutes 5–10: prepare your notes.** Copy `EnvPilot-Lab/notes/TEMPLATE.md` to `EnvPilot-Lab/notes/day-1.md`. Record the smoke result and what you expect provisioning to do.
3. **Minutes 10–20: observe one record.** Choose a sample development workspace. Read its project, status, latest event, and technical details. Switch to Viewer and observe the controls, then return to Owner. Use the API contract to inspect a request and compare its response with the card. You do not need to process all 480 environments.
4. **Minutes 20–30: trace the system.** Find the request in the API logs and identify the frontend, API, database, queue, worker, and provider involved. Sketch their relationship and write down what you observed.

From the `EnvPilot-Lab/` directory, inspect recent service logs with:

```powershell
docker compose logs --tail=80 api worker provider
```

After the baseline, open [Exercise 1 — API behavior and tenant isolation](EnvPilot-Lab/issues/01-api.md). Read its acceptance criteria, then run its baseline check:

```powershell
python lab.py check 1
```

An exercise-related failure on the starter is expected. Record the failure, write a hypothesis in your notes, and investigate the relevant source before editing it. Repeat the workflow in **How you use it** for each exercise, following the Day 1 and Day 2 checklists.

## Where you work

The checkout contains two adjacent directories. **Make your application changes in `EnvPilot-Lab/`.** The CLI uses `EnvPilot-Instructor/` to run behavioral checks and prepare the independent mock. Avoid browsing the instructor implementation during self-study.

All paths in the following tree are relative to the checkout root. The tree shows the main entry points rather than every file:

```text
README.md                         Overview and training route
EnvPilot-Lab/
  lab.py                          Host-side lab commands
  compose.yaml                    Services, networks, volumes, and local port
  START_HERE.md                   Setup and operating instructions
  DAY_1.md / DAY_2.md              Training schedules
  issues/                         Exercise briefs and acceptance criteria
  docs/                           API contract, architecture, command reference
  hints/                          Optional hints; request only the level you need
  notes/                          Your observations and engineering decisions
  backend/
    manage.py                     Django management-command entry point
    config/                       Django settings, URL routing, Celery setup
    lab/                          Product code: API, data, permissions, jobs, AI
      migrations/                 Versioned database schema/data changes
      management/commands/        Sample data and query profiling commands
    tests/                        Backend smoke and demo setup regression tests
  frontend/
    app/                          Next.js pages, layout, and styles
      guide/                      Browser-based learner documentation
    components/                   Dashboard, environment cards, orientation
    lib/                          Typed API client and guide navigation
    tests/                        Component and UI behavior tests
    e2e/                          Full-stack browser scenarios
  provider/server.py              Local HTTP resource simulator
  infra/                          Nginx configuration and incident overlays
  ansible/                        Playbook, template, and fixture verification
  .lab/                           Reset snapshot, local reports, backups/state
EnvPilot-Instructor/               External checks and independent mock template
```

### Backend: which file does what?

The backend has a **configuration package** (`config/`) and a **product package** (`lab/`). The product package name is a Django app name; it is not a second copy of the training workspace.

| File inside `EnvPilot-Lab/backend/` | Responsibility | Open it when you need to understand… |
|---|---|---|
| [config/urls.py](EnvPilot-Lab/backend/config/urls.py) | Maps HTTP paths to API view classes. | Which code handles `/api/environments/` or a provisioning request. |
| [config/settings.py](EnvPilot-Lab/backend/config/settings.py) | Database, REST Framework, authentication, and Celery configuration. | How the application is configured and connected to other services. |
| [config/celery.py](EnvPilot-Lab/backend/config/celery.py) | Creates the Celery application and discovers tasks. | How the worker is connected to Django's configuration. |
| [lab/views.py](EnvPilot-Lab/backend/lab/views.py) | HTTP request handlers: `Me`, `Projects`, `Environments`, `EnvironmentDetail`, `Provision`, `OperationDetail`, and `Assistant`. | How an endpoint reads parameters, calls product code, and returns a response. |
| [lab/serializers.py](EnvPilot-Lab/backend/lab/serializers.py) | Input serializers such as `EnvironmentInput` and `ProvisionInput`, plus output serializers such as `EnvironmentSerializer`. | How request data is validated and model data becomes JSON. |
| [lab/permissions.py](EnvPilot-Lab/backend/lab/permissions.py) | Shared organization-access helper, `organization_for(...)`. | How membership and read/write role rules are represented. |
| [lab/queries.py](EnvPilot-Lab/backend/lab/queries.py) | Builds the environment queryset used by the list endpoint. | Which records are selected, their ordering, and database-query behavior. |
| [lab/models.py](EnvPilot-Lab/backend/lab/models.py) | Database models: `Organization`, `Membership`, `Project`, `Environment`, `Operation`, `Event`, and `SupportDocument`. | What is stored and how records relate to each other. |
| [lab/services.py](EnvPilot-Lab/backend/lab/services.py) | Product workflow entry point `start_provision(...)`: operation handling and task dispatch. | What happens when the API accepts a provisioning request. |
| [lab/tasks.py](EnvPilot-Lab/backend/lab/tasks.py) | Celery task `provision(...)`, provider HTTP calls, and recorded outcomes. | What runs in the background after the HTTP request has returned. |
| [lab/assistant.py](EnvPilot-Lab/backend/lab/assistant.py) | Deterministic retrieval, fake-model, and assistant workflow. | The applied AI exercise and its data/tool boundaries. |
| [lab/demo.py](EnvPilot-Lab/backend/lab/demo.py) | Fixed demo-account selection for the Role dropdown. | How the local dashboard opens without a login form. |
| [lab/errors.py](EnvPilot-Lab/backend/lab/errors.py) | REST exception formatting. | How API failures become the documented JSON error envelope. |
| [lab/management/commands/seed.py](EnvPilot-Lab/backend/lab/management/commands/seed.py) | Additive creation of initial teams, accounts, projects, environments, and history. | Where the sample data and generated names come from. |
| [lab/management/commands/profile_queries.py](EnvPilot-Lab/backend/lab/management/commands/profile_queries.py) | Query measurement command. | How to collect database evidence for the performance exercise. |

`models.py` defines database structure; `serializers.py` deals with input/output representation; `views.py` handles HTTP; `services.py` coordinates a product action; `tasks.py` runs background work. These responsibilities are related, but they are not interchangeable.

The table describes each file's role, not a guarantee that its starter implementation is correct. Use the API contract and issue criteria to judge behavior. Database migrations record schema/data changes; they are not the usual entry point for tracing an HTTP request.

### Frontend: which file controls the screen?

| File inside `EnvPilot-Lab/frontend/` | Responsibility |
|---|---|
| [app/page.tsx](EnvPilot-Lab/frontend/app/page.tsx) | Dashboard page entry point: demo role selection, session setup, organization choice, and rendering the active dashboard. |
| [app/layout.tsx](EnvPilot-Lab/frontend/app/layout.tsx) | Shared page layout and global stylesheet loading. |
| [app/style.css](EnvPilot-Lab/frontend/app/style.css) | Colors, spacing, responsive layout, and component styles. |
| [components/Dashboard.tsx](EnvPilot-Lab/frontend/components/Dashboard.tsx) | Loads environment rows, tracks status filtering and feedback, and handles the Provision action. |
| [components/EnvironmentCard.tsx](EnvPilot-Lab/frontend/components/EnvironmentCard.tsx) | Displays one record: readable name, purpose, metadata, next-step guidance, and technical details. Its callback delegates provisioning to `Dashboard.tsx`. |
| [components/LabOrientation.tsx](EnvPilot-Lab/frontend/components/LabOrientation.tsx) | First-task instructions, glossary, and links to the learner guide. |
| [lib/api.ts](EnvPilot-Lab/frontend/lib/api.ts) | Shared TypeScript response types and `api<T>(...)`, the authenticated JSON fetch helper. |
| [lib/guides.ts](EnvPilot-Lab/frontend/lib/guides.ts) | Allowed learner documents, their guide URLs, and link rewriting. |
| `app/guide/page.tsx` | Index of the browser-based lab guide. |
| `app/guide/[slug]/page.tsx` | Displays the allowed Markdown document selected by the URL. `[slug]` is a dynamic Next.js route segment, such as `day-1` or `exercise-1`. |

For a confusing label or layout, inspect the card component and stylesheet. For a request or state-management problem, follow the dashboard and API helper. The browser's hidden controls do not determine whether an API operation is authorized; the server is responsible for that decision.

### Follow one request through the files

For an environment list request, use this reading order:

```text
frontend/components/Dashboard.tsx       load()
  -> frontend/lib/api.ts               authenticated GET /api/environments/
  -> infra/nginx.conf                  forwards /api/ to the API service
  -> backend/config/urls.py            selects Environments
  -> backend/lab/views.py              Environments.get()
  -> backend/lab/queries.py            environment_rows(...)
  -> backend/lab/models.py             database records via Django ORM
  -> backend/lab/serializers.py        EnvironmentSerializer -> JSON response
  -> Dashboard.tsx                     receives the rows
  -> EnvironmentCard.tsx               renders each record
```

`GET` reads records; it does not ask the provider to create a resource. For provisioning, the path branches into a background job:

```text
Dashboard.tsx: provision(row)
  -> POST /api/environments/{id}/provision/
  -> urls.py -> views.py: Provision.post()
  -> serializers.py / services.py: start_provision(...)
  -> recorded Operation + task message through Redis
  -> Celery worker -> tasks.py: provision(operation_id)
  -> provider/server.py over HTTP
  -> recorded outcome in PostgreSQL
  -> a later API read supplies the dashboard with newer state
```

The API and worker are separate processes, even though they use the same backend source directory. `services.py` coordinates the action; `tasks.py` performs the background provider call. The maps show where to read the code; expected lifecycle, errors, and reliability rules are defined by the API contract.

### Infrastructure, checks, and generated files

| Path inside `EnvPilot-Lab/` | Role |
|---|---|
| [compose.yaml](EnvPilot-Lab/compose.yaml) | Defines the `api`, `web`, `db`, `redis`, `worker`, `provider`, and `proxy` services, their connections, mounts, and ports; also defines the optional Ansible/browser tools. |
| [infra/nginx.conf](EnvPilot-Lab/infra/nginx.conf) | Sends browser page requests to Next.js and `/api/` requests to Django. |
| `infra/incidents/` | Explicitly activated proxy/queue incident overlays. Reading these files does not activate an incident. |
| [provider/server.py](EnvPilot-Lab/provider/server.py) | Standalone local HTTP simulator with its own resource ledger and deterministic scenarios. Read it to understand the external system's behavior. |
| `ansible/playbook.yml`, `ansible/templates/agent.conf.j2` | Automation exercise and the configuration it renders in an isolated fixture. |
| `ansible/verify.py` | Behavioral verification for the automation fixture. |
| `backend/tests/` | Backend smoke and demo identity/role regression checks; this is not the complete exercise grading suite. |
| `frontend/tests/smoke.test.tsx`, `frontend/tests/environment-card.test.tsx` | Demo navigation, role selection, and card presentation smoke checks. |
| `frontend/tests/dashboard.test.tsx` | Exercise 5 behavior checks; intentional starter failures are expected here. |
| `frontend/e2e/happy.spec.ts` | Browser scenarios involving demo role selection and observed provisioning results. |
| `lab.py` | Host CLI that orchestrates Docker, runs external checks, serves requested hints, and manages the mock/reset commands. |
| `.lab/starter.zip`, `.lab/starter-manifest.json` | Exercise reset baseline and file hashes. These are harness assets, not normal application edit targets. |
| `.lab/reports/`, `.lab/backups/` | Local generated check evidence and reset backups. |

`lab.py` is the host-side training CLI; `backend/manage.py` is Django's management entry point inside the backend environment. They serve different purposes. Use `python lab.py check <number>` (or `python3` in WSL) for exercise checks; it invokes the adjacent instructor grader automatically.

Generated directories such as `node_modules/`, `.next/`, `__pycache__/`, and local reports are not the application's source code. Do not start an investigation by editing generated build/dependency files.

### Where to start reading for each exercise

These are entry points for investigation, not repair instructions or a restriction on which learner files may need changes. Read the issue card and API contract first.

| Exercise | Start with these learner files |
|---|---|
| 1 — API correctness and tenant isolation | `backend/config/urls.py`, `backend/lab/views.py`, `backend/lab/serializers.py`, `backend/lab/permissions.py`, and the related models. |
| 2 — Database performance | `backend/lab/queries.py`, `backend/lab/serializers.py`, `backend/lab/models.py`, and `backend/lab/management/commands/profile_queries.py`. |
| 3 — Provisioning reliability | `backend/lab/services.py`, `backend/lab/tasks.py`, `backend/lab/models.py`; read `provider/server.py` to understand the simulator contract. |
| 4 — Incidents | `compose.yaml`, `infra/nginx.conf`, `infra/incidents/`, and the logs of the affected service. |
| 5 — Dashboard behavior | `frontend/components/Dashboard.tsx`, `frontend/lib/api.ts`, and `frontend/tests/dashboard.test.tsx`. |
| 6 — Ansible | `ansible/playbook.yml`, `ansible/templates/agent.conf.j2`, and `ansible/verify.py`. |
| 7 — Applied AI | `backend/lab/assistant.py`, the `Assistant` view, and `SupportDocument`/related models in `backend/lab/models.py`. |

For Exercise 1, pick one failing request and locate its path in `config/urls.py`. Then read the selected view method, the input/output serializers it uses, the related models, and the access helper. Write down what each part currently does and compare that with the contract before changing code. You do not need to read the whole repository or work on the frontend to begin investigating that request.

## Checks and assessment

Starter smoke checks should pass on healthy infrastructure. Exercise checks intentionally fail until you repair the corresponding behavior. Build, connection, import, and test-collection failures are infrastructure problems and should be investigated separately.

```powershell
python lab.py check 1
python lab.py hint 1 1
python lab.py exam status
```

Hints are opt-in and have three progressive levels per exercise. Checks report behavioral evidence and do not install solutions. Read the [rubric](EnvPilot-Lab/RUBRIC.md) for partial credit and engineering-explanation criteria.

`hint 1 1` requests only level 1 for Exercise 1. A passing smoke check does not mean you have completed an exercise: rerun that exercise's check, compare the outcome with every acceptance criterion, and write an engineering note explaining your evidence, decisions, tradeoffs, and remaining risks.

To stop and resume from `EnvPilot-Lab/`:

```powershell
python lab.py down          # stop services and keep data
python lab.py up            # resume without resetting learner work
```

Instructor reference solutions, construction validation copies, personal notes, dependency directories, and local exam submissions are excluded from the public repository. The intentionally incomplete learner exercises remain intact. This is a self-study lab and does not claim to reproduce any employer's assessment.

The independent mock will be created as `EnvPilot-Mock/` beside the two supplied directories when you explicitly run `python lab.py exam start`. Its clock is not started by cloning or normal lab startup.

The mock has its own database and Compose project on port 8091 and does not depend on your training repairs. Its advisory timer persists across terminal/browser closure, and expiration preserves your work. Read the [mock rules](EnvPilot-Lab/MOCK.md) before starting.

See [EnvPilot-Lab/VERIFICATION.md](EnvPilot-Lab/VERIFICATION.md) for the latest runtime checks and the original construction record.
