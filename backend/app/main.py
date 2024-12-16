import asyncio

import uvicorn
import nest_asyncio
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

import logging
from config import config
from lessons import Lessons
import database.requests as rq
import database.models as db_models

from handlers.GetLessons import router as GetLessons_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def start() -> None:
    await db_models.init_db()
    await rq.SyncLessons(Lessons.lessons)

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    api_router = APIRouter()
    api_router.include_router(GetLessons_router, tags=['lessons'])

    uvicorn.run(app=app, host='0.0.0.0', port=config.BACKEND_PORT)


if __name__ == 'main':
    loop = asyncio.get_event_loop()
    nest_asyncio.apply(loop)
    
    asyncio.run(start())