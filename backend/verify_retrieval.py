import sys
import os

# Add backend directory to sys.path so we can import app modules
# Assuming this script is placed in backend/
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

from app.rag.retriever import retrieve

queries = [
    "ما عاصمة السعودية؟",
    "أين تقع منطقة عسير؟",
    "متى تأسست المملكة العربية السعودية؟"
]

print("Starting Verification of LLM Reranker...")
print("-" * 50)

for q in queries:
    print(f"\n>> QUERY: {q}")
    try:
        results = retrieve(q, top_k=3)
        if not results:
            print("  No results found.")
        else:
            for i, r in enumerate(results):
                score = r.get('score', 'N/A')
                text = r.get('text', '')[:120].replace("\n", " ")
                print(f"  [{i+1}] Score: {score} | {text}...")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\nVerification Complete.")
