import asyncio
import websockets
import json
import webbrowser
from dotenv import load_dotenv
import os

load_dotenv()

DID_API_KEY = os.getenv("DID_API_KEY")

print("Loaded API Key: ",DID_API_KEY)

async def run_did_live(script_text):
    url = f"wss://api.d-id.com/ws?api_key={DID_API_KEY}"

    async with websockets.connect(url) as ws:
        print("✅ Connected to D-ID WebSocket")

        # Example talk message
        message = {
            "type": "talk",
            "data": {
                "script": script_text,
                "voiceConfig": {
                    "gender": "female",
                    "language": "en-US"
                },
                "config": {
                    "driver_expressions": {
                        "expressions": {
                            "smile": 0.5
                        }
                    }
                }
            }
        }

        await ws.send(json.dumps(message))
        print("📨 Sent message to avatar:", script_text)

        while True:
            response = await ws.recv()
            data = json.loads(response)

            if data.get("type") == "stream-url":
                video_url = data.get("url")
                print("🎥 Avatar video URL:", video_url)
                webbrowser.open(video_url)
                break


# Example: Replace with your chatbot's response
bot_response = "Hi there, how are you?"

# Run it
asyncio.run(run_did_live(bot_response))