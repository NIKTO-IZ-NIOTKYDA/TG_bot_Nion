import logging

import uvicorn
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from bot.config import __WEBAPP_FRONTEND_PORT__
from webapp.backend.handlers.auth import router as login_router
from webapp.backend.handlers.GetDiary import router as GetDiary_router
from webapp.backend.handlers.GetLessons import router as GetLessons_router
from webapp.backend.handlers.AddNetSchool import router as AddNetSchool_router
from webapp.backend.handlers.GetLessonPhoto import router as GetLessonsPhoto_router
from webapp.backend.handlers.GetAverageMark import router as GetAverageMark_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start(host: str, port: int) -> None:
    app = FastAPI()


    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            f'http://localhost:{__WEBAPP_FRONTEND_PORT__}',
            '*'
        ],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )

    api_router = APIRouter()
    api_router.include_router(login_router, tags=['login'])
    api_router.include_router(GetDiary_router, tags=['diary'])
    api_router.include_router(GetLessons_router, tags=['lessons'])
    api_router.include_router(GetLessonsPhoto_router, tags=['lessons'])
    api_router.include_router(GetAverageMark_router, tags=['mark'])
    api_router.include_router(AddNetSchool_router, tags=['netschool'])

    uvicorn.run(app=app, host=host, port=port)
