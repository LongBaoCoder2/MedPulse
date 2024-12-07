from llama_index.core.settings import Settings

from qllm.core.config import settings as app_settings


def init_openai():
    from llama_index.core.constants import DEFAULT_TEMPERATURE
    from llama_index.embeddings.openai import OpenAIEmbedding
    from llama_index.llms.openai import OpenAI

    max_tokens = app_settings.LLM_MAX_TOKENS
    temperature = app_settings.LLM_TEMPERATURE
    Settings.llm = OpenAI(
        model=app_settings.LLM_OPENAI_MODEL,
        temperature=(
            float(temperature) if temperature is not None else DEFAULT_TEMPERATURE
        ),
        max_tokens=int(max_tokens) if max_tokens is not None else None,
    )

    dimensions = app_settings.EMBEDDING_DIM
    embedding_model = app_settings.EMBEDDING_MODEL
    Settings.embed_model = OpenAIEmbedding(
        model=embedding_model or "text-embedding-3-small",
        dimensions=int(dimensions) if dimensions is not None else None,
    )
