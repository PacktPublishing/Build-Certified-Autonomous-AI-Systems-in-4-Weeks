from pathlib import Path
import shutil

src = Path('/Users/arjunvaid/Desktop/day7-ai-copilot-interface')
dst = Path('/Users/arjunvaid/Desktop/day7-ai-copilot-interface-walkthrough-source')

shutil.rmtree(dst, ignore_errors=True)
dst.mkdir(parents=True)

for name in [
    'requirements.txt',
    'approval_service.py',
    'llm_service.py',
    'speech_service.py',
    'tts_service.py',
    'app.py',
]:
    shutil.copy2(src / name, dst / name)

print(dst)
