from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from lessons import Lessons
import database.requests as rq
from database.models import Lesson

router = APIRouter(tags=['GetLessons'])


@router.get('/GetLessons', summary='Get lessons')
async def GetLessons():
    data_lessons: list[Lesson] = await rq.GetLessons()
    lessons: list[dict[str | None, bytes | None]] = []

    for lesson in data_lessons:
        lessons.append({
            'lesson_id': lesson.lesson_id,
            'lesson_name': await Lessons.GetName(lesson.lesson_id),
            'homework': lesson.homework,
            'photo': lesson.photo,
            'url': lesson.url
            })

    return JSONResponse(status_code=status.HTTP_200_OK, content=lessons)
