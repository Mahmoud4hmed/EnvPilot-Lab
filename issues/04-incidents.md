# Exercise 4 — Investigate two Linux/Docker incidents

Estimated time: 75 minutes (target timebox).

## Context and symptoms

Normal startup is healthy. Activate each incident independently. Scenario proxy: API requests through the public local URL return 502 while the dashboard may still load. Scenario queue: POST accepts jobs, but they remain queued. Investigate logs, processes, ports and configuration.

## Acceptance criteria

- Reproduce both incidents separately with commands and timestamps.
- Make durable configuration repairs; checks recreate the active service before verifying behavior.
- Proxy: health/API through Nginx recover. Queue: accepted operation reaches ready via actual worker.
- Write one short incident note per scenario: symptoms, evidence, root cause, repair, verification, and prevention.
- Stop the scenario before activating the next; do not modify host services.

## Relevant checks

```bash
python lab.py incident start proxy
python lab.py check 4
python lab.py incident stop proxy
python lab.py incident start queue
python lab.py check 4
python lab.py incident stop queue
```

Run each check after your repair. check 4 does not silently activate incidents or repair configs. systemd/journalctl examples are in docs/CHEATSHEET.md.

Deliver: working changes, regression evidence, and a short English engineering note using notes/TEMPLATE.md.
