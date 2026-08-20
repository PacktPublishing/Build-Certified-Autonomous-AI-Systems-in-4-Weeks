"""Prompt templates for the Day 16 final presentation lab.

Each function returns one complete prompt. Keeping prompts here makes the app
feel organized and makes it easy for learners to improve the coaching style.
"""

from __future__ import annotations


COACHING_STYLE = """
You are a practical product demo coach helping a beginner present their final AI project.
Write in clear, confident, human language.
Avoid hype, vague claims, and complicated startup jargon.
Make the output specific to the product brief.
Use Markdown.
""".strip()


def final_demo_script_prompt(product_brief: str) -> str:
    """Build the final spoken demo script."""
    return f"""
{COACHING_STYLE}

Create `final_demo_script.md` for this product.

The script should help the presenter speak naturally during a live demo.
It should include:

# Final Demo Script

## 1. Opening
A short welcome and one-line explanation of the product.

## 2. Problem
Explain the user's pain in simple terms.

## 3. Product Walkthrough
A step-by-step demo flow with spoken lines for each step.

## 4. Technical Explanation
A beginner-friendly explanation of how the app works behind the scenes.
Mention Ollama only if it makes sense for the product.

## 5. Value Proposition
Explain why the product is useful.

## 6. Limitations
Mention honest limitations without weakening confidence.

## 7. Closing
End with a strong final line.

Product brief:
{product_brief}
""".strip()


def judge_rubric_prompt(product_brief: str) -> str:
    """Build a simple judging rubric for the final demo."""
    return f"""
{COACHING_STYLE}

Create `judge_rubric.md` for this product demo.

The rubric should help someone evaluate the final presentation fairly.
Use a 100-point scoring system.

Include:

# Judge Rubric

## Scoring Summary
A Markdown table with categories, points, and what excellent means.

Required categories:
- Problem clarity
- Demo flow
- Product usefulness
- Technical explanation
- Presentation confidence
- Handling limitations
- Next-step thinking

## Detailed Notes For Judges
Explain what judges should listen for.

## Red Flags
List things that would lower the score.

## Bonus Points
List optional strengths that could impress judges.

Product brief:
{product_brief}
""".strip()


def launch_post_prompt(product_brief: str) -> str:
    """Build a launch announcement post."""
    return f"""
{COACHING_STYLE}

Create `launch_post.md` for this product.

The post should sound like a real founder or builder sharing a completed project.
Make it suitable for LinkedIn or a course community.
Keep it polished but not exaggerated.

Include:

# Launch Post

## Short Version
A concise social post under 900 characters.

## Longer Version
A more detailed launch post with:
- What I built
- Who it helps
- The problem it solves
- What I learned
- What I want feedback on

## Feedback Request
A short paragraph asking for useful feedback.

## Suggested Hashtags
5 to 8 relevant hashtags.

Product brief:
{product_brief}
""".strip()


def improvement_plan_prompt(product_brief: str) -> str:
    """Build a realistic post-demo improvement plan."""
    return f"""
{COACHING_STYLE}

Create `improvement_plan.md` for this product.

The plan should help the builder improve the project after the final demo.
Keep it realistic for a beginner or early-stage product builder.

Include:

# Improvement Plan

## Quick Fixes
Small improvements that can be done quickly.

## Product Improvements
Feature ideas that make the product more useful.

## Technical Improvements
Code, reliability, security, data, or deployment improvements.

## User Feedback Questions
Questions to ask early users.

## 7-Day Next Step Plan
A simple day-by-day plan for the next week.

## Final Recommendation
One practical recommendation for what to do first.

Product brief:
{product_brief}
""".strip()
