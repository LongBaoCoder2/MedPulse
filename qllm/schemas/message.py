from typing import List, Optional

from llama_index.core.llms import ChatMessage
from pydantic import BaseModel


class ChatConversationSchema(BaseModel):
    id: str
    chat_history_id: str
    messages: List[ChatMessage]

    class Config:
        orm_mode = True


class ChatHistorySchema(BaseModel):
    id: str
    user_id: str
    title: str
    chat_conversation: Optional[ChatConversationSchema] = None

    class Config:
        orm_mode = True
