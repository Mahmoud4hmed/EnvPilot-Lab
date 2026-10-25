# Independent three-hour mock

When you are ready, run `python lab.py exam start`.
The CLI copies an independent template from the instructor folder into the sibling `EnvPilot-Mock` directory once, then starts a separate `envpilot-mock` Compose project and database at http://localhost:8091.
The mock does not depend on your training exercise repairs. Its exact issue cards appear in `EnvPilot-Mock/TASKS.md` when you start it.

`python lab.py exam status` shows the UTC start time and remaining time. The clock continues when you close the terminal or browser.
Running `exam start` again resumes the same workspace and clock. The timer is advisory: reaching 180 minutes never deletes or locks your files.
`python lab.py exam submit` saves a source snapshot, runs checks, and produces a separate report. It preserves your original work and supports displaying the previous submission again.
The clock starts on the first start command, before stack setup. Record any setup interruptions for manual review; the timer is not a security boundary.
Feedback includes functional checks, manual review of your tests, diagnosis and engineering explanation, and your top three improvement priorities. The final score is out of 100 after manual review; automatic checks alone do not constitute a complete assessment.
There are three tasks: API behavior, React asynchronous state, and service configuration. Read the acceptance criteria when the mock starts and use its notes template.
