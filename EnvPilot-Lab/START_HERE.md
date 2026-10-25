# EnvPilot Lab — Start Here

Mahmoud, this is an independent hands-on lab for a fictional product that manages temporary development environments.
The target is 14 focused hours over two days, including a three-hour mock assessment at the end. Breaks are additional.
These are target timeboxes, not guaranteed completion times.
The exercises contain intentional defects. Your job is to read the code, reproduce the problems, fix them, and explain your decisions.
This lab does not reproduce EasyEnv's assessment or claim knowledge of its interview questions.

## Setup

You need Docker Engine, Compose v2, and Python 3.10+ for the CLI only. The first build requires Internet access.
On Windows, run Docker Desktop in Linux containers mode and enable WSL2 integration for your Ubuntu distribution under Settings → Resources → WSL Integration.
Running from WSL2 is recommended. You can copy the two adjacent folders into `~/envpilot` for better filesystem performance.
Do not modify host services. The lab does not mount the Docker socket or use privileged containers.
Allocate approximately 4 CPUs and 6 GB RAM to Docker. The stack is designed for a laptop, and internal services are not exposed to the host.

Start from the root of this repository. From WSL2:

```bash
cd EnvPilot-Lab
python3 lab.py doctor
python3 lab.py up
python3 lab.py check smoke
```

From PowerShell:

```powershell
cd EnvPilot-Lab
python lab.py doctor
python lab.py up
python lab.py check smoke
```

Open http://localhost:8090. All accounts are fictional and use the password `LabPass123!`.

| Username | Membership |
|---|---|
| mahmoud | Nile Labs owner |
| developer | Nile Labs developer |
| viewer | Nile Labs viewer |
| nora | Delta Works owner |
| dual | developer in both organizations |
| outsider | no memberships |

The first `up` applies migrations and adds seed data. Running it again preserves your work, notes, and any passwords you have changed.
The initial seed creates 480 environments and 1,440 history events. Get IDs from `/api/me/` and `/api/projects/` rather than assuming fixed values.
`up` does not repair exercises and preserves active incidents. Stop any active incident before running the baseline smoke checks.

## Your first practical step — 30 minutes

Open [DAY_1.md](DAY_1.md) and copy the [notes template](notes/TEMPLATE.md) to `notes/day-1.md`.
Record the smoke check results, sketch the request path from Nginx to the database, try signing in, and view one environment.
Read the API contract before making changes. Then open [Exercise 1](issues/01-api.md).
Avoid opening the adjacent `EnvPilot-Instructor` folder during training. It contains the grader and reference repairs used to validate the exercises.
The checks invoke it automatically. This separation supports self-study; it is not a security boundary.

## Important rules

`python lab.py check smoke` must pass when the infrastructure is healthy.
Exercise checks, from `python lab.py check 1` through `python lab.py check 7`, are expected to fail on exercise-related assertions until you repair the relevant behavior.
Build, connection, import, and test collection failures are infrastructure failures, not learner tasks.
Read [VERIFICATION.md](VERIFICATION.md) to see exactly what was executed during construction.
Do not use SQLite results as evidence of PostgreSQL concurrency or treat eager task execution as an actual worker test.

## Everyday commands

```bash
python3 lab.py down                 # stop, keep data
python3 lab.py up                   # restart, keep code/data/notes
python3 lab.py seed                 # additive, preserve existing objects
python3 lab.py check 3              # PostgreSQL parallel API + actual worker/provider
python3 lab.py hint 3 1             # only the explicitly requested hint
python3 lab.py incident start proxy
python3 lab.py incident stop proxy
python3 lab.py incident start queue
python3 lab.py incident stop queue
python3 lab.py reset 2              # print exact scope, change nothing
python3 lab.py reset 2 --yes        # mandatory backup, then selected code only
python3 lab.py e2e                  # browser happy path; downloads browser image
```

Backend changes are available through a bind mount, but Gunicorn and Celery do not reload automatically:
run `docker compose restart api worker`. The frontend supports hot reload; dependency changes require a rebuild.
If an incident is active, use `lab.py` commands to recreate the service with the correct overlay.
Reset restores selected source files, not the database or migrations you have added. Files shared by multiple exercises may be affected, so read the reset scope first.
Backups are stored in `.lab/backups/`, and reports in `.lab/reports/`. To repeat a scenario, use a new pending environment and a new idempotency key instead of deleting volumes.

## Later: the independent mock

Only when you are ready, run `python3 lab.py exam start`. This prepares a separate workspace, Compose project, and database on port 8091.
Read [MOCK.md](MOCK.md) for timing and submission rules. The task details appear inside the exam workspace when you start it.
