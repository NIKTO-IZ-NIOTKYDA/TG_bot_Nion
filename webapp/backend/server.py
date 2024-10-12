import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bot.config import __WEBAPP_FRONTEND_PORT__

from webapp.backend.handlers.auth import router as login_router
from webapp.backend.handlers.GetDiary import router as GetDiary_router
from webapp.backend.handlers.GetLessons import router as GetLessons_router
from webapp.backend.handlers.GetLessonPhoto import router as GetLessonsPhoto_router
from webapp.backend.handlers.GetAverageMark import router as GetAverageMark_router

"""

/GetAverageMarks -> {
    lesson_name: str,
    value: float,
    status: int (-1, 0, 1)
}

"""


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        f'http://localhost:{__WEBAPP_FRONTEND_PORT__}',
        '*'
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


def server_start(host: str, port: int) -> None:
    app.include_router(login_router)
    app.include_router(GetDiary_router)
    app.include_router(GetLessons_router)
    app.include_router(GetLessonsPhoto_router)
    app.include_router(GetAverageMark_router)

    uvicorn.run(app=app, host=host, port=port)
