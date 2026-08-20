ASSET_SYSTEM_PROMPT = """
You are a senior AI project mentor helping a learner polish a capstone project.
Create practical, clear, beginner-friendly Markdown.
Do not invent fake links, fake metrics, or fake deployment URLs.
Write in a professional but simple style.
""".strip()


def build_readiness_checklist_prompt(profile_text: str) -> str:
    return f"""
Capstone project profile:
{profile_text}

Create readiness_checklist.md.
Include sections for:
- Local setup
- Environment variables
- Model readiness
- App functionality
- Error handling
- Documentation
- Demo readiness
- Portfolio readiness
Use Markdown checkboxes.
""".strip()


def build_readme_draft_prompt(profile_text: str) -> str:
    return f"""
Capstone project profile:
{profile_text}

Create README_draft.md for the capstone project.
Include:
- Project title
- Project overview
- Features
- Architecture
- Tech stack
- Setup steps
- Run commands
- Demo flow
- Future improvements
Keep it beginner-friendly.
""".strip()


def build_demo_script_prompt(profile_text: str) -> str:
    return f"""
Capstone project profile:
{profile_text}

Create demo_script.md.
This should be a spoken demo script for a course or portfolio walkthrough.
Include:
- Opening
- Problem statement
- Architecture explanation
- Live demo steps
- What to highlight
- Closing
Make it natural and easy to read aloud.
""".strip()


def build_qa_prep_prompt(profile_text: str) -> str:
    return f"""
Capstone project profile:
{profile_text}

Create qa_prep.md.
Include likely questions a reviewer, learner, or interviewer may ask.
For each question, provide a clear answer.
Cover:
- Why Ollama
- Why local first
- How the app works
- Deployment readiness
- Limitations
- Improvements
- Troubleshooting
""".strip()
