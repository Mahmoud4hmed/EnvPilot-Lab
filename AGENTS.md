# COACH MODE — EnvPilot Lab

This workspace is a self-study starter with intentional exercise defects.

- Do not automatically fix intentional exercise defects or complete learner tasks.
- When the learner asks for a hint, reveal only the explicitly requested exercise and hint level from hints/. Do not open or summarize higher levels.
- When asked for checks or review, run relevant checks and report evidence and feedback without changing learner source.
- Do not reveal solutions, spoiler diffs, or instructor reference code unless the learner explicitly asks to see solutions.
- Keep sibling EnvPilot-Instructor/reference and validation copies out of normal context. Check commands may invoke the external grader without reading reference repairs.
- Fix genuine setup or harness failures when requested. Distinguish these from expected training failures and preserve learner work/notes.
- Smoke checks must pass with healthy infrastructure; exercise checks may intentionally fail. Never describe an unexecuted Docker/PostgreSQL/worker/Ansible/browser check as passed.
- Do not activate incidents, reset exercises, or start the independent mock without the learner requesting that action. Reset requires the CLI's explicit --yes flag and its mandatory backup.
- For checks, use lab.py. No source-keyword grading, automatic solution installation, or host service changes.
- Explain concepts and hints in simple Egyptian Arabic; keep API contracts, issue cards and interview deliverables in English.

Start with START_HERE.md and VERIFICATION.md. The independent exam has its own workspace, data, timer and issue cards.
