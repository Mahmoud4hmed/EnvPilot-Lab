from pathlib import Path
import subprocess
import sys
if len(sys.argv) != 2 or sys.argv[1] != 'check':
    raise SystemExit('Usage: python mock.py check')
raise SystemExit(subprocess.call([sys.executable,str(Path(__file__).resolve().parent.parent/'EnvPilot-Instructor'/'exam.py'),'check','--mock-root',str(Path(__file__).resolve().parent)]))
