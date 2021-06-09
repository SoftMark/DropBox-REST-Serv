from dropbox import Dropbox
from dropboxAPI import DbxApi
from SECRET import ACCESS_TOKEN


class CurrentUser:
    def __init__(self, auth_code):
        self.auth_code = auth_code
        self.auth(auth_code)
        self.files = []
        self.active = False

        self.visible = {
            "files": True,
            "upload": False
        }

    def auth(self, auth_code):
        try:
            self.acc = DbxApi.get_account(auth_code)
            self.auth_code = auth_code
        except: self.acc = None

    def get_files(self):
        result = []
        for file in DbxApi.files_list().entries:
            result.append(file)
        self.files = result
        return result

    def has_files(self):
        if not self.get_files(): return False
        return True

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    def upload_bin(self, file):
        if file.filename[-4:len(file.filename)] == ".bin":
            DbxApi.upload(file)
            return True
        return False


