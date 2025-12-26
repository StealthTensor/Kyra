import requests
import json

def test_chat():
    url = "http://localhost:8000/api/v1/chat/"
    payload = {
        "query": "What is the most urgent email?",
        "user_id": "feeb51d3-21f3-44ff-90f5-9860d8e27c49"
    }
    
    try:
        print(f"Sending request to {url}...")
        response = requests.post(url, json=payload, timeout=60)
        
        if response.status_code == 200:
            print("✅ Success!")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"❌ Failed: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        print("Make sure the backend is running!")

if __name__ == "__main__":
    test_chat()
