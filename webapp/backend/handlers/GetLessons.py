from typing import Annotated

from fastapi.responses import JSONResponse
from fastapi import APIRouter, Cookie, status, HTTPException

import bot.database.requests as rq
from bot.database.models import Lesson
from bot.handlers.core import GetLessons as GetLessons_
from webapp.backend.handlers.auth import Cookies

router = APIRouter(prefix='api/', tags=['GetLessons'])


@router.get('/GetLessons', summary='Get lessons')
async def GetLessons(cookies: Annotated[Cookies, Cookie()]):
    data_lessons: list[Lesson] = await rq.GetLessons(cookies.UserID)
    lessons = []

    for lesson in data_lessons:
        lessons.append({
            'lesson_id': lesson.lesson_id,
            'lesson_name': await GetLessons_().GetName(lesson.lesson_id),
            'homework': lesson.homework,
            'photo': lesson.photo,
            'url': lesson.url
            })

    return JSONResponse(status_code=status.HTTP_200_OK, content=lessons)
