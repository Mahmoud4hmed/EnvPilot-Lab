# Exercise 4 — Investigate two Linux/Docker incidents

**Target time:** 75 minutes total. **Your role:** engineer responding to two independent local service incidents.

## The problem

The baseline stack is healthy, but the lab can deliberately activate two failures:

| Incident | User-visible symptom | Required recovery |
|---|---|---|
| `proxy` | Requests through `http://localhost:8090` return 502 for API/health routes, while the dashboard may still load. | Nginx successfully forwards health and API requests again. |
| `queue` | A provisioning request is accepted, but the operation remains queued instead of being processed. | A fresh accepted operation is processed by the real worker and reaches ready. |

Your task is to collect evidence, explain the root cause, and make a configuration repair that survives service recreation. Merely restarting a process, switching off the incident, or editing a running container without a persistent change is not sufficient.

## Before you start

Read [the shared workflow](../docs/EXERCISE_WORKFLOW.md) and [the command sheet](../docs/CHEATSHEET.md). Confirm baseline smoke passes before activating a failure. Run commands from `EnvPilot-Lab/`, use one incident at a time, and keep a timestamped note for each.

These are Docker-container incidents. Host systemd/SSH/network/security changes are not part of the assignment. The commands below are instructions for when you deliberately start this exercise; ordinary startup and `check 4` do not activate incidents for you.

## Scenario A — proxy

### Reproduce and investigate

Activate only the proxy incident:

```bash
python3 lab.py incident start proxy
curl -i http://localhost:8090/health/
docker compose ps
docker compose logs --tail=100 proxy api
docker compose exec proxy nginx -T
```

Record the public response, service health, and relevant logs/configuration. Compare the public route with the API service's own availability; do not assume that a loading frontend proves the API route is healthy.

Inspect `compose.yaml`, `infra/nginx.conf`, and `infra/incidents/` to understand how the active configuration is assembled. For the effective proxy overlay configuration, use:

```bash
docker compose -f compose.yaml -f infra/incidents/proxy.yaml config
```

### Repair and verify

Make a durable learner configuration repair, then check while the scenario is still active:

```bash
python3 lab.py check 4
```

The checker recreates the affected service before verifying recovery. Save the result and repeat a public health/API request. Only after recording evidence, stop the scenario:

```bash
python3 lab.py incident stop proxy
```

## Scenario B — queue

### Reproduce and investigate

After the proxy scenario has been stopped, activate the queue incident:

```bash
python3 lab.py incident start queue
docker compose ps
docker compose logs --tail=100 api worker redis
docker compose exec worker celery -A config inspect active_queues
docker compose exec worker celery -A config inspect active
docker compose exec redis redis-cli LLEN provision
```

Using the shared API setup and [provisioning contract](../docs/API_CONTRACT.md), create a fresh pending environment and submit a normal `success` provisioning request with a fresh key. Record the environment/operation IDs, accepted HTTP response, and later operation status. A 202 response proves acceptance, not that a worker consumed the message.

Inspect the effective queue overlay configuration as needed:

```bash
docker compose -f compose.yaml -f infra/incidents/queue.yaml config
```

### Repair and verify

Make a persistent configuration repair and check with the queue scenario still active:

```bash
python3 lab.py check 4
```

Confirm an accepted operation completes through the real worker, then record the evidence and stop the scenario:

```bash
python3 lab.py incident stop queue
```

The CLI includes active overlays for its service-changing commands; a plain base-only Compose recreation may not represent the scenario you are investigating. Logs/inspection commands do not themselves repair it.

## Acceptance criteria

- [ ] Both incidents are reproduced independently with commands, timestamps, and observed symptoms.
- [ ] Repairs are in persistent learner configuration and survive the checker's service recreation.
- [ ] Proxy recovery is demonstrated through public health/API requests, not only an internal API check.
- [ ] Queue recovery is demonstrated by a real worker/provider result, not only a successful POST or a worker process existing.
- [ ] The first scenario is stopped before the second starts; both are stopped when finished.
- [ ] One English incident note per scenario covers symptom → evidence → cause → repair → verification → prevention.

## Deliverables

Submit configuration changes, before/after command output, operation/request evidence, both `check 4` results, and two short notes using [the incident appendix](../notes/TEMPLATE.md). Do not repair unrelated application exercises or change host services to satisfy this incident task.
