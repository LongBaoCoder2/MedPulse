from llama_index.core.llms import MessageRole
from pydantic import BaseModel


class Message(BaseModel):
    role: MessageRole
    content: str
