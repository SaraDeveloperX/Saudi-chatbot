import requests
import json

# Test 1: In-scope query
print("=" * 60)
print("TEST 1: In-scope query")
print("=" * 60)
r = requests.post('http://localhost:8000/chat', json={'message': 'ما هي المملكة العربية السعودية؟'})
d = r.json()
print(f"Status: {r.status_code}")
print(f"Answer: {d['answer'][:500]}...")
print(f"Sources count: {len(d['sources'])}")
for i, s in enumerate(d['sources'][:3]):
    print(f"  [{i+1}] {s['section']}: {s['snippet'][:100]}...")

# Test 2: Out-of-scope query
print("\n" + "=" * 60)
print("TEST 2: Out-of-scope query")
print("=" * 60)
r2 = requests.post('http://localhost:8000/chat', json={'message': 'ما هي عاصمة فرنسا؟'})
d2 = r2.json()
print(f"Status: {r2.status_code}")
print(f"Answer: {d2['answer']}")
print(f"Sources count: {len(d2['sources'])}")
