
import requests
import json

def verify_gating():
    url = "http://localhost:8000/chat"
    
    test_cases = [
        {"name": "Greeting", "query": "هلا"},
        {"name": "Out-of-scope", "query": "ما هي عاصمة فرنسا؟"},
        {"name": "In-scope", "query": "ما عاصمة السعودية؟"}
    ]
    
    with open("verify_output.txt", "w", encoding="utf-8") as f:
        for case in test_cases:
            f.write(f"--- Testing {case['name']}: '{case['query']}' ---\n")
            try:
                resp = requests.post(url, json={"message": case['query']})
                data = resp.json()
                
                sources = data.get("sources", [])
                f.write(f"Sources Length: {len(sources)}\n")
                if len(sources) > 0:
                    f.write(f"Top Score: {sources[0].get('score', 'N/A')}\n")
                else:
                    f.write("Sources: []\n")
                    
                f.write("-" * 30 + "\n")
                
            except Exception as e:
                f.write(f"Error: {e}\n")

if __name__ == "__main__":
    verify_gating()
