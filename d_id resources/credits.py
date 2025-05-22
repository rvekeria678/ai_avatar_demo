from dotenv import load_dotenv
import requests
import os

load_dotenv

DID_API_KEY = os.getenv("DID_API_KEY")


url = "https://api.d-id.com/credits"

headers = {
    "accept": "application/json",
    "authorization": f"Basic {DID_API_KEY}"
}

response = requests.get(url, headers = headers)

data = response.json()

print(f"Remaining Credits: {data['total']}")