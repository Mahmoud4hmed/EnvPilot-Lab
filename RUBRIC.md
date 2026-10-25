# Training rubric — 100 weighted points

| Exercise | Weight | Observable behavior (80% of exercise) | Engineering evidence (20%) |
|---|---:|---|---|
| 1 API | 20 | Auth, tenant list/detail/related IDs, role, validation, valid requests | Regression tests and permission explanation |
| 2 DB | 12 | Constant query growth and correct fields/filter/order/pages | Before/after counts and EXPLAIN/index decision |
| 3 async | 25 | Replay/conflict, real PG parallel calls, retries/reconciliation, real worker redelivery | State/error reasoning and remote-effect tradeoffs |
| 4 ops | 12 | Two durable repairs surviving recreation and working request/job | Two evidence-based incident notes |
| 5 UI | 14 | Async states/races/cleanup, truthful readiness, name search, browser path | Typed boundaries and regression tests |
| 6 Ansible | 7 | Correct contents/modes, no-change second run, changed input | Maintainable declarative tasks and evidence |
| 7 AI | 10 | Grounding/isolation/schema/fallback/tools incl. valid access | Evaluation notes and limitations |

Partial credit: award behavioral points in proportion to passed independent criteria within each exercise; parameter cases count as separate behavior checks. Infrastructure failures are ungraded, not learner failures.
For exercise 4 each incident is half its behavioral points; exercise 6 content/modes, unchanged second run, changed input each earn one third.
Engineering evidence: 0% absent; 50% plausible but incomplete; 100% clear reproducible tests/commands, decision tradeoffs and remaining risks. No points for a particular component layout, source keywords, or exact answer prose.
`check` prints pass/fail evidence and writes XML/JSON for API/UI checks to .lab/reports. CLI-only checks print file/worker evidence. A passing automatic check does not award manual evidence points by itself.
Checks are read-only with respect to source, but create isolated test DBs and diagnostic live operations/fixture files as documented. They do not install a solution.
The independent mock is scored separately; its scoring criteria appear at mock start.
