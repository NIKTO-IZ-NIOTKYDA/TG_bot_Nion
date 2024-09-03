from telebot import types

import sgo.types_NSAPI as types_NSAPI
from db import get_net_school
from utils import dict_name_lessons, num_lessons, check_for_admin

del_schedule_button = types.InlineKeyboardButton(text='❌ Удалить ❌', callback_data='schedule_del_warn')
paragraph = types.InlineKeyboardButton(text='§', callback_data='paragraph')
back = types.InlineKeyboardButton(text='⬅️  Назад', callback_data='back_dz')
back_in_main_menu = types.InlineKeyboardButton(text='⏪ Вернуться в главное меню', callback_data='back_in_main_menu')


def gen_markup_start(user_id: int):
    markup = types.InlineKeyboardMarkup(row_width=1)
    DZ = types.InlineKeyboardButton(text='Домашнее задание 📚', callback_data='dz')
    Schedule = types.InlineKeyboardButton(text='Расписание 📑', callback_data='schedule')
    Call_schedule = types.InlineKeyboardButton(text='Расписание звонков 🕝', callback_data='call_schedule')
    NetSchool = types.InlineKeyboardButton(text='СГО [В разработке]', callback_data='pass')
    Profile = types.InlineKeyboardButton(text='Профиль 👤', callback_data='profile')

    markup.add(DZ, Schedule, Call_schedule)

    if get_net_school(user_id=user_id, decode=False) != None:
        markup.add(NetSchool)

    if check_for_admin(user_id):
        markup.add(types.InlineKeyboardButton(text='Админ-панель‼️', callback_data='admin_panel'))

    markup.add(Profile)
    
    return markup


# SGO
markup_NetSchool = types.InlineKeyboardMarkup(row_width=1)
Diary = types.InlineKeyboardButton(text='Дневник', callback_data='diary')
Overdue = types.InlineKeyboardButton(text='Просроченные задания', callback_data='overdue')
Announcements = types.InlineKeyboardButton(text='Объявления', callback_data='announcements')
School = types.InlineKeyboardButton(text='Информация о школе', callback_data='school')
markup_NetSchool.add(Diary, Overdue, Announcements, School, back_in_main_menu)

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


def gen_profile_markup(rsn: bool | None, net_school: dict[str] | KeyError | None) -> types.InlineKeyboardMarkup:
    if rsn == None:
        return types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(text='DB_ERROR', callback_data='pass'))

    markup = types.InlineKeyboardMarkup()

    if rsn:
        markup.add(types.InlineKeyboardButton(text='Отключить уведомления', callback_data='off_notifications_warn'))
    else:
        markup.add(types.InlineKeyboardButton(text='Включить уведомления', callback_data='on_notifications'))

    #if net_school == None:
        #markup.add(types.InlineKeyboardButton(text='Включить интеграцию с СГО', callback_data='on_net_school'))
    #else:
        #markup.add(types.InlineKeyboardButton(text='Отключить интеграцию с СГО', callback_data='off_net_school'))

    return markup.add(back_in_main_menu)


def gen_announcements(an: list) -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup(row_width=3)

    if an != []:
        # TODO:
        pass

    markup.row_width = 1
    markup.add(types.InlineKeyboardButton(text='Объявлений нет', callback_data='pass'), types.InlineKeyboardButton(text='⬅️  Назад', callback_data='netschool'), back_in_main_menu)
    return markup


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
markup_update_dz_or_gdz.add(dz, gdz, back_in_main_menu)

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
