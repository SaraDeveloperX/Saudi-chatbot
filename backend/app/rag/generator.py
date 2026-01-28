import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

NO_ANSWER_MESSAGE = "عذرًا، لم أتمكن من العثور على هذه المعلومة في السياق المتاح."

def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    return OpenAI(api_key=api_key)

def generate_answer(question: str, contexts: list) -> str:
    """
    Generate an Arabic answer using OpenAI based on retrieved contexts.
    Returns the no-answer message if contexts are empty.
    """
    if not contexts:
        return NO_ANSWER_MESSAGE
    
    # Build context string with numbered references
    context_parts = []
    for i, ctx in enumerate(contexts, 1):
        context_parts.append(f"[{i}] {ctx['text']}")
    
    context_str = "\n\n".join(context_parts)
    
    # Build the prompt
    system_prompt = """You are an Arabic knowledge assistant.

Answer the user's question using ONLY the provided retrieved context.
If the answer is not found in the context, respond politely in Arabic that the information is not available.

IMPORTANT FORMATTING RULES:
- Output MUST be plain Arabic text only.
- DO NOT use Markdown formatting of any kind.
- DO NOT use symbols such as **, ##, -, *, or bullet Markdown.
- DO NOT use emojis.
- DO NOT use headings or titles with formatting.

STRUCTURE RULES:
- Use clear numbered lists in this exact format:

1) Title:
Explanation text in full sentences.

2) Title:
Explanation text in full sentences.

- Leave a blank line between each numbered item.
- If the answer is a paragraph, write it as clean Arabic paragraphs with proper punctuation.
- Keep the tone professional, neutral, and informative.

LANGUAGE RULES:
- Use Modern Standard Arabic (MSA).
- Avoid slang or casual phrasing.
- Keep sentences clear and easy to read.

CONSTRAINTS:
- Do not invent facts.
- Do not add information not present in the context.
- Do not mention sources explicitly in the text.

Return ONLY the final Arabic answer."""

    user_prompt = f"""السؤال: {question}

السياق:
{context_str}

الإجابة:"""

    client = get_openai_client()
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )
    
    return response.choices[0].message.content
