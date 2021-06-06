import dropbox
from dropbox import Dropbox
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from dropbox import DropboxOAuth2FlowNoRedirect

from DropBoxAPI import DbxApi

app = Flask(__name__)

# app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite///DataBase.db'
# db = SQLAlchemy(app)

# User

# class User(db.Model):


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html", auth_link=DbxApi._authorize_url)


@app.route('/test1')
@app.route('/test2')
def test():
    return "Test page"


@app.route('/user')
def user(auth_code):
    account = DbxApi.get_account(auth_code)
    return account.email


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        auth_code = request.form["auth_code"]
        if auth_code != "":
            return redirect(url_for("user", auth_code=auth_code))

#  elif request.method == 'GET':
    #flash('You must be logged in DropBox in current browser!')
    return index()


if __name__ == "__main__":
    app.run(debug=True)