from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
from uuid import uuid4

from llama_index.core.embeddings import BaseEmbedding
from llama_index.core.schema import NodeWithScore
from llama_index.core.vector_stores.types import VectorStore
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from qllm.core.config import settings
from qllm.models.model import Memory, MemoryIndex, MemoryType


class MemoryService:
    def __init__(
        self, db: AsyncSession, vector_store: VectorStore, embed_model: BaseEmbedding
    ):
        self.db = db
        self.vector_store = vector_store
        self.embed_model = embed_model

    async def add_memory(
        self,
        user_id: str,
        content: Dict[str, Any],
        memory_type: MemoryType,
        metadata: Optional[Dict] = None,
        importance_score: float = 0.0,
    ) -> Memory:
        """
        Thêm một memory mới cho user.
        """
        # Tạo embedding cho content
        text_content = str(content)  # Convert content to string for embedding
        embedding = await self.embed_model.aembed_query(text_content)

        # Tạo memory record
        memory = Memory(
            id=str(uuid4()),
            user_id=user_id,
            type=memory_type,
            content=content,
            metadata=metadata or {},
            embedding=embedding,
            importance_score=importance_score,
        )

        # Lưu vào database
        self.db.add(memory)
        await self.db.commit()

        # Lưu vào vector store
        self.vector_store.add(
            [text_content], [embedding], [{"memory_id": memory.id, "user_id": user_id}]
        )

        return memory

    async def query_memories(
        self,
        user_id: str,
        query: str,
        memory_type: Optional[MemoryType] = None,
        top_k: int = 5,
    ) -> List[NodeWithScore]:
        """
        Tìm kiếm các memories liên quan đến query.
        """
        # Tạo embedding cho query
        query_embedding = await self.embed_model.aembed_query(query)

        # Tìm kiếm trong vector store
        filter_dict = {"user_id": user_id}
        if memory_type:
            filter_dict["type"] = memory_type.value

        results = self.vector_store.similarity_search_with_score(
            query_embedding, k=top_k, filter=filter_dict
        )

        # Cập nhật last_accessed cho các memories được truy xuất
        for node in results:
            memory_id = node.metadata["memory_id"]
            stmt = select(Memory).where(Memory.id == memory_id)
            memory = (await self.db.execute(stmt)).scalar_one_or_none()
            if memory:
                memory.last_accessed = datetime.utcnow()

        await self.db.commit()

        return results

    async def update_memory_importance(self, memory_id: str, importance_delta: float):
        """
        Cập nhật điểm quan trọng của memory.
        """
        stmt = select(Memory).where(Memory.id == memory_id)
        memory = (await self.db.execute(stmt)).scalar_one_or_none()

        if memory:
            memory.importance_score += importance_delta
            await self.db.commit()

    async def forget_old_memories(
        self, user_id: str, threshold_days: int = 30, importance_threshold: float = 0.3
    ):
        """
        Xóa các memories cũ và ít quan trọng.
        """
        cutoff_date = datetime.utcnow() - timedelta(days=threshold_days)

        stmt = select(Memory).where(
            Memory.user_id == user_id,
            Memory.last_accessed < cutoff_date,
            Memory.importance_score < importance_threshold,
        )

        old_memories = (await self.db.execute(stmt)).scalars().all()

        # Xóa từ vector store và database
        for memory in old_memories:
            await self.db.delete(memory)
            self.vector_store.delete(filter={"memory_id": memory.id})

        await self.db.commit()
