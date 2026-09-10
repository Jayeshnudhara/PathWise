from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()


def generate_roadmap(career, skill_gaps):
    prompt = f"""
You are an AI career mentor for a platform called PathWise.

The student's target career is:
{career}

The student's skill gaps are:
{', '.join(skill_gaps)}

Create a practical learning roadmap for this student.

Give:
1. The recommended learning order
2. What to learn for each skill
3. One small project idea
4. A simple 4-week plan
5. Give the exact materials to use for free

Keep it beginner-friendly and concise.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text


