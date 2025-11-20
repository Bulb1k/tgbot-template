from aiogram.types import InlineKeyboardMarkup

from texts.keyboards import BACK
from .consts import InlineConstructor


def build_back_kb(callback_data: str) -> InlineKeyboardMarkup:
    return InlineConstructor.create_kb(
        actions=[{"text": BACK, "callback_data": callback_data}],
        schema=[1]
    )
