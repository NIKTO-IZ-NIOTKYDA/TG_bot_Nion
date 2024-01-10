from telebot import types

# Start
markup_start = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
DZ = types.KeyboardButton('Домашнее задание 📚')
schedule = types.KeyboardButton('Расписание 📑')
call_schedule = types.KeyboardButton('Расписание звонков 🕝')
markup_start.add(DZ, schedule, call_schedule)

# send nummer
markup_send_nummer = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
nummer = types.KeyboardButton(text='Отправить номер телефона', request_contact=True)
markup_send_nummer.add(nummer)

# DZ
markup_dz = types.InlineKeyboardMarkup()
algebra = types.InlineKeyboardButton(text='Алгебра', callback_data='algebra')
english_lang_1 = types.InlineKeyboardButton(text='Англ. Яз. (1 группа)', callback_data='english_lang_1')
english_lang_2 = types.InlineKeyboardButton(text='Англ. Яз. (2 группа)', callback_data='english_lang_2')
biology = types.InlineKeyboardButton(text='Биология', callback_data='biology')
geography = types.InlineKeyboardButton(text='География', callback_data='geography')
geometry = types.InlineKeyboardButton(text='Геометрия', callback_data='geometry')
computer_science_1 = types.InlineKeyboardButton(text='Информатика (1 группа)', callback_data='computer_science_1')
computer_science_2 = types.InlineKeyboardButton(text='Информатика (2 группа)', callback_data='computer_science_2')
story = types.InlineKeyboardButton(text='История', callback_data='story')
literature = types.InlineKeyboardButton(text='Литература', callback_data='literature')
music = types.InlineKeyboardButton(text='Музыка', callback_data='music')
OBZH = types.InlineKeyboardButton(text='ОБЖ', callback_data='OBZH')
social_science = types.InlineKeyboardButton(text='Обществознание', callback_data='social_science')
native_literature = types.InlineKeyboardButton(text='Родноя литература', callback_data='native_literature')
russian_lang = types.InlineKeyboardButton(text='Русский язык', callback_data='russian_lang')
TBIS = types.InlineKeyboardButton(text='Теория вероятностей и статистика', callback_data='TBIS')
technology = types.InlineKeyboardButton(text='Технология', callback_data='technology')
physics = types.InlineKeyboardButton(text='Физика', callback_data='physics')
chemistry = types.InlineKeyboardButton(text='Химия', callback_data='chemistry')
markup_dz.add(algebra, english_lang_1, english_lang_2, biology, geography, geometry, computer_science_1, computer_science_2, story, literature, music, OBZH, social_science, native_literature, russian_lang, TBIS, technology, physics, chemistry)

# DZ replace
markup_dz_update = types.InlineKeyboardMarkup()
algebra_update = types.InlineKeyboardButton(text='Алгебра (r)', callback_data='algebra_update')
english_lang_1_update = types.InlineKeyboardButton(text='Англ. Яз. (1 группа) (r)', callback_data='english_lang_1_update')
english_lang_2_update = types.InlineKeyboardButton(text='Англ. Яз. (2 группа) (r)', callback_data='english_lang_2_update')
biology_update = types.InlineKeyboardButton(text='Биология (r)', callback_data='biology_update')
geography_update = types.InlineKeyboardButton(text='География (r)', callback_data='geography_update')
geometry_update = types.InlineKeyboardButton(text='Геометрия (r)', callback_data='geometry_update')
computer_science_1_update = types.InlineKeyboardButton(text='Информатика (1 группа) (r)', callback_data='computer_science_1_update')
computer_science_2_update = types.InlineKeyboardButton(text='Информатика (2 группа) (r)', callback_data='computer_science_2_update')
story_update = types.InlineKeyboardButton(text='История (r)', callback_data='story_update')
literature_update = types.InlineKeyboardButton(text='Литература (r)', callback_data='literature_update')
music_update = types.InlineKeyboardButton(text='Музыка (r)', callback_data='music_update')
OBZH_update = types.InlineKeyboardButton(text='ОБЖ (r)', callback_data='OBZH_update')
social_science_update = types.InlineKeyboardButton(text='Обществознание (r)', callback_data='social_science_update')
native_literature_update = types.InlineKeyboardButton(text='Родноя литература (r)', callback_data='native_literature_update')
russian_lang_update = types.InlineKeyboardButton(text='Русский язык (r)', callback_data='russian_lang_update')
TBIS_update = types.InlineKeyboardButton(text='Теория вероятностей и статистика (r)', callback_data='TBIS_update')
technology_update = types.InlineKeyboardButton(text='Технология (r)', callback_data='technology_update')
physics_update = types.InlineKeyboardButton(text='Физика (r)', callback_data='physics_update')
chemistry_update = types.InlineKeyboardButton(text='Химия (r)', callback_data='chemistry_update')
markup_dz_update.add(algebra_update, english_lang_1_update, english_lang_2_update, biology_update, geography_update, geometry_update, computer_science_1_update, computer_science_2_update, story_update, literature_update, music_update, OBZH_update, social_science_update, native_literature_update, russian_lang_update, TBIS_update, technology_update, physics_update, chemistry_update)

# DZ and photo update
markup_dz_update_p = types.InlineKeyboardMarkup()
algebra_update_p = types.InlineKeyboardButton(text='Алгебра (rp)', callback_data='algebra_update_p')
english_lang_1_update_p = types.InlineKeyboardButton(text='Англ. Яз. (1 группа) (rp)', callback_data='english_lang_1_update_p')
english_lang_2_update_p = types.InlineKeyboardButton(text='Англ. Яз. (2 группа) (rp)', callback_data='english_lang_2_update_p')
biology_update_p = types.InlineKeyboardButton(text='Биология (rp)', callback_data='biology_update_p')
geography_update_p = types.InlineKeyboardButton(text='География (rp)', callback_data='geography_update_p')
geometry_update_p = types.InlineKeyboardButton(text='Геометрия (rp)', callback_data='geometry_update_p')
computer_science_1_update_p = types.InlineKeyboardButton(text='Информатика (1 группа) (rp)', callback_data='computer_science_1_update_p')
computer_science_2_update_p = types.InlineKeyboardButton(text='Информатика (2 группа) (rp)', callback_data='computer_science_2_update_p')
story_update_p = types.InlineKeyboardButton(text='История (rp)', callback_data='story_update_p')
literature_update_p = types.InlineKeyboardButton(text='Литература (rp)', callback_data='literature_update_p')
music_update_p = types.InlineKeyboardButton(text='Музыка (rp)', callback_data='music_update_p')
OBZH_update_p = types.InlineKeyboardButton(text='ОБЖ (rp)', callback_data='OBZH_update_p')
social_science_update_p = types.InlineKeyboardButton(text='Обществознание (rp)', callback_data='social_science_update_p')
native_literature_update_p = types.InlineKeyboardButton(text='Родноя литература (rp)', callback_data='native_literature_update_p')
russian_lang_update_p = types.InlineKeyboardButton(text='Русский язык (rp)', callback_data='russian_lang_update_p')
TBIS_update_p = types.InlineKeyboardButton(text='Теория вероятностей и статистика (rp)', callback_data='TBIS_update_p')
technology_update_p = types.InlineKeyboardButton(text='Технология (rp)', callback_data='technology_update_p')
physics_update_p = types.InlineKeyboardButton(text='Физика (rp)', callback_data='physics_update_p')
chemistry_update_p = types.InlineKeyboardButton(text='Химия (rp)', callback_data='chemistry_update_p')
markup_dz_update_p.add(algebra_update_p, english_lang_1_update_p, english_lang_2_update_p, biology_update_p, geography_update_p, geometry_update_p, computer_science_1_update_p, computer_science_2_update_p, story_update_p, literature_update_p, music_update_p, OBZH_update_p, social_science_update_p, native_literature_update_p, russian_lang_update_p, TBIS_update_p, technology_update_p, physics_update_p, chemistry_update_p)

# URL
markup_url = types.InlineKeyboardMarkup()
algebra_url = types.InlineKeyboardButton(text='Алгебра (u)', callback_data='algebra_url')
english_lang_1_url = types.InlineKeyboardButton(text='Англ. Яз. (1 группа) (u)', callback_data='english_lang_1_url')
english_lang_2_url = types.InlineKeyboardButton(text='Англ. Яз. (2 группа) (u)', callback_data='english_lang_2_url')
biology_url = types.InlineKeyboardButton(text='Биология (u)', callback_data='biology_url')
geography_url = types.InlineKeyboardButton(text='География (u)', callback_data='geography_url')
geometry_url = types.InlineKeyboardButton(text='Геометрия (u)', callback_data='geometry_url')
computer_science_1_url = types.InlineKeyboardButton(text='Информатика (1 группа) (u)', callback_data='computer_science_1_url')
computer_science_2_url = types.InlineKeyboardButton(text='Информатика (2 группа) (u)', callback_data='computer_science_2_url')
story_url = types.InlineKeyboardButton(text='История (u)', callback_data='story_url')
literature_url = types.InlineKeyboardButton(text='Литература (u)', callback_data='literature_url')
music_url = types.InlineKeyboardButton(text='Музыка (u)', callback_data='music_url')
OBZH_url = types.InlineKeyboardButton(text='ОБЖ (u)', callback_data='OBZH_url')
social_science_url = types.InlineKeyboardButton(text='Обществознание (u)', callback_data='social_science_url')
native_literature_url = types.InlineKeyboardButton(text='Родноя литература (u)', callback_data='native_literature_url')
russian_lang_url = types.InlineKeyboardButton(text='Русский язык (u)', callback_data='russian_lang_url')
TBIS_url = types.InlineKeyboardButton(text='Теория вероятностей и статистика (u)', callback_data='TBIS_url')
technology_url = types.InlineKeyboardButton(text='Технология (u)', callback_data='technology_url')
physics_url = types.InlineKeyboardButton(text='Физика (u)', callback_data='physics_url')
chemistry_url = types.InlineKeyboardButton(text='Химия (u)', callback_data='chemistry_url')
markup_url.add(algebra_url, english_lang_1_url, english_lang_2_url, biology_url, geography_url, geometry_url, computer_science_1_url, computer_science_2_url, story_url, literature_url, music_url, OBZH_url, social_science_url, native_literature_url, russian_lang_url, TBIS_url, technology_url, physics_url, chemistry_url)


# -=-=-=-=-=-=-=-=-=- Admin Panel -=-=-=-=-=-=-=-=-=- #

markup_admin_panel = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
mailing = types.KeyboardButton('Рассылка✉️')
reboot = types.KeyboardButton('Перезагрузка 🔄')
backup_db = types.KeyboardButton('Бэкап базы данных 📑')
info = types.KeyboardButton('Статус сервера 🛠️')
markup_admin_panel.add(mailing, reboot, backup_db, info)

markup_chack_mailing = types.ReplyKeyboardMarkup(resize_keyboard=True)
yes = types.KeyboardButton('✅ YES ✅')
no = types.KeyboardButton('❌ NO ❌')
markup_chack_mailing.add(yes, no)

markup_update_dz_or_gdz = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
dz = types.KeyboardButton(text='Д/3')
gdz = types.KeyboardButton(text='ГДЗ')
markup_update_dz_or_gdz.add(dz, gdz)

markup_photo = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
schedule = types.KeyboardButton(text='Расписание')
dz = types.KeyboardButton(text='Д/З')
back_photo = types.KeyboardButton(text='⬅️ Назад')
markup_photo.add(schedule, dz, back_photo)

# -=-=-=-=-=-=-=-=-=- End Admin Panel -=-=-=-=-=-=-=-=-=- #
