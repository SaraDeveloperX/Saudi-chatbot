import os
import json
import logging
from typing import List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure logging to console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_openai_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    return OpenAI(api_key=api_key)

def rerank(question: str, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Reranks a list of candidate documents based on their relevance to the question
    using gpt-4o-mini.
    
    Args:
        question: The user's question.
        candidates: List of dictionaries, each containing at least 'text'.
        
    Returns:
        List[Dict]: The candidates list with updated scores and sorted by relevance.
                    Adds 'rerank_score' to each candidate.
    """
    if not candidates:
        return []

    # Prepare candidates for the prompt (trim to max 600 chars)
    prompt_candidates = []
    for idx, cand in enumerate(candidates, 1):
        text_snippet = cand.get("text", "")[:600]
        # Clean up newlines for cleaner prompt
        text_snippet = text_snippet.replace("\n", " ")
        prompt_candidates.append(f"[{idx}] {text_snippet}")

    candidates_block = "\n\n".join(prompt_candidates)

    system_prompt = """أنت خبير في ولاية دقة استرجاع المعلومات.
مهمتك هي تقييم مدى صلة النصوص المسترجعة بسؤال المستخدم.
للقيام بذلك:
1. اقرأ السؤال والنصوص المرقمة.
2. لكل نص، حدد درجة الصلة (score) بين 0.0 (غير ذي صلة تمامًا) و 1.0 (شديد الصلة).
3. أخرج النتيجة بتنسيق JSON حصريًا.

التنسيق المطلوب:
{
  "ranking": [
    {"i": 1, "score": 0.95},
    {"i": 2, "score": 0.30}
    ...
  ]
}
حيث "i" هو رقم النص في القائمة (1-based index).
"""

    user_prompt = f"""السؤال: {question}

النصوص المرشحة:
{candidates_block}

المطلوب:
قم بترتيب النصوص حسب الصلة وأعطني JSON فقط."""

    client = get_openai_client()

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0,
            timeout=10 # Fail-safe timeout
        )

        content = response.choices[0].message.content
        if not content:
            logger.warning("Reranker returned empty content.")
            return candidates

        data = json.loads(content)
        ranking = data.get("ranking", [])

        # Create score map: index (int) -> score (float)
        score_map = {}
        for item in ranking:
            try:
                idx = int(item.get("i"))
                score = float(item.get("score"))
                score_map[idx] = score
            except (ValueError, TypeError):
                continue

        # Assign scores to candidates
        # Note: prompt used 1-based index, cand list is 0-based
        for i, cand in enumerate(candidates):
            # Default to 0.0 if not found in LLM output, or keep original weak score behavior?
            # We'll default to 0.0 effectively dropping it if strictly filtering.
            # But let's check if we want fallback for items missed?
            # Usually LLM should return all, but if it skips, it's likely irrelevant.
            cand["rerank_score"] = score_map.get(i + 1, 0.0)

        # Sort by rerank_score descending
        candidates.sort(key=lambda x: x["rerank_score"], reverse=True)
        
        return candidates

    except Exception as e:
        logger.error(f"Reranking failed: {e}. Falling back to original order.")
        # Fallback: maintain original order. 
        # Mark them with a special flag or just copy original score?
        # Use simple heuristic: map 'score' (original) to 'rerank_score' if available for compatibility
        for cand in candidates:
            cand["rerank_score"] = cand.get("score", 0.0) # Fallback to search score
            cand["rerank_fallback"] = True
            
        return candidates
