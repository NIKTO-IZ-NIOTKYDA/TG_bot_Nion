from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, HTTPException

import bot.database.requests as rq
from webapp.backend.netschoolapi.errors import AuthError
from webapp.backend.netschoolapi.netschoolapi import NetSchoolAPI
from bot.config import __API_NETSCHOOL__, __SCHOOL_NAME__, __DAIRY_DATE__
from webapp.backend.handlers.bodys.AddNetSchool import Body as BodyRQFromAddNetSchool


router = APIRouter(tags=['Auth'])


@router.post('/AddNetSchool')
async def InitFilters(body: BodyRQFromAddNetSchool):
    try:
        try:
            client = NetSchoolAPI(__API_NETSCHOOL__, 30)
            
            await client.login(body.Login, body.Password, __SCHOOL_NAME__)
            diary = await client.diary(__DAIRY_DATE__['start'], __DAIRY_DATE__['end'], json=True)

            await client.logout()
        except AuthError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        await rq.SetNetSchoolData(body.UserID, diary)

        await rq.SetNetSchool(
            body.UserID,
            body.Login,
            body.Password,
            body.Key
        )

        return JSONResponse(status_code=status.HTTP_200_OK, content={'status': 'success'})
    except Exception as Error:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f'UserID: {body.UserID} | Critical error: {Error}')
