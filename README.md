# EnvPilot Lab

A local, two-day engineering lab for a fictional product that manages temporary development environments. The 14-hour schedule includes seven exercises and an independent three-hour mock assessment.

The repository is a running application with realistic demo data, deliberately incomplete features, reproducible defects, and issue cards with clear acceptance criteria. You investigate the code and behavior, implement repairs, run checks, and explain your engineering decisions.

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

## Local stack

Django and Django REST Framework provide the API, PostgreSQL stores application data, Redis and a real Celery worker process jobs, and Next.js/React/TypeScript provide the dashboard behind Nginx. A deterministic HTTP provider simulates remote resource creation. Ansible runs in an isolated fixture container, and the AI exercise uses a deterministic local model/retriever.

No paid account, cloud subscription, API key, real VM, or GPU is required. All accounts, organizations, and product data are fictional.

## Repository layout

- `EnvPilot-Lab/`: the learner repository, exercises, notes, and startup guide.
- `EnvPilot-Instructor/`: behavioral graders, harness tests, and the independent mock template. Keep this folder adjacent to the learner directory; avoid browsing instructor materials during training.
- `EnvPilot_Two_Day_Lab_Codex_Prompt.md`: the original lab requirements.

Keep the learner and instructor directories adjacent so the CLI can run checks and prepare the mock.

## Getting started

Start with [EnvPilot-Lab/START_HERE.md](EnvPilot-Lab/START_HERE.md).

In the running app, use **Start Day 1** or open http://localhost:8090/guide for the exercise cards and a dashboard glossary. Default login: `owner` / `LabPass123!`. Demo organizations are Team Alpha and Team Beta.

Clone this repository using GitHub's **Code** button, then run the lab from its checkout:

```powershell
cd EnvPilot-Lab
python lab.py doctor
python lab.py up
python lab.py check smoke
```

On Linux/WSL2, use `python3` instead of `python` if needed. Docker Engine with Compose v2 is required. Everything runs locally; no paid services or cloud credentials are required.

Use Python 3.10+ for the CLI. On Windows, use Docker Desktop with Linux containers and WSL2 integration. The first build requires Internet access.

## Checks and assessment

Starter smoke checks should pass on healthy infrastructure. Exercise checks intentionally fail until you repair the corresponding behavior. Build, connection, import, and test-collection failures are infrastructure problems and should be investigated separately.

```powershell
python lab.py check 1
python lab.py hint 1 1
python lab.py exam status
```

Hints are opt-in and have three progressive levels per exercise. Checks report behavioral evidence and do not install solutions. Read the [rubric](EnvPilot-Lab/RUBRIC.md) for partial credit and engineering-explanation criteria.

Instructor reference solutions, construction validation copies, personal notes, dependency directories, and local exam submissions are excluded from the public repository. The intentionally incomplete learner exercises remain intact. This is a self-study lab and does not claim to reproduce any employer's assessment.

The independent mock will be created as `EnvPilot-Mock/` beside the two supplied directories when you explicitly run `python lab.py exam start`. Its clock is not started by cloning or normal lab startup.

The mock has its own database and Compose project on port 8091 and does not depend on your training repairs. Its advisory timer persists across terminal/browser closure, and expiration preserves your work. Read the [mock rules](EnvPilot-Lab/MOCK.md) before starting.

See [EnvPilot-Lab/VERIFICATION.md](EnvPilot-Lab/VERIFICATION.md) for the latest runtime checks and the original construction record.
