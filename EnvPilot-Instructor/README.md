# Instructor materials — spoilers

Keep this folder adjacent to EnvPilot-Lab. Avoid browsing graders and mock task cards during training.
Separation is for self-study, not a security boundary. The learner CLI mounts only grader/ read-only into test containers.

- grader/: behavioral API, performance, async and AI checks; live real-worker harness.
- mock-template/: independent three-task exam. Exact issue cards stay out of normal onboarding.
- mock-grader/: independent archive API checks, including PostgreSQL parallel calls.
- exam.py: persistent advisory timer, isolated workspace, submission snapshot and evidence report.
- tests/: CLI/exam/provider harness checks.

Reference repairs, construction scripts, validation copies, and detailed construction logs are local authoring materials and are excluded from the public repository. They are not required by lab.py check or the independent mock. Check commands do not install a solution.

See learner VERIFICATION.md for what ran during construction and what remains blocked. Its instructor-only validation procedure applies to the original authoring installation, where the excluded local materials are available.
