from dropbox import Dropbox
from dropboxAPI import DbxApi
from SECRET import ACCESS_TOKEN


class CurrentUser:
    def __init__(self, auth_code):
        self.auth_code = auth_code
        self.auth(auth_code)

        self.visible = {
            "files": False,
            "upload": False
        }

    def auth(self, auth_code):
        try:
            self.acc = DbxApi.get_account(auth_code)
        except: self.acc = None

    @classmethod
    def get_files(cls):
        result = []
        for file in DbxApi.files_list().entries:
            result.append(file)
        return result

    def put_file(self):
        pass

