
import requests
import json
import sys

def test_chat(message, valid_sources=False):
    url = "http://localhost:8000/chat"
    print(f"\n--- Testing: '{message}' ---")
    try:
        response = requests.post(url, json={"message": message})
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "")
            sources = data.get("sources", [])
            print(f"Answer: {answer[:100]}...")
            print(f"Sources Count: {len(sources)}")
            
            if valid_sources:
                if len(sources) > 0:
                    print("✅ PASS: Sources returned as expected.")
                else:
                    print("❌ FAIL: Expected sources but got none.")
            else:
                if len(sources) == 0:
                     print("✅ PASS: Sources empty as expected.")
                else:
                     print(f"❌ FAIL: Expected empty sources but got {len(sources)}.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    # 1. Greeting (Expect empty sources)
    test_chat("هلا", valid_sources=False)
    
    # 2. Greeting 2 (Expect empty sources)
    test_chat("السلام عليكم", valid_sources=False)
    
    # 3. Out of scope (Expect empty sources due to gating)
    test_chat("ما هي عاصمة فرنسا؟", valid_sources=False)
    
    # 4. In scope (Expect sources)
    test_chat("ما عاصمة السعودية؟", valid_sources=True)
