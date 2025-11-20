from aiogram import Router

from handlers import commands
from handlers.common.helper import Handler


def prepare_router() -> Router:
    router = Router()

    command_list = [

    ]

    for message in command_list:
        router.message.register(message.handler, *message.filters)

    return router
