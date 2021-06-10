import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from SECRET import APP_KEY, APP_SECRET, ACCESS_TOKEN
from werkzeug.utils import secure_filename
import os


class DbxService:
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
    dbx_folder_path = "/Binary"
    serv_folder_path = "bin/"
    _auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
    _authorize_url = _auth_flow.start()

    # Loads files of current authorized user
    @classmethod
    def files_list(cls):
        return cls.dbx.files_list_folder(cls.dbx_folder_path).entries

    # Loads user account object
    @classmethod
    def get_account(cls, auth_code):
        oauth_result = cls._auth_flow.finish(auth_code)
        with dropbox.Dropbox(oauth2_access_token=oauth_result.access_token) as dbx:
            acc = dbx.users_get_current_account()
            return acc

    # Uploads file
    @classmethod
    def upload(cls, file):
        filename = secure_filename(file.filename)
        serv_path = cls.serv_folder_path + f"{filename}"
        file.save(serv_path)
        with open(serv_path, 'rb') as bin_f:
            cls.dbx.files_upload(bin_f.read(), cls.dbx_folder_path+f"/{filename}")
        os.remove(serv_path)

    # Deletes file from Dbx account
    @classmethod
    def delete_file(cls, file_name):
        cls.dbx.files_delete(f"{cls.dbx_folder_path}/{file_name}")

