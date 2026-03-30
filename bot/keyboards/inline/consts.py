from typing import Type, TypeVar

from aiogram.filters.callback_data import CallbackData
from aiogram.types import LoginUrl
from aiogram_i18n import LazyProxy
from aiogram_i18n.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from ..keyboard_utils import schema_generator

A = TypeVar("A", bound=Type[CallbackData])


class InlineConstructor:
    aliases = {"cb": "callback_data"}

    available_properties = [
        "text",
        "callback_data",
        "url",
        "login_url",
        "switch_inline_query",
        "switch_inline_query_current_chat",
        "callback_game",
        "pay",
        "web_app",
        "icon_custom_emoji_id",
        "style",
    ]

    @staticmethod
    def create_kb(
            actions: list[dict[str, str | bool | A | LoginUrl | LazyProxy]],
            schema: list[int],
    ) -> InlineKeyboardMarkup:
        buttons: list[InlineKeyboardButton] = []

        for a in actions:
            data: dict[str, str | bool | A | LoginUrl | LazyProxy] = {}

            for k, v in InlineConstructor.aliases.items():
                if k in a:
                    a[v] = a[k]
                    del a[k]

            for k in a:
                if k in InlineConstructor.available_properties:
                    data[k] = a[k]

            if "text" not in data:
                raise ValueError("Кнопка повинна мати поле 'text'")

            has_action = any(k in data for k in [
                "callback_data", "url", "login_url",
                "switch_inline_query", "switch_inline_query_current_chat",
                "callback_game", "pay", "web_app"
            ])
            if not has_action:
                raise ValueError("Кнопка повинна мати хоча б одну дію (callback_data, url, тощо)")

            if "callback_data" in data:
                if isinstance(data["callback_data"], CallbackData):
                    data["callback_data"] = data["callback_data"].pack()

            buttons.append(InlineKeyboardButton(**data))

        kb = InlineKeyboardMarkup(
            inline_keyboard=schema_generator.create_keyboard_layout(buttons, schema)
        )
        return kb
