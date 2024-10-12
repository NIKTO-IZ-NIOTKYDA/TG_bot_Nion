from aiogram import Router

from bot.lessons import Lessons
import bot.logging.logging as logging
import bot.logging.colors as colors

lessons: Lessons = Lessons()
router = Router(name=__name__)
admin_router = Router(name=__name__)
log = logging.logging(Name='HANDLER', Color=colors.green)


def GetRouter() -> Router: return router


def GetLessons() -> Lessons: return lessons
