# Exercise 3 — Make asynchronous provisioning reliable

**Target time:** 120 minutes. **Your role:** backend engineer responsible for a background workflow that calls another service.

## The problem

An owner requests provisioning of a pending environment. The API creates an Operation and a worker calls the fake provider. A normal request can succeed, but the starter is unreliable when requests repeat, a provider fails temporarily, a response is lost after creation, or a task is delivered more than once.

A lost response is particularly important: the caller did not receive confirmation, but the provider may already have created a resource. Your job is to preserve one logical operation/resource, report truthful state, and settle failures within a bounded time.

## Before you start

Read [the shared workflow](../docs/EXERCISE_WORKFLOW.md), [provisioning/idempotency](../docs/API_CONTRACT.md), and [provider behavior](../docs/API_CONTRACT.md). Use real PostgreSQL, Redis, the provider service, and a Celery worker. Eager/synchronous unit execution alone is not sufficient evidence.

`Idempotency-Key` identifies a logical request within an organization and operation kind. Retrying that same request must not create a new logical effect. An Environment's lifecycle and its Operation's status are related but separate records.

## Reproduce the problem

1. Run `python3 lab.py check 3` and keep the API and worker scenario results.
2. Obtain an owner token/project ID using the shared setup. Create a fresh pending record with `POST /api/environments/`, such as `{"name":"async-example-1","project":<your project ID>}`. Capture the returned environment ID.
3. Send `POST /api/environments/{id}/provision/` with JSON `{"scenario":"success"}` and a fresh `Idempotency-Key`, then inspect the returned operation through `GET /api/operations/{operation_id}/`.
4. Repeat the request with exactly the same key/body. Compare operation IDs, statuses, and provider evidence.
5. Use a fresh pending environment and fresh key for each different provider scenario below. Record the before/after state and relevant worker logs.

Use actual response IDs; placeholder braces are not literal IDs. A ready or failed environment is not a fresh pending test case. Seeded `seed-…` references are fictional history, not proof that the provider contains corresponding resources.

## Required request and lifecycle rules

| Case | Required outcome |
|---|---|
| New valid key on a pending environment | 202, one Operation, environment moves to provisioning on acceptance; worker may also enforce the transition. |
| Same key and identical environment/scenario | 200 and the same logical Operation, including after it finishes. |
| Same key but a different environment or scenario | 409, no new operation or remote side effect. |
| Same literal key in another organization | Independent key scope; it must not reuse the first organization's operation. |
| New key on provisioning/ready/failed environment | 409. An already accepted replay is considered before rejecting a new lifecycle request. |
| Eight genuinely parallel identical API requests | One logical Operation and consistent 200/202 results on PostgreSQL. |
| Missing/overlong key, unknown scenario, missing environment | Follow the API contract; no successful partial effect. Keys are 1–80 characters. |
| Unauthorized caller | Preserve endpoint membership/role rules; valid owner/developer access still works. |

## Required provider outcomes

| Scenario | Simulator behavior | Required final outcome |
|---|---|---|
| `success` | Immediate creation. | Environment ready, Operation succeeded, resource reference recorded. |
| `transient` | First request fails before creation; a later attempt can succeed. | Recover to ready/succeeded within the bounded policy. |
| `lost_response` | Resource is committed before a delayed response; the caller can time out. | Recover without creating an extra resource; finish ready/succeeded. |
| `permanent` | Provider rejects the request without creation. | Settle failed with a useful nonempty error; do not retry a terminal validation failure. |

At most **3 provider creation attempts** per operation; HTTP connect/read timeouts at most **1 second each**; retry delay at most **2 seconds**. Bounded scenarios must settle within **25 seconds** on healthy infrastructure. Do not reset the attempt budget when a message is redelivered.

Four concurrent duplicate task deliveries through a real worker must create **zero additional resources** and preserve a terminal outcome. Local database state must be committed before task dispatch. Explain why a database transaction alone cannot undo a completed remote HTTP effect.

## Where to investigate

`backend/lab/views.py` receives provisioning requests; `serializers.py` defines inputs; `services.py` coordinates operation acceptance; `tasks.py` performs background work; `models.py` stores lifecycle/operation/event data. Read `provider/server.py` to understand the simulator contract, not to weaken its scenarios. The exercise does not prescribe a particular synchronization or recovery implementation.

## Acceptance criteria

- [ ] Request replay, key scope, conflicts, lifecycle rejection, and authorization follow the contract.
- [ ] Eight parallel API requests preserve one logical Operation.
- [ ] Success, transient, lost-response, and permanent scenarios settle as specified.
- [ ] Attempts, timeouts, delays, errors, and terminal-state handling are bounded and observable.
- [ ] Four concurrent worker redeliveries do not create extra resources or regress terminal state.
- [ ] The note explains remote uncertainty and the remaining production delivery limitation: database commit and broker publication are not one distributed transaction. Full outbox recovery is outside this exercise.

## Verification and deliverables

```bash
python3 lab.py check 3
docker compose logs --tail=100 api worker provider
```

The check creates uniquely named diagnostic environments/operations in the live database and preserves them for investigation; API unit tests use a separate test database. Submit changes, regression tests, operation/resource evidence for each scenario, parallel/redelivery results, and an English [engineering note](../notes/TEMPLATE.md). Do not claim a real worker/concurrency check from an eager-only or SQLite run.
