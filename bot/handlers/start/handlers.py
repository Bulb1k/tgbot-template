from http.client import responses

from dto import UserDto
from state import StartState
from texts import texts
from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove
from handlers.common.helper import open_menu
from services.http_client import HttpUser


async def greeting(message: types.Message, state: FSMContext):
    await message.answer(texts.start.GREETING, reply_markup=ReplyKeyboardRemove())

    response = await HttpUser.get(chat_id=message.chat.id)
    if response.status != 200:
        await HttpUser.create(UserDto(
            chat_id=message.chat.id,
            user_name=message.from_user.username,
            first_name=message.from_user.first_name)
        )

    await open_menu(state=state, message=message, msg_text=texts.asking.SEND_ME_MESSAGE)

