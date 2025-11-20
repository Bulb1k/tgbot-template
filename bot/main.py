from contextlib import asynccontextmanager

import uvicorn

from bot import bot, dp
from data.config import SERVER_ADDRESS, SERVER_HOST, SERVER_PORT, USE_NGROK, WEBHOOK_PATH
from data.logger_config import logger
from server.app import app
from setup import setup_aiogram
from utils.ngrok import get_ngrok_url


@asynccontextmanager
async def lifespan(app):
    logger.info("Configuring aiogram")
    await setup_aiogram(bot=bot, dp=dp)

    if USE_NGROK:
        public = await get_ngrok_url()
        webhook_url = f"{public}{WEBHOOK_PATH}"
    else:
        webhook_url = f"{SERVER_ADDRESS}{WEBHOOK_PATH}"

    logger.info("Webhook URL: %s", webhook_url)
    await bot.set_webhook(
        url=webhook_url,
        drop_pending_updates=True,
        allowed_updates=["message", "callback_query", "pre_checkout_query"]
    )
    logger.info("Configured aiogram")

    yield

    logger.info("Deleting webhook")
    await bot.delete_webhook()
    await bot.session.close()
    logger.info("Bot stopped")


if __name__ == "__main__":
    app.router.lifespan_context = lifespan
    uvicorn.run(
        app,
        host=SERVER_HOST,
        port=SERVER_PORT,
        reload=False,
        log_level="info",
    )
