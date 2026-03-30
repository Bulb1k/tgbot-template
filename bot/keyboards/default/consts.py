from typing import Sequence, Dict, Union
from aiogram.types import KeyboardButtonPollType
from aiogram_i18n import LazyProxy
from aiogram_i18n.types import ReplyKeyboardMarkup, KeyboardButton
from ..keyboard_utils import schema_generator


class DefaultConstructor:
    aliases = {
        "contact": "request_contact",
        "location": "request_location",
        "poll": "request_poll",
        "web": "web_app",
        "users": "request_users",
        "chat": "request_chat",
        "emoji": "icon_custom_emoji_id",
    }

    available_properties = [
        "text",
        "request_contact",
        "request_location",
        "request_poll",
        "request_users",
        "request_chat",
        "web_app",
        "icon_custom_emoji_id",
        "style",                
    ]

    @staticmethod
    def create_kb(
            actions: Sequence[str | LazyProxy | Dict[str, str | bool | KeyboardButtonPollType | LazyProxy]],
            schema: Sequence[int],
            resize_keyboard: bool = True,
            selective: bool = False,
            one_time_keyboard: bool = False,
            is_persistent: bool = True,
    ) -> ReplyKeyboardMarkup:
        buttons: list[KeyboardButton] = []

        for a in actions:
            if isinstance(a, (str, LazyProxy)):
                a = {"text": a}

            data: Dict[str, str | bool | KeyboardButtonPollType | LazyProxy] = {}

            for k, v in DefaultConstructor.aliases.items():
                if k in a:
                    a[v] = a[k]
                    del a[k]

            for k in a:
                if k in DefaultConstructor.available_properties:
                    data[k] = a[k]

            # Перевірка обов'язкового поля
            if "text" not in data:
                raise ValueError("Кнопка повинна мати поле 'text'")

            buttons.append(KeyboardButton(**data))

        kb = ReplyKeyboardMarkup(
            is_persistent=is_persistent,
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            selective=selective,
            keyboard=schema_generator.create_keyboard_layout(buttons, schema)
        )
        return kb
