from telebot import types

# Start
markup_start = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
subject1 = types.KeyboardButton('1️⃣')
subject2 = types.KeyboardButton('2️⃣')
subject3 = types.KeyboardButton('3️⃣')
subject4 = types.KeyboardButton('4️⃣')
subject5 = types.KeyboardButton('5️⃣')
hastory = types.KeyboardButton('История (Конфуцианство в Китае)')
markup_start.add(subject1, subject2, subject3, subject4, subject5, hastory)


# Send date
# send nummer
markup_send_nummer = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
nummer = types.KeyboardButton(text='Send phone', request_contact=True)
markup_send_nummer.add(nummer)

# send geolocation
markup_send_geolocation = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
geolocation = types.KeyboardButton(text='Send geolocation', request_location=True)
markup_send_geolocation.add(geolocation)

# -=-=-=-=-=-=-=-=-=- Admin Panel -=-=-=-=-=-=-=-=-=- #

markup_admin_panel = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
# reboot = types.KeyboardButton('Перезагрузка 🔄')
backup_db = types.KeyboardButton('Бэкап базы данных 📑')
info = types.KeyboardButton('Статус сервера 🛠️')
markup_admin_panel.add(backup_db, info)  # *deleted reboot

# -=-=-=-=-=-=-=-=-=- End Admin Panel -=-=-=-=-=-=-=-=-=- #
