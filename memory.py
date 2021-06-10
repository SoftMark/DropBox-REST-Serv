from currentuser import CurrentUser


class Memory:
    user = CurrentUser(None)

    @classmethod
    def deactivate_user(cls):
        cls.user.deactivate()

    @classmethod
    def load_user(cls, auth_code):
        cls.user.auth(auth_code)
