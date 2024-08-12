cd /home/server/TG_bot_Nion && mv photo /tmp/ && mv db/db.db /tmp/ && mv schedule.jpg /tmp/
git checkout master && git pull -f
cd /home/server/TG_bot_Nion && rm -rf photo && rm /home/server/TG_bot_Nion/db/db.db && rm schedule.jpg
cd /home/server/TG_bot_Nion && mv /tmp/photo/ . && mv /tmp/db.db db/db.db && mv /tmp/schedule.jpg .
rm -rf /tmp/* && sudo systemctl restart TG_bot_Nion
exit 0