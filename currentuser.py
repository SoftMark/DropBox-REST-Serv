from dropboxAPI import DbxApi


class CurrentUser:
    def __init__(self, auth_code):
        self.auth(auth_code)

        self.visible = {
            "files": False,
            "upload": False
        }

    def auth(self, auth_code):
        try: self.acc = DbxApi.get_account(auth_code)
        except: self.acc = None

    def get_file(self):
        pass

    def put_file(self):
        pass

