from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove


from handlers.common.helper import open_menu
from texts import texts


async def greeting(message: types.Message, state: FSMContext):
    await message.answer(texts.start.GREETING, reply_markup=ReplyKeyboardRemove())

    await open_menu(state=state, message=message, msg_text=texts.asking.SEND_ME_MESSAGE)
