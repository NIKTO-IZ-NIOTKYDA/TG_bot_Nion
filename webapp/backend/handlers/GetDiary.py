from datetime import date
from typing import Annotated
from xml.dom import NotFoundErr

from fastapi.responses import JSONResponse
from fastapi import APIRouter, Cookie, status, HTTPException

from webapp.backend.handlers.auth import Cookies
from webapp.backend.session_manager import SessionManager
from webapp.backend.netschoolapi.netschoolapi import NetSchoolAPI


router = APIRouter(tags=['Diary'])


@router.get('/GetDiary', summary='Get diary')
async def GetDiary(start: date, end: date, cookies: Annotated[Cookies, Cookie()]):
    if not await SessionManager.isSession(cookies.UserID): raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Вы не авторизованны')
    try: SessionNetSchool = await SessionManager.GetSession(cookies.UserID, cookies.SessionID)
    except NotFoundErr: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Сессия не найдена')

    try: return JSONResponse(status_code=status.HTTP_200_OK, content=await NetSchoolAPI.diary(SessionNetSchool, start, end, json=True))
    except Exception as Error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                   detail=f'UserID: {cookies.UserID} | SessionID: {cookies.SessionID} | Critical error: {Error}')
