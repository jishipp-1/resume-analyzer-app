import os
from openai import OpenAI

# Initialize client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

def detect_role(resume_text: str) -> str:
    prompt = f"""You are a resume classifier. Choose only one label from:
["Frontend Developer","Backend Developer","Fullstack Developer","DevOps Engineer",
 "Data Analyst","Machine Learning Engineer","HR Professional","Marketing",
 "Project Manager","QA Engineer","Other"]

Resume text:
{resume_text[:3500]}
Return only the label."""

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0,
        )
        label = resp.choices[0].message.content.strip()
        return label

    except Exception:
        # Fallback if AI fails
        t = resume_text.lower()
        if "react" in t or "javascript" in t:
            return "Frontend Developer"
        if "spring" in t or "java" in t:
            return "Backend Developer"
        return "Other"


def analyze_resume_evidence(found_keywords, missing_keywords, role, excerpt):
    prompt = f"""
You are an expert resume reviewer.

Role: {role}
Found keywords (with small snippets): {found_keywords or 'None'}
Missing keywords: {missing_keywords or 'None'}
Resume excerpt:
{excerpt[:2000]}

Using ONLY the evidence above, give:
1) 3-5 concise strengths.
2) 3-5 concise gaps.
3) 5 short improvements / bullet-lines candidate can copy/paste.

Be factual and conservative.
"""

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=800,  # ✅ correct argument for current SDK
        )
        return resp.choices[0].message.content.strip()

    except Exception as e:
        return f"Analysis generation error: {e}"
