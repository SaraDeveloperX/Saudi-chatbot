import requests
import json
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

queries = [
    "ما عاصمة السعودية؟",
    "أين تقع منطقة عسير؟",
    "متى تأسست المملكة العربية السعودية؟"
]

url = "http://localhost:8000/chat"

print("--- Verifying Hybrid Search ---")
for q in queries:
    print(f"\nQuery: {q}")
    try:
        response = requests.post(url, json={"message": q})
        if response.status_code == 200:
            data = response.json()
            print(f"Answer: {data.get('answer')[:100]}...")
            sources = data.get('sources', [])
            print(f"Sources found: {len(sources)}")
            for i, s in enumerate(sources[:3]): # Show top 3 sources
                print(f"  {i+1}. Score: {s.get('score')} | Source: {s.get('source')} | Snippet: {s.get('snippet')[:50]}...")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request failed: {e}")
