import bot.config as config
from webapp.backend.server import server_start  # noqa: F401

server_start(config.__HOST__, config.port, config.__DEBUGGING__)
