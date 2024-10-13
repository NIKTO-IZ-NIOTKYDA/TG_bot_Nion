from base64 import b64decode
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, HTTPException

import bot.database.requests as rq
from webapp.backend.session_manager import SessionManager


router = APIRouter(tags=['Auth'])


class Cookies(BaseModel):
    UserID: int
    SessionID: str


@router.post('/login', summary='Login')
async def login(user_id: int, key: str):
    if await rq.GetUser(user_id) == AttributeError: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Пользователь не найден')

    try: key = b64decode(key)
    except Exception: raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='It was not possible to decode base64 in key')

    try: key = key.decode('UTF-8').replace('\n', '')
    except Exception: raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail='It was not possible to decode utf-8 in key')

    netschool = await rq.GetNetSchool(user_id)

    if netschool == AttributeError: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Интеграция с СГО не подключена')
    if netschool.enc_key != key: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Неправильный ключ шифрования')

    expire=datetime.now(timezone.utc) + timedelta(days=1)
    SessionID = await SessionManager.AddSession(user_id, expire, netschool)

    response = JSONResponse(status_code=status.HTTP_201_CREATED, content={'SessionID': SessionID})
    response.set_cookie(key='UserID', value=user_id, httponly=True, secure=False, expires=expire)
    response.set_cookie(key='SessionID', value=SessionID, httponly=True, secure=False, expires=expire)

    return response
