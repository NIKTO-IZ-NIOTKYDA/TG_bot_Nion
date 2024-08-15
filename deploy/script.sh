cd /home/server/TG_bot_Nion && mv photo /tmp/ && mv db/db.db /tmp/ && mv schedule.jpg /tmp/
git checkout master && git pull -f
cd /home/server/TG_bot_Nion && rm -rf photo && rm /home/server/TG_bot_Nion/db/db.db && rm schedule.jpg
cd /home/server/TG_bot_Nion && mv /tmp/photo/ . && mv /tmp/db.db db/db.db && mv /tmp/schedule.jpg .
rm -rf /tmp/* 
cd /home/server/TG_bot_Nion && pip3 install -r requirements.txt
echo "tr1OyC8IzeDW2Vw340encWlmvdlVg3uS8vrZlSYXsdRsIGbUMiPwBS30rQtV7ynoMDMlKcVaPyCr0R0AFFYu4Rgkx57VSePlryPCCtI84nbUmPC6rXpbs22xEcBMc9i3fHKw7w1LTYKksd52a6C4ceqpNhcZ7zUHz4px9ySLuQz3JJjKEWNuRpNMgIhUG3hbGhWAdpVzpXmFughGi69LjC0g4sm9C0UQ0zArZSAYSxS7YTN70nrXbYhI3eiD34oU" | sudo --stdin systemctl restart TG_bot_Nion
exit 0