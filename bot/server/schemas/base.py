from pydantic import BaseModel


class ResponseBase(BaseModel):
    status: str = "success"
