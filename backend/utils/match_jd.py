import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

def compare_resume_and_jd(resume_text: str, jd_text: str) -> str:
    prompt = f"""
You are a resume-to-job-description comparison assistant.

Compare the following resume and job description, and provide:

1) Overall compatibility (High / Medium / Low)
2) 3-5 matching strengths (based on resume evidence)
3) 3-5 gaps or missing skills
4) 3 short recommendations to improve alignment

Resume:
{resume_text[:3000]}

Job Description:
{jd_text[:2000]}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are an expert HR analyst."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=800,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Comparison generation error: {str(e)}"
