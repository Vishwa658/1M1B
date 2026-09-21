from openai import OpenAI

from config import (
    GROQ_API_KEY,
    GROQ_MODEL,
    GROQ_BASE_URL
)

from rag.rag_service import build_context


def ask_rag(question):

    if not GROQ_API_KEY:
        return {
            "answer": (
                "Groq API key is not configured. "
                "Please configure GROQ_API_KEY in the .env file."
            ),
            "sources": []
        }

    # Connect to Groq
    client = OpenAI(
        api_key=GROQ_API_KEY,
        base_url=GROQ_BASE_URL
    )

    # Retrieve relevant AquaGuard documents
    context, documents = build_context(question)

    prompt = f"""
You are AquaGuard AI.

You answer questions about:

- Groundwater
- Water sustainability
- Chennai
- Rainfall
- Water resources
- Environmental issues
- Groundwater recharge
- Water scarcity
- Flooding and drainage
- Government water-related information

Use the retrieved information below as your
primary source of factual information.

==================================================
RETRIEVED INFORMATION
==================================================

{context}

==================================================
USER QUESTION
==================================================

{question}

==================================================
RULES
==================================================

1. Use the retrieved information when relevant.

2. Do not invent groundwater measurements.

3. Do not invent government projects.

4. Do not present an estimate as an official measurement.

5. If the retrieved information is insufficient,
   clearly say that more information or data is required.

6. Explain technical information in simple language.

7. If discussing groundwater depth, remember that
   the value represents depth below ground level.

8. Do not automatically classify groundwater as
   safe, dangerous or critical unless an authoritative
   classification is available in the retrieved data.

9. Mention relevant source documents when useful.

10. Answer the user's question directly.
"""

    response = client.responses.create(
        model=GROQ_MODEL,
        input=prompt
    )

    sources = []

    for document in documents:

        filename = document.get("filename")

        if filename:
            sources.append(filename)

    return {
        "answer": response.output_text,
        "sources": sources
    }