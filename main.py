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
    return render_template("index.html", auth_link=DbxApi._authorize_url)


def safe_route(route):
    def wrapper(*args):
        try: return route(args)
        except:
            flash("Error! Try again please.")
            return index()
    return wrapper


@safe_route
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        auth_code = request.form["auth_code"]
        if auth_code != "":
            mem.update_user(auth_code)
            if mem.user.acc is not None:
                mem.user.activate()
                href = '/user/'+auth_code+'/'
                return redirect(href)
            else: flash("Wrong auth code!")
        else: flash("Field is empty!")

#  elif request.method == 'GET':
    #flash('You must be logged in DropBox in current browser!')
    mem.user.deactivate()
    return index()


@app.route('/user/<string:auth_code>/')
def user_page(auth_code):
    print("Authorized by " + auth_code)
    return render_template("user_page.html", user=mem.user, dbx=DbxApi.dbx)


@app.route('/user/<string:auth_code>/files/')
def show_user_files(auth_code):
    print("Displaying " + auth_code + " files")
    #mem.user.visible["files"] = not mem.user.visible["files"]
    return render_template("user_page.html", user=mem.user, dbx=DbxApi.dbx)


@safe_route
@app.route('/open_uploader')
def open_uploader():
    mem.user.visible["upload"] = not mem.user.visible["upload"]
    return render_template("user_page.html", user=mem.user, dbx=DbxApi.dbx)


@app.route('/user/<string:auth_code>/files/<string:file_name>/delete/')
def delete_file(auth_code, file_name):
    print("User with auth: " + auth_code + " deletes file " + file_name)
    DbxApi.dbx.files_delete("/Binary/"+file_name)
    # return render_template("user_page.html", user=mem.user, dbx=DbxApi.dbx)
    return redirect(f'/user/{auth_code}/files/')


if __name__ == "__main__":
    app.run(debug=True)




