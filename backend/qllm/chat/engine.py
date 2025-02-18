import os
from datetime import UTC, datetime
from typing import AsyncGenerator, Dict, List, Optional

from llama_index.core.agent import ReActAgent
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.callbacks import CallbackManager
from llama_index.core.query_engine import SubQuestionQueryEngine
from llama_index.core.settings import Settings
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.vector_stores.types import VectorStore
from sqlalchemy.ext.asyncio import AsyncSession

from qllm.chat.index import IndexConfig, get_index
from qllm.chat.synthesizer import get_medical_response_synth
from qllm.chat.tools.pubmed_tool import get_tools as get_pubmed_tools
from qllm.models.model import Document as DocumentSchema
from qllm.prompts import PromptRegistry
from qllm.services.memory_service import MemoryService


class ChatEngine:
    def __init__(
        self,
        vector_store: Optional[VectorStore] = None,
        db: Optional[AsyncSession] = None,
        documents: Optional[List[DocumentSchema]] = None,
        filters=None,
        params=None,
        event_handlers=None,
    ):
        # Lấy system prompt từ registry
        self.system_prompt = PromptRegistry.get("system").format()
        self.TOP_K = int(os.getenv("TOP_K", "0"))

        # Khởi tạo các components
        self.callback_manager = CallbackManager(handlers=event_handlers)

        if db and vector_store:
            self.memory_service = MemoryService(
                db=db, vector_store=vector_store, embed_model=Settings.embed_model
            )

        # Khởi tạo response synthesizer
        # self.response_synth = get_medical_response_synth(documents or [])
        self.response_synth = get_medical_response_synth()

        # Khởi tạo vector store query engine
        vector_query_tools = []
        if vector_store is not None:
            index_config = IndexConfig(
                callback_managers=self.callback_manager, **(params or {})
            )
            index = get_index(vector_store, index_config)
            if index is not None:
                medical_records_engine = index.as_query_engine(
                    filters=filters,
                )
                vector_query_tools.append(
                    QueryEngineTool(
                        query_engine=medical_records_engine,
                        metadata=ToolMetadata(
                            name="medical_records",
                            description="Công cụ tìm kiếm trong hồ sơ y tế của bệnh nhân. Sử dụng khi cần tra cứu thông tin về bệnh án, kết quả xét nghiệm, và lịch sử điều trị.",
                        ),
                    )
                )

        # Khởi tạo PubMed tools
        pubmed_tools = get_pubmed_tools()

        # Tạo SubQuestionQueryEngine cho medical records
        self.medical_records_engine = SubQuestionQueryEngine.from_defaults(
            query_engine_tools=vector_query_tools,
            response_synthesizer=self.response_synth,
            verbose=True,
            use_async=True,
        )

        # Tạo SubQuestionQueryEngine cho PubMed
        self.pubmed_engine = SubQuestionQueryEngine.from_defaults(
            query_engine_tools=pubmed_tools,
            response_synthesizer=self.response_synth,
            verbose=True,
            use_async=True,
        )

        # Tạo top-level tools cho ReActAgent
        self.tools = [
            QueryEngineTool(
                query_engine=self.medical_records_engine,
                metadata=ToolMetadata(
                    name="medical_records_engine",
                    description="Công cụ truy vấn hồ sơ y tế. Sử dụng khi cần tìm kiếm thông tin từ hồ sơ bệnh án của bệnh nhân.",
                ),
            ),
            QueryEngineTool(
                query_engine=self.pubmed_engine,
                metadata=ToolMetadata(
                    name="pubmed_engine",
                    description="Công cụ tìm kiếm thông tin y khoa từ PubMed. Sử dụng khi cần tra cứu thông tin về bệnh lý, phương pháp điều trị, và nghiên cứu y học.",
                ),
            ),
        ]

        # Khởi tạo ReActAgent
        self.agent = ReActAgent.from_llm(
            llm=Settings.llm,
            tools=self.tools,
            callback_manager=self.callback_manager,
            system_prompt=self.system_prompt,
            verbose=True,
        )

    async def achat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
        user_id: Optional[str] = None,
    ):
        """
        Xử lý tin nhắn của người dùng với query transform và memory.
        """
        # Transform query thành các subqueries

        final_response = await self.agent.achat(message, chat_history)

        return final_response

    async def astream_chat(
        self,
        message: str,
        chat_history: Optional[List[ChatMessage]] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Phiên bản streaming của phương thức chat.
        Trả về một async generator để stream từng token của response.
        """
        response_stream = await self.agent.astream_chat(message, chat_history)

        async for response in response_stream.async_response_gen():
            yield response


def get_chat_engine(**kwargs):
    """
    Factory function để tạo ChatEngine.
    """
    return ChatEngine(**kwargs)
