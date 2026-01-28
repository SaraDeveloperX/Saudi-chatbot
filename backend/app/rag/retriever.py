import os
import weaviate
from openai import OpenAI
from dotenv import load_dotenv
from .reranker import rerank

load_dotenv()

COLLECTION_NAME = "KnowledgeDocument"


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    return OpenAI(api_key=api_key)

def embed_query(query: str) -> list:
    """Embed the query using OpenAI text-embedding-3-small."""
    client = get_openai_client()
    clean_query = query.replace("\n", " ")
    response = client.embeddings.create(
        input=[clean_query],
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def retrieve(query: str, top_k: int = 3) -> list:
    """
    Retrieve relevant documents from Weaviate and rerank them.
    Returns list of dicts with text, question, section, source, score.
    """
    # retrieval constants
    TOP_K_CANDIDATES = 10
    RERANK_THRESHOLD = 0.5  # Filter out candidates with low LLM relevance score

    # Connect to Weaviate
    weaviate_client = weaviate.connect_to_local(port=8080)
    
    try:
        # Embed the query
        query_vector = embed_query(query)
        
        # Perform Hybrid Search (Vector + Keyword)
        collection = weaviate_client.collections.get(COLLECTION_NAME)
        response = collection.query.hybrid(
            query=query,
            vector=query_vector,
            alpha=0.6, # 0.6 = favor vector slightly
            limit=TOP_K_CANDIDATES, # Retrieve more for reranking
            return_metadata=weaviate.classes.query.MetadataQuery(score=True, explain_score=True, distance=True, certainty=True)
        )
        
        # Convert objects to candidates list
        candidates = []
        if response.objects:
            for obj in response.objects:
                candidates.append({
                    "text": obj.properties.get("text", ""),
                    "question": obj.properties.get("question", ""),
                    "section": obj.properties.get("section", ""),
                    "source": obj.properties.get("source", ""),
                    "score": obj.metadata.score, # Keep hybrid score for reference/fallback
                    "certainty": obj.metadata.certainty,
                    "uuid": str(obj.uuid)
                })

        print(f"DEBUG: retrieval: hybrid top_k={TOP_K_CANDIDATES} found={len(candidates)}")
        
        if not candidates:
            return []

        # Rerank candidates
        reranked_candidates = rerank(query, candidates)
        
        # Check if fallback occurred (if 'rerank_fallback' is present and True)
        is_fallback = any(c.get('rerank_fallback') for c in reranked_candidates)
        top_rerank_score = reranked_candidates[0].get('rerank_score', 0.0) if reranked_candidates else 0.0
        
        print(f"DEBUG: rerank: enabled top_final={top_k} top_rerank_score={top_rerank_score:.4f} fallback={is_fallback}")

        final_results = []
        for cand in reranked_candidates:
            r_score = cand.get('rerank_score', 0.0)
            
            # If fallback logic was triggered inside reranker, we trust original scores/order
            # But the prompt said: "If reranker score < THRESHOLD, drop candidate"
            # It also said "stable behavior if reranker fails (fallback works)"
            # If fallback used, we probably shouldn't filter by RERANK_THRESHOLD which defaults to 0.0 in fallback?
            # In reranker.py fallback, I mapped original score to rerank_score.
            # Hybrid scores are unbounded (can be > 1 or < 0 or small).
            
            if is_fallback:
                # In fallback, just take them all (or trust hybrid order)
                final_results.append(cand)
            else:
                if r_score >= RERANK_THRESHOLD:
                    # Update the visible score to be the reranker score
                    cand['score'] = r_score 
                    final_results.append(cand)
        
        # Slice to final top_k
        final_results = final_results[:top_k]
        
        print(f"DEBUG: returned_sources={len(final_results)}")
        
        # Strip internal keys before returning if needed, but extra keys usually fine
        # Ensure 'score' is float and rounded
        for res in final_results:
            if isinstance(res['score'], float):
                res['score'] = round(res['score'], 4)

        return final_results
        
    finally:
        weaviate_client.close()

