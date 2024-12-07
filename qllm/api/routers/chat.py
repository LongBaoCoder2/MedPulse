from fastapi import APIRouter, HTTPException, status

from qllm.api.schema.chat import ChatRequest, ChatResponse, Message
from qllm.engine.engine import get_chat_engine

chat_router = APIRouter()


@chat_router.post("", response_model=ChatResponse)
async def chat_controller(chat_request: ChatRequest):
    chat_engine = get_chat_engine()
    if chat_engine is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cannot set up chat engine.",
        )

    message = chat_request.message
    history = chat_request.history or []
    chat_response = await chat_engine.achat(message, history)

    # Build the updated history including the assistant's response
    updated_history = history.append(
        Message(role="assistant", content=chat_response.response)
    )

    # Construct the response
    response = ChatResponse(
        response=chat_response.response,
        history=updated_history,
    )

    return response
