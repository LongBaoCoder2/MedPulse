from typing import List

from llama_index.core.prompts.prompt_type import PromptType
from llama_index.core.prompts.prompts import QuestionAnswerPrompt, RefinePrompt
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.core.response_synthesizers.factory import get_response_synthesizer

from qllm.models.model import Document as DocumentSchema


# def get_medical_response_synth(documents: List[DocumentSchema]) -> BaseSynthesizer:
def get_medical_response_synth() -> BaseSynthesizer:
    # doc_titles = "\n".join("- " + doc.title for doc in documents)

    refine_template_str = f"""
Bạn là một trợ lý y tế AI đang phân tích các tài liệu y tế của bệnh nhân và thông tin từ PubMed. \
Các tài liệu y tế bao gồm:

Câu hỏi ban đầu là: {{query_str}}
Chúng ta đã có câu trả lời hiện tại: {{existing_answer}}

Dưới đây là thêm thông tin bổ sung:
------------
{{context_msg}}
------------

Dựa trên thông tin mới, hãy tinh chỉnh câu trả lời ban đầu để trả lời tốt hơn. \
Nếu thông tin không hữu ích, giữ nguyên câu trả lời ban đầu.

Câu trả lời tinh chỉnh:
""".strip()

    qa_template_str = f"""
Bạn là một trợ lý y tế AI đang phân tích các tài liệu y tế của bệnh nhân và thông tin từ PubMed. \
Các tài liệu y tế bao gồm:

Thông tin ngữ cảnh:
---------------------
{{context_str}}
---------------------

Dựa trên thông tin ngữ cảnh được cung cấp và không sử dụng kiến thức trước đó, \
hãy trả lời câu hỏi sau.

Câu hỏi: {{query_str}}
Câu trả lời:
""".strip()

    refine_prompt = RefinePrompt(
        template=refine_template_str,
        prompt_type=PromptType.REFINE,
    )

    qa_prompt = QuestionAnswerPrompt(
        template=qa_template_str,
        prompt_type=PromptType.QUESTION_ANSWER,
    )

    return get_response_synthesizer(
        refine_template=refine_prompt,
        text_qa_template=qa_prompt,
        structured_answer_filtering=False,
    )
