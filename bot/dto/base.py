from pydantic import BaseModel, Field
from typing import Optional
from abc import ABC, abstractmethod
import aiohttp
import json
from data.config import API_BACKEND_URL, API_BACKEND_KEY


class BaseDto(BaseModel):
    def to_payload(self) -> dict:
        return self.model_dump(exclude_none=True)

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True
