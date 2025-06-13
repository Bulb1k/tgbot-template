from state import StartState
from texts import texts
from aiogram import types
from aiogram.fsm.context import FSMContext


async def greeting(message: types.Message, state: FSMContext):
    await message.answer(texts.start.GREETING)

