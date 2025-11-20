from aiogram import types
from aiogram.fsm.context import FSMContext


async def main_handler(message: types.Message, state: FSMContext):
    bt_action = message.text
    data = await state.get_data()
