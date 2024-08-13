from telebot import types

# Start
markup_start = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
DZ = types.KeyboardButton('Домашнее задание 📚')
schedule = types.KeyboardButton('Расписание 📑')
call_schedule = types.KeyboardButton('Расписание звонков 🕝')
profile = types.KeyboardButton('Профиль 👤')
markup_start.add(DZ, schedule, call_schedule, profile)

# Warn off notifications
markup_off_notifications_warn = types.InlineKeyboardMarkup(row_width=1)
off_notifications_warn = types.InlineKeyboardButton(text='Да, я хочу отключить уведомления', callback_data='off_notifications')
no_off_notifications_warn = types.InlineKeyboardButton(text='Нет, я хочу оставить уведомления', callback_data='no_off_notifications')
markup_off_notifications_warn.add(off_notifications_warn, no_off_notifications_warn)

# Del schedule
markup_del_schedule = types.InlineKeyboardMarkup()
del_schedule_button = types.InlineKeyboardButton(text='❌ Удалить ❌', callback_data='schedule_del_warn')
markup_del_schedule.add(del_schedule_button)

# Warn del schedule
markup_del_schedule_warn = types.InlineKeyboardMarkup()
yes = types.InlineKeyboardButton(text='✅ Да ✅', callback_data='schedule_del')
no = types.InlineKeyboardButton(text='❌ Нет ❌', callback_data='schedule_del_no')
markup_del_schedule_warn.add(yes, no)

num_lessons: int = 19
dect_name_lessons: dict[int | list[str]] = {
    0: ['algebra', 'Алгебра'],
    1: ['english_lang_1', 'Англ. Яз. (1 группа)'],
    2: ['english_lang_2', 'Англ. Яз. (2 группа)'],
    3: ['biology', 'Биология'],
    4: ['geography', 'География'],
    5: ['geometry', 'Геометрия'],
    6: ['computer_science_1', 'Информатика (1 группа)'],
    7: ['computer_science_2', 'Информатика (2 группа)'],
    8: ['story', 'История'],
    9: ['literature', 'Литература'],
    10: ['music', 'Музыка'],
    11: ['OBZH', 'ОБЖ'],
    12: ['social_science', 'Обществознание'],
    13: ['native_literature', 'Родная литература'],
    14: ['russian_lang', 'Русский язык'],
    15: ['TBIS', 'Теория вероятностей и статистика'],
    16: ['technology', 'Технология'],
    17: ['physics', 'Физика'],
    18: ['chemistry', 'Химия'],
}

def gen_dz_markup(pstr_t: str, pstr_cbd: str) -> types.InlineKeyboardMarkup:
    r_markup = types.InlineKeyboardMarkup(row_width=3)

    i: int = 0
    while i < num_lessons:
        try:
            a = types.InlineKeyboardButton(text=dect_name_lessons[i][1]+pstr_t, callback_data=dect_name_lessons[i][0]+pstr_cbd)
        except KeyError:
            return r_markup

        try:
            b = types.InlineKeyboardButton(text=dect_name_lessons[i+1][1]+pstr_t, callback_data=dect_name_lessons[i+1][0]+pstr_cbd)
        except KeyError:
            return r_markup.add(a)
        
        try:
            c = types.InlineKeyboardButton(text=dect_name_lessons[i+2][1]+pstr_t, callback_data=dect_name_lessons[i+2][0]+pstr_cbd)
        except KeyError:
            return r_markup.add(a, b)
        
        r_markup.add(a, b, c)
        i += 3

    return r_markup
def check(input: str, pstr_cbd: str) -> bool:
    i: int = 0
    while i < num_lessons:
        if input == dect_name_lessons[i]+pstr_cbd:
            return True
    return False


# DZ
markup_dz = gen_dz_markup(pstr_t='', pstr_cbd='')


paragraph = types.InlineKeyboardButton(text='§', callback_data='paragraph')

# DZ replace
markup_dz_update = gen_dz_markup(pstr_t=' (r)', pstr_cbd='_update').add(paragraph)

# DZ and photo update
markup_dz_update_p = gen_dz_markup(pstr_t=' (rp)', pstr_cbd='_update_p').add(paragraph)

# URL
markup_url = gen_dz_markup(pstr_t=' (u)', pstr_cbd='_url').add(paragraph)


# -=-=-=-=-=-=-=-=-=- Main Admin Panel -=-=-=-=-=-=-=-=-=- #

markup_admin_panel = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
mailing = types.KeyboardButton('Рассылка✉️')
info = types.KeyboardButton('Статус сервера 🛠️')
markup_admin_panel.add(mailing, info)

# -=-=-=-=-=-=-=-=-=- End Main Admin Panel -=-=-=-=-=-=-=-=-=- #

# -=-=-=-=-=-=-=-=-=- Admin Panel -=-=-=-=-=-=-=-=-=- #

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
