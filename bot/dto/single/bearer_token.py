from .. import BaseDto


class BearerTokenDto(BaseDto):
    token: str

    def to_payload(self) -> dict:
        return {
            "Authorization": f'Bearer {self.token}'
        }