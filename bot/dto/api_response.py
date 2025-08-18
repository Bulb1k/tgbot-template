from typing import Optional, List

from dto import BaseDto


class ApiResponse(BaseDto):
    status: int
    data: List[BaseDto] | BaseDto = None
    message: str | None = None
