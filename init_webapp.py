from webapp.backend.server import server_start
from bot.config import __WEBAPP_HOST__, __WEBAPP_BACKEND_PORT__

server_start(__WEBAPP_HOST__, __WEBAPP_BACKEND_PORT__)
