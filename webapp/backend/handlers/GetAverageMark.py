from datetime import date
from typing import Annotated, Literal

from fastapi.responses import JSONResponse
from fastapi import APIRouter, Cookie, status, HTTPException

from webapp.backend.handlers.auth import Cookies
from webapp.backend.session_manager import SessionManager
from webapp.backend.netschoolapi.netschoolapi import NetSchoolAPI
from webapp.backend.handlers.bodys.InitFilters import Body as BodyRQFromInitFilters


router = APIRouter(tags=['AverageMark'])

# async def GenAverageMark(user_id: int) -> dict:


@router.get('/InitFilters')
async def InitFilters(body: BodyRQFromInitFilters, cookies: Annotated[Cookies, Cookie()]):
    if not await SessionManager.isSession(cookies.UserID): raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Вы не авторизованны')

    try: SessionNetSchool = await SessionManager.GetSession(cookies.UserID, cookies.SessionID)
    except Exception: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Сессия не найдена')
    
    try:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=await SessionNetSchool.initfilters(class_data=body, json=True))
    except Exception as Error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                   detail=f'UserID: {cookies.UserID} | SessionID: {cookies.SessionID} | Critical error: {Error}')



@router.get('/GetInitDataAverageMark', summary='Get data to initialize the receipt of average assessments')
async def GetInitDataAverageMark(cookies: Annotated[Cookies, Cookie()]):
    if not await SessionManager.isSession(cookies.UserID): raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Вы не авторизованны')

    try: SessionNetSchool = await SessionManager.GetSession(cookies.UserID, cookies.SessionID)
    except NotFoundErr: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Сессия не найдена')

    try: return JSONResponse(status_code=status.HTTP_200_OK, content=await SessionNetSchool.params_average_mark(json=True))
    except Exception as Error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                   detail=f'UserID: {cookies.UserID} | SessionID: {cookies.SessionID} | Critical error: {Error}')


@router.get('/GetAverageMark', summary='Get average mark')
async def GetAverageMark(start: date, end: date, cookies: Annotated[Cookies, Cookie()]):
    if not await SessionManager.isSession(cookies.UserID): raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Вы не авторизованны')

    try: SessionNetSchool = await SessionManager.GetSession(cookies.UserID, cookies.SessionID)
    except NotFoundErr: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Сессия не найдена')

    try:
        diary_data = await NetSchoolAPI.diary(SessionNetSchool, start, end)
        return_data = list[dict[str, float, Literal[-1, 0, 1]]]


    except Exception as Error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                                   detail=f'UserID: {cookies.UserID} | SessionID: {cookies.SessionID} | Critical error: {Error}')
