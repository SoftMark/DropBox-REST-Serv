from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite///DataBase.db'
db = SQLAlchemy(app)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/test1')
@app.route('/test2')
def test():
    return "Test page"


@app.route('/user/<string:login>/<int:id>')
def user(login, id):
    return f"| Login: {login} | ID: {str(id) } |"


if __name__ == "__main__":
    app.run(debug=True)