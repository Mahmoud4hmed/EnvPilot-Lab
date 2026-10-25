# Exercise 3 — Make asynchronous provisioning reliable

Estimated time: 120 minutes (target timebox).

## Context and symptoms

A normal provision succeeds, but temporary provider failures leave environments failed. Lost responses can leave live remote resources behind. Repeated requests and task redelivery do not behave consistently.

## Acceptance criteria

- Honor all key scope/replay/conflict rules, including eight genuinely parallel API requests on PostgreSQL.
- Implement explicit lifecycle transitions and a bounded 3-attempt retry/timeout policy.
- Recover transient and created-then-lost outcomes using provider contract; permanent failures settle with useful errors.
- Four concurrent duplicate deliveries through a real worker create zero additional resources and preserve terminal state.
- Verify API authorization, one success worker round trip, all deterministic failure scenarios, and a clear explanation of remote uncertainty.
- Commit local state before dispatch; state the remaining production delivery guarantee limitation.

## Relevant checks

```bash
python lab.py check 3
```

The check creates uniquely named diagnostic environments in the live DB and preserves them for investigation. Unit tests use a separate test DB. PostgreSQL/Redis/provider/worker must actually run; eager-only is not enough.

Deliver: working changes, regression evidence, and a short English engineering note using notes/TEMPLATE.md.
