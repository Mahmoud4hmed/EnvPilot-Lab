# Exercise 2 — Diagnose and improve PostgreSQL access

**Target time:** 60 minutes. **Your role:** backend engineer investigating database work behind a slow list endpoint.

## The problem

The dashboard lists environments together with project/organization information and the latest history event. As a page contains more records, the starter performs increasing database work. This can make a larger page expensive even though it is still one HTTP request.

Your task is to measure and reduce query growth without changing the API's results. This is a database-access exercise, not a CSS task or a contest to obtain the lowest laptop response time.

## Before you start

Read [the shared workflow](../docs/EXERCISE_WORKFLOW.md) and [the environment-list contract](../docs/API_CONTRACT.md). Use PostgreSQL and an organization you are authorized to read. Exercise 1 is not a prerequisite for measuring the valid list path.

Discover your organization ID from `/api/me/`; the examples below assume you ran the shared API setup and have `ALPHA_ORG_ID`.

## Reproduce and measure

```bash
python3 lab.py check 2
docker compose exec api python manage.py profile_queries --organization "$ALPHA_ORG_ID"
```

The profiling command serializes 5, 20, and 60 rows, prints one `{rows, queries}` result per size, and prints a PostgreSQL execution plan for a pending-environment query. Record all three counts and the plan before editing. The normal seed has enough history and environments for these measurements; verify the reported row counts instead of measuring an accidentally empty organization.

Inspect the request path in `backend/lab/views.py`, queryset construction in `queries.py`, field generation in `serializers.py`, and relationships in `models.py`. You are investigating why data access changes with page size; do not change the response shape or remove required fields to reduce queries.

## Required behavior

| Concern | Required outcome |
|---|---|
| Query growth | Let the three counts be Q5, Q20, and Q60. `max(counts) - min(counts) <= 2` and `max(counts) <= 12`; all three sizes must meet this budget. |
| Latest event | Return the event with the highest numeric event ID, not an arbitrary event; return null when none exists. |
| Record data | Preserve IDs, names, project/organization fields, statuses, provider IDs, timestamps, and other contracted fields. |
| Filtering and boundaries | Preserve authorized organization scope and valid status filtering. |
| Ordering / pagination | Descending environment ID; count is the total after filtering; page limits/defaults and empty out-of-range pages follow the contract. |
| Query-plan evidence | Use PostgreSQL `EXPLAIN (ANALYZE, BUFFERS)` and explain an index/query-plan decision using observed selectivity and estimates versus actual rows. |

A justified decision **not** to add an index is acceptable. A sequential scan is not automatically a defect. Explain the cost of your approach, including extra memory, index storage/write maintenance, or data fetched but not needed. There is no required wall-clock benchmark result.

## Your evidence

Fill this in with your own results:

| Rows serialized | Queries before | Queries after |
|---:|---:|---:|
| 5 | | |
| 20 | | |
| 60 | | |

Include a plan excerpt and explain what distribution/selectivity it represents. Compare representative API responses before/after, including an environment with no events and one with several events. Explain why correctness is preserved, not just why the counts fell.

## Acceptance criteria

- [ ] Query counts meet the growth/overhead budget at all three sizes.
- [ ] Latest-event, null-event, field, scope, filter, order, count, and pagination behavior is preserved.
- [ ] PostgreSQL plan evidence supports an explicit index/query decision.
- [ ] The note explains memory/maintenance tradeoffs and includes before/after measurements.

## Verification and deliverables

```bash
python3 lab.py check 2
docker compose exec api python manage.py profile_queries --organization "$ALPHA_ORG_ID"
```

Submit source changes, regression evidence, the completed query-count table, a PostgreSQL plan excerpt, and an English [engineering note](../notes/TEMPLATE.md). SQLite timings or an empty dataset are not substitutes for the required evidence.
