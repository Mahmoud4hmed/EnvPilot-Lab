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

| Path inside `EnvPilot-Lab/` | Purpose |
|---|---|
| `backend/` | Django API, models, queries, provisioning logic, Celery tasks, and backend tests |
| `frontend/` | Next.js/React dashboard, guides, and frontend tests |
| `provider/` | Deterministic local fake provider |
| `infra/` | Nginx and incident configuration |
| `ansible/` | Automation exercise in an isolated fixture container |
| `issues/` | The seven training assignments and acceptance criteria |
| `docs/` | Architecture, API contract, and supporting documentation |
| `notes/` | Your engineering notes and their template |
| `lab.py` | Startup, checks, optional hints, and mock commands |

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
