#!/bin/bash

cd ~/TG_bot_Nion/
systemctl stop TG_bot_Nion.service

cp -r ~/TG_bot_Nion/photo /tmp/
if [ -e ~/TG_bot_Nion/schedule.jpg ]
then
cp ~/TG_bot_Nion/schedule.jpg /tmp/
else
echo "pass" >> /dev/null
fi
cp ~/TG_bot_Nion/db/db.db /tmp/

rm -rf ~/TG_bot_Nion/*

git clone git@github.com:NIKTO-IZ-NEOTKYDA/TG_bot_Nion.git

rm -rf ~/TG_bot_Nion/TG_bot_Nion/photo
if [ -e ~/TG_bot_Nion/schedule.jpg ]
then
rm ~/TG_bot_Nion/TG_bot_Nion/schedule.jpg
else
echo "pass" >> /dev/null
fi
rm ~/TG_bot_Nion/TG_bot_Nion/db/db.db

mv ~/TG_bot_Nion/TG_bot_Nion/* ~/TG_bot_Nion/
rm -rf ~/TG_bot_Nion/TG_bot_Nion

mv /tmp/photo ~/TG_bot_Nion/
if [ -e /tmp/schedule.jpg ]
then
mv /tmp/schedule.jpg ~/TG_bot_Nion/
else
echo "pass" >> /dev/null
fi
mv /tmp/db.db ~/TG_bot_Nion/db/

systemctl start TG_bot_Nion.service
