from typing import List

from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.settings import Settings

from qllm.prompts import PromptRegistry


class QueryTransformer:
    def __init__(self):
        self.llm = Settings.llm
        self.prompt = PromptRegistry.get("query_transform")

    async def transform(
        self, query: str, chat_history: List[ChatMessage] = None
    ) -> List[str]:
        """
        Chuyển đổi câu hỏi gốc thành các câu hỏi phụ.

        Args:
            query: Câu hỏi gốc của người dùng
            chat_history: Lịch sử trò chuyện (tùy chọn)

        Returns:
            List[str]: Danh sách các câu hỏi phụ
        """
        chat_history_str = ""
        if chat_history:
            chat_history_str = "\n".join(
                [
                    f"{msg.role}: {msg.content}"
                    for msg in chat_history[-5:]  # Chỉ lấy 5 tin nhắn gần nhất
                ]
            )

        prompt_str = self.prompt.format(query=query, chat_history=chat_history_str)

        response = await self.llm.acomplete(prompt_str)

        # Xử lý kết quả để lấy các câu hỏi phụ
        subqueries = []
        for line in response.text.strip().split("\n"):
            if line and line[0].isdigit():
                # Loại bỏ số thứ tự và dấu chấm
                subquery = line.split(".", 1)[1].strip()
                # Loại bỏ dấu ngoặc vuông nếu có
                subquery = subquery.strip("[]")
                subqueries.append(subquery)

        return subqueries
