import requests
import json

url = "http://localhost:11434/api/generate"

data = {
    "model": "llama3",
    "prompt": "Why is the sky blue?",
    "stream": False
}

print(f"Testing Ollama at {url}...")
try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Failed: {e}")
