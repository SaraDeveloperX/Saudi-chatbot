#!/usr/bin/env python3
"""Verification script for greeting intent handling."""
import requests
import sys

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000"

test_cases = [
    ("hi", "greeting"),
    ("hello", "greeting"),
    ("السلام عليكم", "greeting-salam"),
    ("هلا", "greeting"),
    ("مرحبا", "greeting"),
    ("شكرا", "thanks"),
    ("يعطيك العافية", "thanks"),
    ("باي", "goodbye"),
    ("مع السلامة", "goodbye"),
]

print("=" * 60)
print("GREETING INTENT VERIFICATION")
print("=" * 60)

for msg, intent_type in test_cases:
    resp = requests.post(f"{BASE_URL}/chat", json={"message": msg})
    data = resp.json()
    answer = data.get("answer", "")[:80]
    sources = data.get("sources", [])
    sources_count = len(sources)
    
    # Check if it's the "not found" response
    is_not_found = "ما لقيت" in data.get("answer", "")
    status = "[FAIL - not found]" if is_not_found else "[PASS]"
    if sources_count > 0:
        status = "[FAIL - sources not empty]"
    
    print(f"\n[{intent_type.upper()}] Message: \"{msg}\"")
    print(f"  Status: {status}")
    print(f"  Answer: {answer}...")
    print(f"  Sources count: {sources_count}")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
