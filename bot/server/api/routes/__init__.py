from fastapi import APIRouter

from server.api.routes.notify import router as notify_router
from server.api.routes.webhook import router as webhook_router

api_router = APIRouter()

api_router.include_router(prefix="/notify", router=notify_router)
