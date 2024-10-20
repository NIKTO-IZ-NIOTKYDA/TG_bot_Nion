from netschoolapi import NetSchoolAPI


class tmp_vars:
    input_text_mailing: str | None = None
    on_net_school_list_users: list[int] = []
    login_net_school_list_users: list[int] = []
    logined_net_school_list_users: dict[int, NetSchoolAPI] = {}
    press_button_notification_admin_list_users: dict[int, str] = {}
    newsletter: bool = False
    input_text: str = r'None'


def get_logined_net_school(self: type[tmp_vars], user_id: int) -> NetSchoolAPI | ValueError:
    try:
        return self.logined_net_school_list_users[user_id]
    except Exception:
        return ValueError
