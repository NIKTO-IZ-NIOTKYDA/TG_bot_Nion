SERVER_IP: str = '185.204.2.64'
SERVER_PORT: int = 5378
STRING: str = 'start-deploy'
CAMMAND_COPY: str = 'cd /home/server/TG_bot_Nion && mv photo /tmp/ && mv db/db.db /tmp/ && mv schedule.jpg /tmp/'
CAMMAND_UPDATE: str = 'cd /home/server/TG_bot_Nion && git checkout master && git pull'
CAMMAND_REMOVE: str ='cd /home/server/TG_bot_Nion && rm -rf photo && rm db/db.db && rm schedule.jpg'
CAMMAND_PASTE: str = 'cd /home/server/TG_bot_Nion && mv /tmp/photo/ . && mv /tmp/db.db db/db.db && mv /tmp/schedule.jpg .'
CAMMAND_RESTART: str = 'rm -rf /tmp/* && sudo systemctl restart TG_bot_Nion && sudo systemctl restart Deploy_tg_bot_nion'
