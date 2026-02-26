from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def generate_summary(user_input, computed_data):

    prompt = f"""
User asked:
{user_input}

Computed metrics:
{computed_data}

Write a concise founder-level business insight.

Include:
- Key metric
- Interpretation
- Risks
- Actionable takeaway
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()