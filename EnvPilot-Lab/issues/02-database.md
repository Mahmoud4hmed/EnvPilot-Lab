# Exercise 2 — Diagnose and improve PostgreSQL access

Estimated time: 60 minutes (target timebox).

## Context and symptoms

The environment list slows down as the page size increases. Seeded project and audit history data are representative enough to reproduce query growth. Product behavior must stay the same.

## Acceptance criteria

- Capture query counts at 5, 20, and 60 results before/after; query growth must remain within two queries and fixed overhead ≤12.
- Preserve latest-event selection, fields, tenant boundaries, descending IDs, status filters, counts, and pagination.
- Run EXPLAIN (ANALYZE, BUFFERS) against PostgreSQL. Explain one index/query-plan decision with measured selectivity; a justified decision not to add an index is valid.
- Explain memory/maintenance tradeoffs; avoid a wall-clock benchmark requirement.

## Relevant checks

```bash
python lab.py check 2
docker compose exec api python manage.py profile_queries --organization 1
```

Performance checks use an authorized organization so exercise 1 is not a prerequisite for measuring query growth.

Deliver: working changes, regression evidence, and a short English engineering note using notes/TEMPLATE.md.
