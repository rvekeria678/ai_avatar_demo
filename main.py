from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from astronomy_agent import astronomy_agent_response

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"server status": "active"}

@app.get("/chatbot/response")
async def get_cb_response(input: str):
    print(input)
    return {"response": "hello"}

@app.get("/chatbot_strict/response")
async def get_cb_strict_response(query):
    return {"response": astronomy_agent_response(query)}