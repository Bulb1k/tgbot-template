from typing import Any

from dto.base import BaseDto


class ApiResponse(BaseDto):
    status: int
    data: Any | None = None
