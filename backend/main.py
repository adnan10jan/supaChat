import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio

from mcp_agent import process_chat_query

load_dotenv()

app = FastAPI(title="SupaChat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory history cache
query_history = []

class ChatRequest(BaseModel):
    message: str

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.get("/api/history")
async def get_history():
    return {"history": query_history}

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response_data = await process_chat_query(request.message)
        
        # Save to history
        query_history.append({
            "message": request.message,
            "response": response_data["text"]
        })
        # Keep only last 20
        if len(query_history) > 20:
            query_history.pop(0)

        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
