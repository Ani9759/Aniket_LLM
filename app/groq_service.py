from groq import Groq

from .config import GROQ_API_KEY


groq_client = Groq(
    api_key=GROQ_API_KEY
)


def generate_answer(query: str, search_results: list):

    context = ""

    for i, result in enumerate(search_results, start=1):

        title = result.get("title", "")
        url = result.get("url", "")
        content = result.get("content", "")

        context += f"""
SOURCE {i}

TITLE:
{title}

URL:
{url}

CONTENT:
{content}

--------------------------------
"""

    prompt = f"""
You are an AI company research assistant.

USER QUESTION:
{query}

The following information was retrieved from the live internet
using a web search engine.

WEB SOURCES:
{context}

Instructions:

1. Answer the user's question using the retrieved sources.
2. Focus on recent information when the user asks for latest information.
3. Prefer official company sources where available.
4. Prefer reliable news organizations.
5. Do not invent information.
6. If the available information is insufficient, clearly say so.
7. Mention dates when relevant.
8. Organize the answer using headings and bullet points.
9. At the end, provide a Sources section.
10. Include the URL of each important source.

Give a concise but informative answer.
"""

    response = groq_client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": "You are a factual company research assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.2,

        max_tokens=2000
    )

    return response.choices[0].message.content