import datetime
import json
import logging
from datetime import UTC, datetime, timezone
from typing import AsyncGenerator, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from llama_index.core.llms import ChatMessage
from llama_index.core.vector_stores.types import VectorStore
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from qllm.api.deps import get_db, get_qdrant_vector_store
from qllm.api.middlewares.jwt import CurrentUser
from qllm.api.schemas.conversation import ConversationRenameRequest
from qllm.api.schemas.message import ChatRequest, ChatResponse
from qllm.chat.engine import get_chat_engine
from qllm.models import model

logger = logging.getLogger("uvicorn")

conversation_route = r = APIRouter()


async def fetch_conversation(
    db: AsyncSession, conversation_id: str
) -> Optional[model.Conversation]:
    """
    Fetch a conversation
    return None if the conversation with the given id does not exist
    """
    stmt = select(model.Conversation).where(model.Conversation.id == conversation_id)

    result = await db.execute(stmt)
    conversation = result.scalars().first()
    return conversation


async def fetch_conversation_with_messages(
    db: AsyncSession, conversation_id: str
) -> Optional[model.Conversation]:
    """
    Fetch a conversation with its messages + messagesubprocesses
    return None if the conversation with the given id does not exist
    """
    # Eagerly load required relationships
    stmt = (
        select(model.Conversation)
        .options(
            joinedload(model.Conversation.messages).subqueryload(
                model.Message.sub_processes
            )
        )
        .options(
            joinedload(model.Conversation.conversation_document).subqueryload(
                model.ConversationDocument.document
            )
        )
        .where(model.Conversation.id == conversation_id)
    )

    result = await db.execute(stmt)
    conversation = result.scalars().first()

    return conversation


@r.get("")
async def get_all_conversation(
    current_user: CurrentUser, db: AsyncSession = Depends(get_db)
):
    stmt = select(model.Conversation).where(
        model.Conversation.user_id == current_user.id
    )
    conversation = await db.execute(stmt)
    return conversation.scalars().all()


@r.post("")
async def create_chat_conversation(
    current_user: CurrentUser, db: AsyncSession = Depends(get_db)
):
    conversation = model.Conversation()
    conversation.title = "New conversation"
    conversation.user_id = current_user.id

    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    return await fetch_conversation_with_messages(db, str(conversation.id))


@r.get("/{conversation_id}")
async def get_conversation(
    conversation_id: UUID, current_user: CurrentUser, db: AsyncSession = Depends(get_db)
):
    """Get all chat histories of a user."""
    conversations = await fetch_conversation_with_messages(db, str(conversation_id))

    if not conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")

    if conversations.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this conversation"
        )

    return conversations


@r.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: UUID, current_user: CurrentUser, db: AsyncSession = Depends(get_db)
):
    """Delete conversation."""
    conversation = await fetch_conversation(db, str(conversation_id))

    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation is not found.")

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Authorization Error. User doesn't have this permission.",
        )

    await db.delete(conversation)
    await db.commit()

    return {"message": "Delete conversation successfully."}


@r.patch("/{conversation_id}/rename")
async def rename_conversation(
    conversation_id: UUID,
    payload: ConversationRenameRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
):
    """Rename a conversation title."""
    # Lấy cuộc hội thoại từ database
    conversation = await fetch_conversation(db, str(conversation_id))

    # Kiểm tra xem cuộc hội thoại có tồn tại không
    if not conversation:
        raise HTTPException(status_code=404, detail="Cuộc hội thoại không tồn tại")

    # Kiểm tra quyền truy cập
    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Không có quyền đổi tên cuộc hội thoại này"
        )

    # Cập nhật tiêu đề
    conversation.title = payload.title
    await db.commit()
    await db.refresh(conversation)

    return conversation


@r.post("/{conversation_id}", response_model=ChatResponse)
async def chat_handler(
    conversation_id: UUID,
    payload: ChatRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    vector_store: VectorStore = Depends(get_qdrant_vector_store),
):
    logger.info("Get chat engine with Qdrant vector store")
    chat_engine = get_chat_engine(vector_store=vector_store)
    if chat_engine is None:
        raise HTTPException(status_code=500, detail="Chat Engine is not found.")

    conversation = await fetch_conversation_with_messages(db, str(conversation_id))

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this conversation"
        )

    histories = conversation.messages
    message = payload.message
    user_message = model.Message(
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None),
        conversation_id=conversation_id,
        content=message,
        role=model.MessageRoleEnum.USER,
        status=model.MessageStatusEnum.SUCCESS,
    )

    chat_history = []
    if histories:
        chat_history = [
            ChatMessage(role=message.role, content=message.content)
            for message in histories
        ]
    chat_response = await chat_engine.achat(message, chat_history)

    final_status = model.MessageStatusEnum.SUCCESS
    assis_message = model.Message(
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None),
        conversation_id=conversation_id,
        content=chat_response.response,
        role=model.MessageRoleEnum.ASSISTANT,
        status=final_status,
    )

    db.add(user_message)
    db.add(assis_message)
    await db.commit()

    # Construct the response
    response = ChatResponse(
        conversation_id=str(conversation_id),
        response=assis_message.content,
        history=chat_history,
    )
    return response


async def stream_chat_response(
    conversation_id: UUID,
    message: str,
    chat_response: AsyncGenerator,
    db: AsyncSession,
) -> AsyncGenerator[str, None]:
    """Stream the chat response and save messages to database"""
    user_message = model.Message(
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None),
        conversation_id=conversation_id,
        content=message,
        role=model.MessageRoleEnum.USER,
        status=model.MessageStatusEnum.SUCCESS,
    )

    assis_message = model.Message(
        created_at=datetime.now(timezone.utc).replace(tzinfo=None),
        updated_at=datetime.now(timezone.utc).replace(tzinfo=None),
        conversation_id=conversation_id,
        content="",
        role=model.MessageRoleEnum.ASSISTANT,
        status=model.MessageStatusEnum.PENDING,
    )

    db.add(user_message)
    db.add(assis_message)
    await db.commit()

    full_response = ""
    try:
        async for token in chat_response:
            full_response += token
            # Send token and space info as JSON
            response_data = {
                "p": token,
            }
            yield f"data: {json.dumps(response_data)}\n\n"

        assis_message.content = full_response
        assis_message.status = model.MessageStatusEnum.SUCCESS
        await db.commit()

        yield "data: [DONE]\n\n"
    except Exception as e:
        assis_message.status = model.MessageStatusEnum.ERROR
        await db.commit()
        yield f"data: Error: {str(e)}\n\n"


@r.post("/{conversation_id}/stream")
async def stream_chat_handler(
    conversation_id: UUID,
    payload: ChatRequest,
    current_user: CurrentUser,
    db: AsyncSession = Depends(get_db),
    vector_store: VectorStore = Depends(get_qdrant_vector_store),
):
    logger.info("Get chat engine with Qdrant vector store")
    chat_engine = get_chat_engine(vector_store=vector_store)
    if chat_engine is None:
        raise HTTPException(status_code=500, detail="Chat Engine is not found.")

    conversation = await fetch_conversation_with_messages(db, str(conversation_id))

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this conversation"
        )

    histories = conversation.messages
    message = payload.message

    chat_history = []
    if histories:
        chat_history = [
            ChatMessage(role=message.role, content=message.content)
            for message in histories
        ]

    # Lấy streaming response từ chat engine
    chat_response = chat_engine.astream_chat(message, chat_history)

    return StreamingResponse(
        stream_chat_response(conversation_id, payload.message, chat_response, db),
        media_type="text/event-stream",
    )
