from aiogram import Router
from aiogram.filters import CommandStart

from handlers.common.helper import Handler
from handlers.start import handlers


def prepare_router() -> Router:
    router = Router()

    message_list = [
        Handler(handlers.greeting, [CommandStart()]),
    ]

    callback_list = [
    ]

    for message in message_list:
        router.message.register(message.handler, *message.filters)

    for callback in callback_list:
        router.callback_query.register(callback.handler, *callback.filters)

    return router
