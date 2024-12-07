from typing import List

from fastapi import AppRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from qllm.api.deps import get_db
from qllm.models import model
from qllm.schemas import ChatConversationSchema, ChatHistorySchema

conversation_route = r = AppRouter()


@r.get("/chat_histories", response_model=List[ChatHistorySchema])
def get_chat_histories(user_id: str, db: Session = Depends(get_db)):
    """Get all chat histories of a user."""
    user = db.query(model.User).filter(model.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.chat_histories


@r.get(
    "/chat_histories/{history_id}/chat_conversation",
    response_model=ChatConversationSchema,
)
def get_chat_conversation(history_id: str, db: Session = Depends(get_db)):
    """Get a chat conversation for a specific chat history."""
    chat_history = (
        db.query(model.ChatHistory).filter(model.ChatHistory.id == history_id).first()
    )

    if not chat_history:
        raise HTTPException(status_code=404, detail="Chat history not found")

    if not chat_history.chat_conversation:
        raise HTTPException(status_code=404, detail="Chat conversation not found")

    return chat_history.chat_conversation
