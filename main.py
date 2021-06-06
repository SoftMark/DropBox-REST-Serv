from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite///DataBase.db'
db = SQLAlchemy(app)

# User

# class User(db.Model):


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/test1')
@app.route('/test2')
def test():
    return "Test page"


@app.route('/user/<string:mail>/')
def user(mail):
    return f"| MAIL: {mail} |"


@app.route('/login', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        email = request.form["mail"]
        return redirect(url_for("user", mail=email))
    elif request.method == 'GET':
        return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)