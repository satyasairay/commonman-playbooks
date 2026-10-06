"""Run a command, preserving its exit status and redacting local paths."""
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

def redact(text):
    for value in (str(ROOT), ROOT.as_posix(), str(Path.home()), Path.home().as_posix()):
        text = text.replace(value, '<repo>' if Path(value) == ROOT else '<home>')
        text = text.replace(value.replace('\\', '\\\\'), '<repo>' if Path(value) == ROOT else '<home>')
    return text

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    os.environ['PYTHONUTF8'] = '1'
    output = Path(sys.argv[1])
    run = subprocess.run(sys.argv[2:], cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    log = redact(run.stdout + run.stderr) + f'\nEXIT {run.returncode}\n'
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(log, encoding='utf-8')
    print(log if len(log) < 12000 else log[:1500] + '\nFull output saved in ' + str(output) + '\n' + log[-2500:])
    sys.exit(run.returncode)
