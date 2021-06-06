import dropbox
from dropbox import Dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from SECRET import APP_KEY, APP_SECRET


class DbxApi:
    _auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
    _authorize_url = _auth_flow.start()

    @classmethod
    def get_account(cls, auth_code):
        try:
            oauth_result = cls._auth_flow.finish(auth_code)
            with dropbox.Dropbox(oauth2_access_token=oauth_result.access_token) as dbx:
                acc = dbx.users_get_current_account()
                return acc
        except:
            return None

    @property
    def authorize_url(self):
        return self._authorize_url

# auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
#
# authorize_url = auth_flow.start()
# print("1. Go to: " + authorize_url)
# print("2. Click \"Allow\" (you might have to log in first).")
# print("3. Copy the authorization code.")
# auth_code = input("Enter the authorization code here: ").strip()
#
# try:
#     oauth_result = auth_flow.finish(auth_code)
# except Exception as e:
#     print('Error: %s' % (e,))
#     exit(1)
#
# with dropbox.Dropbox(oauth2_access_token=oauth_result.access_token) as dbx:
#     dbx.users_get_current_account()
#     print("Successfully set up client!")

# dbx = Dropbox("sl.AyLPCSFp_Ms-u5N5oSaZ9Srz5rM-53Xijr3KmhcFNepC1IoXXz7RwBsIcATi_gG8jLHCdJbCthQxI3YkiM7lJf9znj0UT1QJG5X6UUkeP6jG0fnbmTu1UnKP90qLgnThk1OsNxk")
#
# print(dbx.files_list_folder(path=""))