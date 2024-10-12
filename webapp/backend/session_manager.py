from datetime import datetime
from xml.dom import NotFoundErr

from jose.jwt import encode as jwt_encode

import bot.logging.colors as colors
from bot.logging.logging import logging
from bot.database.models import NetSchool
import webapp.backend.netschoolapi.NetSchoolAPI as NetSchoolAPI
from webapp.backend.netschoolapi.netschoolapi import NetSchoolAPI_
from bot.config import __WEBAPP_SECRET_KEY__, __WEBAPP_ALGORITHM__, __API_NETSCHOOL__, __SCHOOL_NAME__


class Session_:
    UserID: int = None
    SessionID: str = None
    Session: NetSchoolAPI_ = None
    Expire: datetime = None

    def __init__(self, UserID: int, SessionID: str, Session: NetSchoolAPI_, Expire: datetime) -> None:
        self.UserID = UserID
        self.SessionID = SessionID
        self.Session = Session
        self.Expire = Expire


class SessionManager_:
    log = logging(Name='SM', Color=colors.blue)
    sessions: list[Session_] = []


    async def __CreateSessionID(self, UserID: int) -> str:
        return jwt_encode({'data': UserID}, key=__WEBAPP_SECRET_KEY__, algorithm=__WEBAPP_ALGORITHM__)


    async def AddSession(self, UserID: int, Expire: datetime, NetSchool: NetSchool) -> str:
        self.log.info(str(UserID), 'Adding new session')

        SessionID = await self.__CreateSessionID(UserID)

        Session = await NetSchoolAPI.create_client(__API_NETSCHOOL__, 60)
        await NetSchoolAPI.login(Session, NetSchool.enc_login, NetSchool.enc_password, __SCHOOL_NAME__)

        self.sessions.append(
            Session_(
                UserID,
                SessionID,
                Session,
                Expire
            )
        )
    
        return SessionID


    async def isSession(self, UserID: int) -> bool:
        self.log.info(str(UserID), 'Checking isSession')

        for session in self.sessions:
            if session.UserID == UserID: return True

        return False


    async def GetSession(self, UserID: int, SessionID: str) -> NetSchoolAPI_ | NotFoundErr:
        self.log.info(str(UserID), 'Getting session')

        for session in self.sessions:
            if session.UserID == UserID and session.SessionID == SessionID: return session.Session

        raise NotFoundErr()


    async def DeleteSession(self, UserID: int, SessionID: str) -> None:
        self.log.info(str(UserID), 'Deleting session')

        for session in self.sessions:
            if session.SessionID == SessionID:
                self.sessions.remove(session)


SessionManager = SessionManager_()
