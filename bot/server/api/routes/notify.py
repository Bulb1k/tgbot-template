from fastapi import APIRouter

from fastapi import APIRouter

from bot import bot
from server.schemas import (
    NotifyResponse,
    CustomNotify,
)

router = APIRouter()


@router.post("/custom", response_model=NotifyResponse)
async def mass_send_message(request: CustomNotify):
    success_ids = []
    for users in request.users:
        try:
            text = request.text.get(users.language) if request.text.get(users.language) else request.text.get('en')
            await bot.send_message(chat_id=users.chat_id, text=text, parse_mode=request.parse_mode)
            success_ids.append(users.chat_id)
        except Exception as e:
            pass

    return NotifyResponse(sent_to=success_ids, status="success")
