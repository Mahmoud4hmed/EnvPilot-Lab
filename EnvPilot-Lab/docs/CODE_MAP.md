# Code and file map

[Back to the README](../../README.md#where-you-work)

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
| [config/urls.py](../backend/config/urls.py) | Maps HTTP paths to API view classes. | Which code handles `/api/environments/` or a provisioning request. |
| [config/settings.py](../backend/config/settings.py) | Database, REST Framework, authentication, and Celery configuration. | How the application is configured and connected to other services. |
| [config/celery.py](../backend/config/celery.py) | Creates the Celery application and discovers tasks. | How the worker is connected to Django's configuration. |
| [lab/views.py](../backend/lab/views.py) | HTTP request handlers: `Me`, `Projects`, `Environments`, `EnvironmentDetail`, `Provision`, `OperationDetail`, and `Assistant`. | How an endpoint reads parameters, calls product code, and returns a response. |
| [lab/serializers.py](../backend/lab/serializers.py) | Input serializers such as `EnvironmentInput` and `ProvisionInput`, plus output serializers such as `EnvironmentSerializer`. | How request data is validated and model data becomes JSON. |
| [lab/permissions.py](../backend/lab/permissions.py) | Shared organization-access helper, `organization_for(...)`. | How membership and read/write role rules are represented. |
| [lab/queries.py](../backend/lab/queries.py) | Builds the environment queryset used by the list endpoint. | Which records are selected, their ordering, and database-query behavior. |
| [lab/models.py](../backend/lab/models.py) | Database models: `Organization`, `Membership`, `Project`, `Environment`, `Operation`, `Event`, and `SupportDocument`. | What is stored and how records relate to each other. |
| [lab/services.py](../backend/lab/services.py) | Product workflow entry point `start_provision(...)`: operation handling and task dispatch. | What happens when the API accepts a provisioning request. |
| [lab/tasks.py](../backend/lab/tasks.py) | Celery task `provision(...)`, provider HTTP calls, and recorded outcomes. | What runs in the background after the HTTP request has returned. |
| [lab/assistant.py](../backend/lab/assistant.py) | Deterministic retrieval, fake-model, and assistant workflow. | The applied AI exercise and its data/tool boundaries. |
| [lab/demo.py](../backend/lab/demo.py) | Fixed demo-account selection for the Role dropdown. | How the local dashboard opens without a login form. |
| [lab/errors.py](../backend/lab/errors.py) | REST exception formatting. | How API failures become the documented JSON error envelope. |
| [lab/management/commands/seed.py](../backend/lab/management/commands/seed.py) | Additive creation of initial teams, accounts, projects, environments, and history. | Where the sample data and generated names come from. |
| [lab/management/commands/profile_queries.py](../backend/lab/management/commands/profile_queries.py) | Query measurement command. | How to collect database evidence for the performance exercise. |

`models.py` defines database structure; `serializers.py` deals with input/output representation; `views.py` handles HTTP; `services.py` coordinates a product action; `tasks.py` runs background work. These responsibilities are related, but they are not interchangeable.

The table describes each file's role, not a guarantee that its starter implementation is correct. Use the API contract and issue criteria to judge behavior. Database migrations record schema/data changes; they are not the usual entry point for tracing an HTTP request.

### Frontend: which file controls the screen?

| File inside `EnvPilot-Lab/frontend/` | Responsibility |
|---|---|
| [app/page.tsx](../frontend/app/page.tsx) | Dashboard page entry point: demo role selection, session setup, organization choice, and rendering the active dashboard. |
| [app/layout.tsx](../frontend/app/layout.tsx) | Shared page layout and global stylesheet loading. |
| [app/style.css](../frontend/app/style.css) | Colors, spacing, responsive layout, and component styles. |
| [components/Dashboard.tsx](../frontend/components/Dashboard.tsx) | Loads environment rows, tracks status filtering and feedback, and handles the Provision action. |
| [components/EnvironmentCard.tsx](../frontend/components/EnvironmentCard.tsx) | Displays one record: readable name, purpose, metadata, next-step guidance, and technical details. Its callback delegates provisioning to `Dashboard.tsx`. |
| [components/LabOrientation.tsx](../frontend/components/LabOrientation.tsx) | First-task instructions, glossary, and links to the learner guide. |
| [lib/api.ts](../frontend/lib/api.ts) | Shared TypeScript response types and `api<T>(...)`, the authenticated JSON fetch helper. |
| [lib/guides.ts](../frontend/lib/guides.ts) | Allowed learner documents, their guide URLs, and link rewriting. |
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
| [compose.yaml](../compose.yaml) | Defines the `api`, `web`, `db`, `redis`, `worker`, `provider`, and `proxy` services, their connections, mounts, and ports; also defines the optional Ansible/browser tools. |
| [infra/nginx.conf](../infra/nginx.conf) | Sends browser page requests to Next.js and `/api/` requests to Django. |
| `infra/incidents/` | Explicitly activated proxy/queue incident overlays. Reading these files does not activate an incident. |
| [provider/server.py](../provider/server.py) | Standalone local HTTP simulator with its own resource ledger and deterministic scenarios. Read it to understand the external system's behavior. |
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
