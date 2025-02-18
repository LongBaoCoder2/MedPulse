from pydantic import BaseModel


class ConversationRenameRequest(BaseModel):
    title: str
