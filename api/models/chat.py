from pydantic import BaseModel


class Chat(BaseModel):
    """db.models.Chat"""

    chat_id: int
    created_time: int
