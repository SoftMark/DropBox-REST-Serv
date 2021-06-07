from currentuser import CurrentUser


class Memory:
    user = CurrentUser(None)

    @classmethod
    def clear_user(cls):
        cls.user = CurrentUser(None)

    @classmethod
    def update_user(cls, auth_code):
        cls.user.auth(auth_code)