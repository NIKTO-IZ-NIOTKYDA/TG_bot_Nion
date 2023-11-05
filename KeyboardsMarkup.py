from telebot import types

# Start
markup_start = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
DZ = types.KeyboardButton('Домашнее задание 📚')
schedule = types.KeyboardButton('Расписание 📑')
call_schedule = types.KeyboardButton('Расписание звонков 🕝')
markup_start.add(DZ, schedule, call_schedule)

# DZ
markup_dz = types.InlineKeyboardMarkup()
russian_lang = types.InlineKeyboardButton(text='Русский язык', callback_data='russian_lang')
literature = types.InlineKeyboardButton(text='Литература', callback_data='literature')
native_literature = types.InlineKeyboardButton(text='Родноя литература', callback_data='native_literature')
english_lang_1 = types.InlineKeyboardButton(text='Иностранный язык (1 группа)', callback_data='english_lang_1')
english_lang_2 = types.InlineKeyboardButton(text='Иностранный язык (2 группа)', callback_data='english_lang_2')
algebra = types.InlineKeyboardButton(text='Алгебра', callback_data='algebra')
geometry = types.InlineKeyboardButton(text='Геометрия', callback_data='geometry')
TBIS = types.InlineKeyboardButton(text='Теория вероятностей и статистика', callback_data='TBIS')
computer_science = types.InlineKeyboardButton(text='Информатика', callback_data='computer_science')
story = types.InlineKeyboardButton(text='История', callback_data='story')
social_science = types.InlineKeyboardButton(text='Обществознание', callback_data='social_science')
geography = types.InlineKeyboardButton(text='География', callback_data='geography')
physics = types.InlineKeyboardButton(text='Физика', callback_data='physics')
chemistry = types.InlineKeyboardButton(text='Химия', callback_data='chemistry')
biology = types.InlineKeyboardButton(text='Биология', callback_data='biology')
music = types.InlineKeyboardButton(text='Музыка', callback_data='music')
technology = types.InlineKeyboardButton(text='Технология', callback_data='technology')
OBZH = types.InlineKeyboardButton(text='ОБЖ', callback_data='OBZH')
markup_dz.add(russian_lang, literature, native_literature, english_lang_1, english_lang_2, algebra, geometry, TBIS, computer_science, story, social_science, geography, physics, chemistry, biology, music, technology, OBZH)

# DZ update
markup_dz_update = types.InlineKeyboardMarkup()
russian_lang_update = types.InlineKeyboardButton(text='Русский язык (r)', callback_data='russian_lang_update')
literature_update = types.InlineKeyboardButton(text='Литература (r)', callback_data='literature_update')
native_literature_update = types.InlineKeyboardButton(text='Родноя литература (r)', callback_data='native_literature_update')
english_lang_1_update = types.InlineKeyboardButton(text='Иностранный язык (1 группа) (r)', callback_data='english_lang_1_update')
english_lang_2_update = types.InlineKeyboardButton(text='Иностранный язык (2 группа) (r)', callback_data='english_lang_2_update')
algebra_update = types.InlineKeyboardButton(text='Алгебра (r)', callback_data='algebra_update')
geometry_update = types.InlineKeyboardButton(text='Геометрия (r)', callback_data='geometry_update')
TBIS_update = types.InlineKeyboardButton(text='Теория вероятностей и статистика (r)', callback_data='TBIS_update')
computer_science_update = types.InlineKeyboardButton(text='Информатика (r)', callback_data='computer_science_update')
story_update = types.InlineKeyboardButton(text='История (r)', callback_data='story_update')
social_science_update = types.InlineKeyboardButton(text='Обществознание (r)', callback_data='social_science_update')
geography_update = types.InlineKeyboardButton(text='География (r)', callback_data='geography_update')
physics_update = types.InlineKeyboardButton(text='Физика (r)', callback_data='physics_update')
chemistry_update = types.InlineKeyboardButton(text='Химия (r)', callback_data='chemistry_update')
biology_update = types.InlineKeyboardButton(text='Биология (r)', callback_data='biology_update')
music_update = types.InlineKeyboardButton(text='Музыка (r)', callback_data='music_update')
technology_update = types.InlineKeyboardButton(text='Технология (r)', callback_data='technology_update')
OBZH_update = types.InlineKeyboardButton(text='ОБЖ (r)', callback_data='OBZH_update')
markup_dz_update.add(russian_lang_update, literature_update, native_literature_update, english_lang_1_update, english_lang_2_update, algebra_update, geometry_update, TBIS_update, computer_science_update, story_update, social_science_update, geography_update, physics_update, chemistry_update, biology_update, music_update, technology_update, OBZH_update)


# Send date
# send nummer
markup_send_nummer = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
nummer = types.KeyboardButton(text='Send phone', request_contact=True)
markup_send_nummer.add(nummer)

# -=-=-=-=-=-=-=-=-=- Admin Panel -=-=-=-=-=-=-=-=-=- #

markup_admin_panel = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
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
