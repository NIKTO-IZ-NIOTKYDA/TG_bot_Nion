from telebot import types

# Start
markup_start = types.InlineKeyboardMarkup(row_width=1)
DZ = types.InlineKeyboardButton(text='Домашнее задание 📚', callback_data='dz')
schedule = types.InlineKeyboardButton(text='Расписание 📑', callback_data='schedule')
call_schedule = types.InlineKeyboardButton(text='Расписание звонков 🕝', callback_data='call_schedule')
profile = types.InlineKeyboardButton(text='Профиль 👤', callback_data='profile')
markup_start.add(DZ, schedule, call_schedule, profile)

# Warn off notifications
markup_off_notifications_warn = types.InlineKeyboardMarkup(row_width=1)
off_notifications_warn = types.InlineKeyboardButton(text='Да, я хочу отключить уведомления', callback_data='off_notifications')
no_off_notifications_warn = types.InlineKeyboardButton(text='Нет, я хочу оставить уведомления', callback_data='profile')
markup_off_notifications_warn.add(off_notifications_warn, no_off_notifications_warn)

# Warn del schedule
markup_del_schedule_warn = types.InlineKeyboardMarkup()
yes = types.InlineKeyboardButton(text='✅ Да ✅', callback_data='schedule_del')
no = types.InlineKeyboardButton(text='❌ Нет ❌', callback_data='schedule_del_no')
markup_del_schedule_warn.add(yes, no)

num_lessons: int = 19
dict_name_lessons = {
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
    18: ['chemistry', 'Химия']
}


def gen_dz_markup(pstr_t: str, pstr_cbd: str) -> types.InlineKeyboardMarkup:
    r_markup = types.InlineKeyboardMarkup(row_width=3)

    i: int = 0
    while i < num_lessons:
        try:
            a = types.InlineKeyboardButton(text=dict_name_lessons[i][1]+pstr_t, callback_data=dict_name_lessons[i][0]+pstr_cbd)
        except KeyError:
            return r_markup

        try:
            b = types.InlineKeyboardButton(text=dict_name_lessons[i+1][1]+pstr_t, callback_data=dict_name_lessons[i+1][0]+pstr_cbd)
        except KeyError:
            return r_markup.add(a)

        try:
            c = types.InlineKeyboardButton(text=dict_name_lessons[i+2][1]+pstr_t, callback_data=dict_name_lessons[i+2][0]+pstr_cbd)
        except KeyError:
            return r_markup.add(a, b)

        r_markup.add(a, b, c)
        i += 3

    return r_markup


def check(input: str, pstr_cbd: str) -> bool:
    i: int = 0
    while i < num_lessons:
        if input == str(dict_name_lessons[i][0]+pstr_cbd):  # type: ignore[operator, unused-ignore]
            return True
        else:
            i += 1
    return False


def gen_notifications_markup(rsn: bool | None) -> types.InlineKeyboardMarkup:
    if rsn == None:
        return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='DB_ERROR', callback_data='pass'))

    markup_notifications = types.InlineKeyboardMarkup()

    if rsn:
        off_notifications = types.InlineKeyboardButton(text='Выключить уведомления', callback_data='off_notifications_warn')
        markup_notifications.add(off_notifications)
    else:
        on_notifications = types.InlineKeyboardButton(text='Включить уведомления', callback_data='on_notifications')
        markup_notifications.add(on_notifications)

    return markup_notifications.add(back_in_main_menu)


del_schedule_button = types.InlineKeyboardButton(text='❌ Удалить ❌', callback_data='schedule_del_warn')
paragraph = types.InlineKeyboardButton(text='§', callback_data='paragraph')
back = types.InlineKeyboardButton(text='⬅️  Назад', callback_data='back_dz')
back_in_main_menu = types.InlineKeyboardButton(text='⏪ Вернуться в главное меню', callback_data='back_in_main_menu')

# DZ
markup_dz = gen_dz_markup(pstr_t='', pstr_cbd='').add(back_in_main_menu)

# DZ replace
markup_dz_update = gen_dz_markup(pstr_t=' (r)', pstr_cbd='_update').add(paragraph)

# DZ and photo update
markup_dz_update_p = gen_dz_markup(pstr_t=' (rp)', pstr_cbd='_update_p').add(paragraph)

# URL
markup_url = gen_dz_markup(pstr_t=' (u)', pstr_cbd='_url').add(paragraph)

# -=-=-=-=-=-=-=-=-=- Admin Panel -=-=-=-=-=-=-=-=-=- #

markup_update_dz_or_gdz = types.InlineKeyboardMarkup(row_width=2)
dz = types.InlineKeyboardButton(text='Д/З', callback_data='update_dz')
gdz = types.InlineKeyboardButton(text='ГДЗ', callback_data='update_gdz')
markup_update_dz_or_gdz.add(dz, gdz)

markup_photo = types.InlineKeyboardMarkup(row_width=2)
dz = types.InlineKeyboardButton(text='Д/З', callback_data='photo_paste_dz')
schedule = types.InlineKeyboardButton(text='Расписание', callback_data='photo_paste_schedule')
markup_photo.add(schedule, dz)

# -=-=-=-=-=-=-=-=-=- End Admin Panel -=-=-=-=-=-=-=-=-=- #

# -=-=-=-=-=-=-=-=-=- Main Admin Panel -=-=-=-=-=-=-=-=-=- #

markup_admin_panel = types.InlineKeyboardMarkup(row_width=1)
mailing = types.InlineKeyboardButton('Рассылка✉️', callback_data='newsletter')
info = types.InlineKeyboardButton('Статус сервера 🛠️', callback_data='status_server')
markup_admin_panel.add(mailing, info, back_in_main_menu)

markup_chack_mailing = types.InlineKeyboardMarkup(row_width=2)
yes = types.InlineKeyboardButton(text='✅ YES ✅', callback_data='chack_mailing_yes')
no = types.InlineKeyboardButton(text='❌ NO ❌', callback_data='chack_mailing_no')
markup_chack_mailing.add(yes, no, back_in_main_menu)

# -=-=-=-=-=-=-=-=-=- End Main Admin Panel -=-=-=-=-=-=-=-=-=- #
