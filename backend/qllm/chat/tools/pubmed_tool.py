from typing import List

from llama_index.core.base.response.schema import Response
from llama_index.core.query_engine.custom import CustomQueryEngine
from llama_index.core.schema import Document
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.readers.papers import PubmedReader
from pydantic import Field


class PubMedQueryEngine(CustomQueryEngine):
    """Custom query engine để tìm kiếm trên PubMed."""

    max_results: int = Field(
        default=2, description="Số lượng kết quả tối đa trả về từ PubMed"
    )

    def custom_query(self, query_str: str) -> Response:
        """
        Thực hiện tìm kiếm trên PubMed và trả về kết quả.

        Args:
            query_str (str): Câu truy vấn tìm kiếm

        Returns:
            Response: Kết quả tìm kiếm được định dạng
        """
        loader = PubmedReader()
        documents: List[Document] = loader.load_data(
            search_query=query_str, max_results=self.max_results
        )

        if not documents or len(documents) == 0:
            response_text = "Không tìm thấy bài báo nào phù hợp với từ khóa tìm kiếm."
        else:
            # Tạo response text từ documents
            response_text = ""
            for idx, doc in enumerate(documents, 1):
                extra_info = doc.extra_info
                max_length = min(100, len(doc.text))

                response_text += f"\nBài báo {idx}:\n"
                response_text += (
                    f"Tiêu đề: {extra_info.get('Title of this paper', 'N/A')}\n"
                )
                response_text += f"Tạp chí: {extra_info.get('Journal it was published in:', 'N/A')}\n"
                response_text += f"URL: {extra_info.get('URL', 'N/A')}\n"
                response_text += f"Nội dung:\n{doc.text[:max_length]}\n"
                response_text += "-" * 50 + "\n"

        return Response(response=response_text)


def get_tools() -> List[QueryEngineTool]:
    """
    Trả về danh sách các công cụ PubMed dưới dạng QueryEngineTool.
    """
    pubmed_engine = PubMedQueryEngine()

    return [
        QueryEngineTool(
            query_engine=pubmed_engine,
            metadata=ToolMetadata(
                name="pubmed_search",
                description="Tìm kiếm các bài báo khoa học y tế trên PubMed. Hữu ích khi cần tìm thông tin về các nghiên cứu y học, bệnh lý, điều trị, v.v.",
            ),
        )
    ]
