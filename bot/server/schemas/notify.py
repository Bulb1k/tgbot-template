from typing import Optional, List, Dict

from pydantic import BaseModel


class User(BaseModel):
    chat_id: int


class CustomNotify(BaseModel):
    text: Dict[str, str]
    users: List[User]
    parse_mode: Optional[str] = 'Markdown'


class NotifyResponse(BaseModel):
    status: str = "success"
    sent_to: List[int]
