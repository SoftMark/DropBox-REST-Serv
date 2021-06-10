from dropbox_serv import DbxService


class CurrentUser:
    def __init__(self, auth_code):
        self.auth_code = auth_code
        self.auth(auth_code)
        self.files = []
        self.active = False

    # Authorization
    def auth(self, auth_code):
        try:
            self.acc = DbxService.get_account(auth_code)
            self.auth_code = auth_code
            self.load_files()
            self.activate()
        except:
            self.acc = None
            self.deactivate()

    # Gets list of files
    def load_files(self):
        self.files = [file for file in DbxService.files_list()]

    # Does account has files
    def has_files(self):
        return not not self.files

    # Account status /
    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
        self.files = []
        self.auth_code = None
    # \

    # Uploads binary file to current account
    def upload_bin(self, file):
        # Is file binary
        if file.filename[-4:] == ".bin":
            # Uploading
            DbxService.upload(file)
            self.load_files()
            return True
        return False

    # Deleting binary file
    @classmethod
    def delete_bin(cls, file_name):
        DbxService.delete_file(file_name)

    # Get file temporary link
    @classmethod
    def load_link(cls, file):
        return DbxService.dbx.files_get_temporary_link(file.path_display).link

