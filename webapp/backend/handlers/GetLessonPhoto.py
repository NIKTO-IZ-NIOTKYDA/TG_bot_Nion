from os import open

from fastapi.responses import FileResponse
from fastapi import APIRouter, status, HTTPException

from bot.config import __SCHEDULE_PATH_FILE__

router = APIRouter(prefix='', tags=['GetLessonPhoto'])


@router.get('/GetLessonPhoto', summary='Get lesson photo')
async def GetLessonPhoto(lesson_id: str):
    try: open(path=f'bot/database/photo/{lesson_id}.png', flags=0)
    except FileNotFoundError: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='FileNotFoundError')

    file = FileResponse(path=f'bot/database/photo/{lesson_id}.png')
    return file
