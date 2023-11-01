from telebot import types

# Start
markup_start = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
name = types.KeyboardButton('ℵ ПОКА ТУТ НИЧЕГО НЕТ ℵ')

markup_start.add(name)


# Send date
# send nummer
markup_send_nummer = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
nummer = types.KeyboardButton(text='Send phone', request_contact=True)
markup_send_nummer.add(nummer)

# -=-=-=-=-=-=-=-=-=- Admin Panel -=-=-=-=-=-=-=-=-=- #

markup_admin_panel = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
mailing = types.KeyboardButton('Рассылка✉️')
# reboot = types.KeyboardButton('Перезагрузка 🔄')
backup_db = types.KeyboardButton('Бэкап базы данных 📑')
info = types.KeyboardButton('Статус сервера 🛠️')
markup_admin_panel.add(mailing, backup_db, info)  # *deleted reboot

markup_chack_mailing = types.ReplyKeyboardMarkup(resize_keyboard=True)
yes = types.KeyboardButton('✅ YES ✅')
no = types.KeyboardButton('❌ NO ❌')
markup_chack_mailing.add(yes, no)

# -=-=-=-=-=-=-=-=-=- End Admin Panel -=-=-=-=-=-=-=-=-=- #
