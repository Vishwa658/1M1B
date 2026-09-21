from openai import OpenAI

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_BASE_URL
)


SYSTEM_PROMPT = """
You are the General AI assistant inside AquaGuard AI.

Answer the user's general questions clearly and accurately.

You can help with:

- General knowledge
- Artificial intelligence
- Programming
- Python
- Technology
- Science
- Education
- Environment
- Sustainability
- Water-related concepts
- Climate concepts

Important rules:

1. Give simple explanations suitable for beginners.

2. If the user asks about current or official
   AquaGuard groundwater measurements, do not invent data.

3. Do not pretend that general knowledge is official
   Chennai government data.

4. Clearly distinguish facts, estimates and suggestions.

5. Do not invent government projects or statistics.

6. Answer the question directly.

7. Use examples when they help the user understand.
"""


def ask_general_ai(question, history=None):

    if not GROQ_API_KEY:
        return (
            "Groq API key is not configured. "
            "Please configure GROQ_API_KEY in the .env file."
        )

    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL
    )

    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    for item in history[-10:]:

        role = item.get("role")
        content = item.get("content")

        if role in ["user", "assistant"] and content:

            messages.append(
                {
                    "role": role,
                    "content": content
                }
            )

    messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    response = client.responses.create(
        model=GROQ_MODEL,
        input=messages
    )

    return response.output_text