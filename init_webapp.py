import webapp.backend.server as server
from bot.config import __WEBAPP_HOST__, __WEBAPP_BACKEND_PORT__

server.start(__WEBAPP_HOST__, __WEBAPP_BACKEND_PORT__)
