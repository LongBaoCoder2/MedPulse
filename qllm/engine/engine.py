import os
from typing import List

from llama_index.core.agent import AgentRunner
from llama_index.core.callbacks import CallbackManager
from llama_index.core.settings import Settings
from llama_index.core.tools import BaseTool, QueryEngineTool

from qllm.engine import ToolFactory
from qllm.engine.index import IndexConfig, get_index_from_disk


def get_chat_engine(filters=None, params=None, event_handlers=None, **kwargs):
    SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT")
    TOP_K = os.getenv("TOP_K", 0)
    tools: List[BaseTool] = []

    callback_manager = CallbackManager(handlers=event_handlers)
    index_config = IndexConfig(callback_managers=callback_manager, **(params or {}))
    index = get_index_from_disk(index_config)

    if index is not None:
        query_engine = index.as_query_engine(
            filters=filters, **{{"similiarity_top_k": TOP_K} if TOP_K != 0 else {}}
        )
        query_tool = QueryEngineTool.from_defaults(query_engine=query_engine)
        tools.append(query_tool)

    # Load configurated tools - config/tool.yaml
    configurated_tools = ToolFactory.from_env()
    tools.extend(configurated_tools)

    return AgentRunner.from_llm(
        llm=Settings.llm,
        tools=tools,
        callback_manager=callback_manager,
        system_prompt=SYSTEM_PROMPT,
        verbose=True,
    )
