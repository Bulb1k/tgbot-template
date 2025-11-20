from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey

from bot import bot, dp


async def get_user_state_data(chat_id: int, user_id: Optional[int] = None) -> dict:
    try:
        storage = dp.storage

        key = StorageKey(
            bot_id=bot.id,
            chat_id=chat_id,
            user_id=user_id or chat_id
        )

        state = FSMContext(storage=storage, key=key)
        state_data = await state.get_data()

        return state_data
    except Exception as e:
        print(f"Error getting state data: {e}")
        return {}


async def get_user_state(chat_id: int, user_id: Optional[int] = None) -> FSMContext:
    storage = dp.storage

    key = StorageKey(
        bot_id=bot.id,
        chat_id=chat_id,
        user_id=user_id or chat_id
    )

    return FSMContext(storage=storage, key=key)
