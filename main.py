from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from chatbot_strict import strict_chatbot
app = FastAPI()

@app.get("/")
async def root():
    return {"server status": "active"}

@app.get("/chatbot/response")
async def get_cb_response(input: str):
    print(input)
    return {"response": "hello"}

@app.get("/chatbot_strict/response")
async def get_cb_strict_response(query):
    return {"response": strict_chatbot(query)}