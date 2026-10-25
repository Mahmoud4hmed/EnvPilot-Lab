# EnvPilot Training

A local, two-day engineering lab for a fictional product that manages temporary development environments. The 14-hour schedule includes seven exercises and an independent three-hour mock assessment.

- `EnvPilot-Lab/`: the learner repository, exercises, notes, and startup guide.
- `EnvPilot-Instructor/`: behavioral graders, harness tests, and the independent mock template. Keep this folder adjacent to the learner directory; avoid browsing instructor materials during training.
- `EnvPilot_Two_Day_Lab_Codex_Prompt.md`: the original lab requirements.

Start with [EnvPilot-Lab/START_HERE.md](EnvPilot-Lab/START_HERE.md).

Clone the repository, then run the lab:

```powershell
git clone https://github.com/Mahmoud4hmed/EnvPilot-Lab.git
cd EnvPilot-Lab/EnvPilot-Lab
python lab.py doctor
python lab.py up
python lab.py check smoke
```

On Linux/WSL2, use `python3` instead of `python` if needed. Docker Engine with Compose v2 is required. Everything runs locally; no paid services or cloud credentials are required.

Instructor reference solutions, construction validation copies, personal notes, dependency directories, and local exam submissions are excluded from the public repository. The intentionally incomplete learner exercises remain intact. This is a self-study lab and does not claim to reproduce any employer's assessment.

The independent mock will be created as `EnvPilot-Mock/` beside the two supplied directories when you explicitly run `python lab.py exam start`. Its clock is not started by cloning or normal lab startup.

See [EnvPilot-Lab/VERIFICATION.md](EnvPilot-Lab/VERIFICATION.md) for the existing Docker startup limitation and the checks already executed.
