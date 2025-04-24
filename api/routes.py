from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from src.chat_handler import Classification, client

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    content: str
    status_code: int

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint để tương tác với chat_with_google
    """
    try:
        # Khởi tạo Classification
        classification = Classification(client)
        
        # Gọi chat_with_google
        response = classification.chat_with_google(request.message)
        
        return ChatResponse(
            content=response.text,
            status_code=200
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 