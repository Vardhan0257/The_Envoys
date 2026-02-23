from openai import OpenAI
import json

client = OpenAI()

MODEL = "gpt-4o-mini"

def generate_naive(context: str, question: str):
    prompt = f"""
Use ONLY the provided context to answer.

Context:
{context}

Question:
{question}
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return resp.choices[0].message.content

def generate_structured(context: str, question: str):
    prompt = f"""
You must respond in STRICT JSON.

Format:
[
  {{
    "claim": "...",
    "evidence_chunk_id": "chunk_X"
  }}
]

Only include claims directly supported by the context.

Context:
{context}

Question:
{question}
"""

    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = resp.choices[0].message.content
    return json.loads(content)  # hard fail if invalid
