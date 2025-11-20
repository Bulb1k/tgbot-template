from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    data: Optional[T] = None
    status_code: int
    success: bool
    detail: Optional[str] = None
