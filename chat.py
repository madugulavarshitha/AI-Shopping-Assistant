from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os

try:
    from agents.orchestrator import run_orchestrator
except ImportError:
    # Fallback if dependencies aren't loaded yet
    def run_orchestrator(query: str):
        return {"text": "I am a fallback AI. I heard: " + query, "products": []}

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    response: str
    recommended_products: List[dict] = []
    structured_data: Optional[dict] = None

@router.post("/", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    if not request.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
        
    try:
        # Run the LangGraph orchestrator
        result = run_orchestrator(request.message)
        return ChatResponse(
            response=result["text"],
            recommended_products=result["products"],
            structured_data=result.get("structured_data")
        )
    except Exception as e:
        print(f"AI Chat Error: {e}")
        # Fallback response so UI doesn't crash as requested by Master Prompt
        return ChatResponse(
            response="I'm sorry, my AI brain is currently taking a nap or experiencing an error. But you can still browse our categories!",
            recommended_products=[],
            structured_data=None
        )
