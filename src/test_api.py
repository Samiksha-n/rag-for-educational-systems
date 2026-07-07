"""
Task 1: API Testing - Week 5
------------------------------
Tests all backend API endpoints for the RAG Educational System.

Verifies:
  - Status codes
  - JSON responses
  - Error conditions

Run with:
    pip install requests
    python test_api.py
    
Make sure app.py (Flask backend) is running first:
    python app.py
"""

import requests
import json

BASE_URL = "http://localhost:5000"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"

passed = 0
failed = 0

def test(name, condition, response=None):
    global passed, failed
    if condition:
        print(f"{GREEN}✅ PASS{RESET} - {name}")
        if response:
            print(f"       Status: {response.status_code} | Response: {response.json()}")
        passed += 1
    else:
        print(f"{RED}❌ FAIL{RESET} - {name}")
        if response:
            print(f"       Status: {response.status_code} | Response: {response.text}")
        failed += 1

print(f"\n{YELLOW}--- Testing GET /api/health ---{RESET}")
try:
    r = requests.get(f"{BASE_URL}/api/health")
    test("Status code is 200", r.status_code == 200, r)
    test("Response has 'status' field", "status" in r.json(), r)
    test("Status is 'ok'", r.json().get("status") == "ok", r)
    test("Response has 'timestamp' field", "timestamp" in r.json(), r)
except Exception as e:
    print(f"{RED}❌ Cannot connect to server: {e}{RESET}")
    print("Make sure app.py is running with: python app.py")
    exit(1)

print(f"\n{YELLOW}--- Testing POST /api/chat (valid) ---{RESET}")
r = requests.post(f"{BASE_URL}/api/chat", json={"prompt": "What is RAG?"})
test("Status code is 200", r.status_code == 200, r)
test("Response has 'response' field", "response" in r.json(), r)
test("Response has 'conversation_id'", "conversation_id" in r.json(), r)
test("Response is not empty", len(r.json().get("response", "")) > 0, r)
conversation_id = r.json().get("conversation_id")

print(f"\n{YELLOW}--- Testing POST /api/chat (error condition) ---{RESET}")
r = requests.post(f"{BASE_URL}/api/chat", json={})
test("Status code is 400 for missing prompt", r.status_code == 400, r)
test("Response has 'error' field", "error" in r.json(), r)

print(f"\n{YELLOW}--- Testing GET /api/history ---{RESET}")
r = requests.get(f"{BASE_URL}/api/history")
test("Status code is 200", r.status_code == 200, r)
test("Response has 'history' field", "history" in r.json(), r)
test("History is a list", isinstance(r.json().get("history"), list), r)
test("History has at least 1 entry", len(r.json().get("history", [])) >= 1, r)

print(f"\n{YELLOW}--- Testing GET /api/users ---{RESET}")
r = requests.get(f"{BASE_URL}/api/users")
test("Status code is 200", r.status_code == 200, r)
test("Response has 'users' field", "users" in r.json(), r)
test("Users is a list", isinstance(r.json().get("users"), list), r)
test("Users list is not empty", len(r.json().get("users", [])) > 0, r)

print(f"\n{YELLOW}--- Testing POST /api/feedback (valid) ---{RESET}")
r = requests.post(f"{BASE_URL}/api/feedback", json={
    "conversation_id": conversation_id,
    "rating": 5,
    "comment": "Very helpful answer!"
})
test("Status code is 201", r.status_code == 201, r)
test("Response has 'message' field", "message" in r.json(), r)
test("Response has 'feedback' field", "feedback" in r.json(), r)
test("Feedback stored message correct", r.json().get("message") == "Feedback stored", r)

print(f"\n{YELLOW}--- Testing POST /api/feedback (error condition) ---{RESET}")
r = requests.post(f"{BASE_URL}/api/feedback", json={"comment": "missing fields"})
test("Status code is 400 for missing fields", r.status_code == 400, r)
test("Response has 'error' field", "error" in r.json(), r)

total = passed + failed
print(f"\n{YELLOW}========== TEST SUMMARY =========={RESET}")
print(f"{GREEN}✅ Passed: {passed}/{total}{RESET}")
print(f"{RED}❌ Failed: {failed}/{total}{RESET}")
if failed == 0:
    print(f"{GREEN}🎉 All tests passed! Backend is working correctly.{RESET}")
else:
    print(f"{YELLOW}⚠️  Some tests failed. Check your app.py.{RESET}")
