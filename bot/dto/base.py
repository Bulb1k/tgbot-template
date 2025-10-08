from pydantic import BaseModel


class BaseDto(BaseModel):
    def to_payload(self) -> dict:
        return self.model_dump(exclude_none=True)

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True
