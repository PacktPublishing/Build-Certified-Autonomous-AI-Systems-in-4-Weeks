from pathlib import Path
import re

out_dir = Path('/Users/arjunvaid/lab_studio_v2/mcp_outputs')
base_path = out_dir / 'day7_ai_copilot_interface_walkthrough.md'
narrated_path = out_dir / 'day7_ai_copilot_interface_walkthrough_final.md'
final_path = out_dir / 'day7_ai_copilot_interface_walkthrough_structured_final.md'

base = base_path.read_text(encoding='utf-8')
narrated = narrated_path.read_text(encoding='utf-8')

pattern = re.compile(r'(### Step \d+ .+?)(?=\n### Step \d+ |\Z)', re.S)
base_blocks = pattern.findall(base)
narrated_blocks = pattern.findall(narrated)

if len(base_blocks) != len(narrated_blocks):
    raise SystemExit(f'Beat count mismatch: base={len(base_blocks)} narrated={len(narrated_blocks)}')


def walkthrough_body(block: str) -> str:
    marker = '**Walkthrough:**\n'
    if marker not in block:
        raise ValueError('Missing walkthrough marker')
    after = block.split(marker, 1)[1]
    if '\n---' not in after:
        raise ValueError('Missing separator after walkthrough')
    return after.rsplit('\n---', 1)[0]


def replace_walkthrough_body(block: str, new_body: str) -> str:
    marker = '**Walkthrough:**\n'
    before, after = block.split(marker, 1)
    old_body, suffix = after.rsplit('\n---', 1)
    return before + marker + new_body + '\n---' + suffix

merged_blocks = []
for base_block, narrated_block in zip(base_blocks, narrated_blocks):
    merged_blocks.append(replace_walkthrough_body(base_block, walkthrough_body(narrated_block)))

merged = '\n'.join(merged_blocks)

# Make the explicit structure display as a clean simple tree. This keeps the same six-file structure supplied to generation.
merged = merged.replace(
    '```\nrequirements.txt, approval_service.py, llm_service.py, speech_service.py, tts_service.py, app.py\n```',
    '```\nday7-ai-copilot-interface/\n  requirements.txt\n  approval_service.py\n  llm_service.py\n  speech_service.py\n  tts_service.py\n  app.py\n```'
)

final_path.write_text(merged, encoding='utf-8')
print(final_path.name)
print(f'beats={len(base_blocks)}')
