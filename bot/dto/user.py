from .base import BaseDto

class UserDto(BaseDto):
    chat_id: int
    user_name: str
    first_name: str
