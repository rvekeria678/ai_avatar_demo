import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("DID_API_KEY")

headers = {
    'Authorization': f'Basic {api_key}',
    'Content-Type': 'application/json'
}

data = {
    "source_url": "https://create-images.d-id.com/avatars/amy.jpg",  # Avatar image
    "script": {
        "type": "text",
        "input": "Hello, welcome to our demo!"
    }
}

response = requests.post('https://api.d-id.com/talks', headers=headers, json=data)
print(response.json())
print(response.status_code)