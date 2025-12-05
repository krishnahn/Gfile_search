"""
Simple test for the API
"""
import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

print("Waiting for server to start...")
time.sleep(2)

try:
    # Test 1: Health check
    print("\n1. Testing Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test 2: List stores
    print("\n2. Testing List Stores...")
    response = requests.get(f"{BASE_URL}/api/stores")
    print(f"   Status: {response.status_code}")
    data = response.json()
    print(f"   Found {data['count']} stores")
    
    # Test 3: Search
    print("\n3. Testing Search...")
    search_data = {
        "query": "What are the key findings from ICAR reports?",
        "store_name": "my-docs",
        "temperature": 0.0,
        "max_tokens": 1024
    }
    
    response = requests.post(f"{BASE_URL}/api/search", json=search_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n   ✅ SUCCESS!")
        print(f"   Answer: {result['answer'][:200]}...")
        print(f"   Citations: {len(result.get('citations', []))} sources")
        print(f"   Processing Time: {result['metadata'].get('processing_time', 0):.2f}s")
    else:
        print(f"   ❌ ERROR: {response.text}")
    
    print("\n✅ All tests completed!")
    
except requests.exceptions.ConnectionError:
    print("\n❌ Error: Could not connect to the API.")
    print("   Make sure the server is running: uvicorn api:app --reload")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
