from typing import List, Optional

from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    user_id: Optional[str] = None
    message: str
    history: Optional[List[Message]] = None


class ChatResponse(BaseModel):
    response: str
    history: Optional[List[Message]] = None
    model_usage: Optional[dict] = None
    processing_time: Optional[float] = None
