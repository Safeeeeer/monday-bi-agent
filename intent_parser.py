from groq import Groq
import json
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def interpret_query(user_input, chat_history=None):

    system_prompt = """
You are a Business Intelligence query parser.

Return STRICT JSON:

{
  "intent": "pipeline" | "revenue" | "compare" | "breakdown" | "conversion" | "top_sector",
  "sector": "sector name or null",
  "time_range": "this_quarter" | "last_quarter" | "this_month" | "all_time"
}
"""

    messages = [{"role": "system", "content": system_prompt}]

    if chat_history:
        messages.extend(chat_history)

    messages.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0
    )

    content = response.choices[0].message.content.strip()

    try:
        return json.loads(content)
    except:
        return {"intent": "breakdown", "sector": None, "time_range": "this_quarter"}