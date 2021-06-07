import dropbox
from dropbox import Dropbox
from flask import Flask, render_template, url_for, request, redirect, flash, session
from currentuser import CurrentUser
from memory import Memory as mem
from flask.sessions import SessionInterface
from flask_sqlalchemy import SQLAlchemy
from dropbox import DropboxOAuth2FlowNoRedirect

from dropboxAPI import DbxApi

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite///DataBase.db'
# db = SQLAlchemy(app)

# User

# class User(db.Model):


def index():
    mem.clear_user()
    return render_template("index.html", auth_link=DbxApi._authorize_url)


@app.route('/user')
def user_page(auth_code):
    mem.update_user(auth_code)
    if mem.user.acc is None:
        flash("Wrong auth code!")
        return index()
    # account.name
    return render_template("user_page.html", user=mem.user, dbx=DbxApi.dbx)


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        auth_code = request.form["auth_code"]
        if auth_code != "":
            mem.clear_user()
            return user_page(auth_code=auth_code)
        else: flash("Field is empty!")

#  elif request.method == 'GET':
    #flash('You must be logged in DropBox in current browser!')
    return index()


@app.route('/show_user_files')
def show_user_files():
    mem.user.visible["files"] = not mem.user.visible["files"]
    return render_template("user_page.html", user=mem.user, dbx=DbxApi.dbx)


@app.route('/open_uploader')
def open_uploader():
    mem.user.visible["upload"] = not mem.user.visible["upload"]
    return render_template("user_page.html", user=mem.user, dbx=DbxApi.dbx)


if __name__ == "__main__":
    app.run(debug=True)
