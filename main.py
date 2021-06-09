from flask import Flask, render_template, request, redirect, flash
from memory import Memory as mem
from dropboxAPI import DbxApi

UPLOAD_FOLDER = '/bin'
ALLOWED_EXTENSIONS = {'bin'}

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def safe_route(route):
    def safe_that(*args):
        print(args)
        try:
            if not args:
                return route()
            else: return route(args[0])
        except:
            flash("Error! Try again please.")
            return index()
    return safe_that


@safe_route
@app.route('/')
def index():
    return render_template("index.html", auth_link=DbxApi._authorize_url)


@safe_route
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
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
    except:
        flash("Error! Try again please.")
        return index()


@safe_route
@app.route('/user/<string:auth_code>/')
def user_page(auth_code):
    try:
        print("Authorized by " + auth_code)
        return render_template("user_page.html", user=mem.user, dbx=DbxApi.dbx)
    except:
        flash("Error! Try again please.")
        return index()


@safe_route
@app.route('/user/<string:auth_code>/files/')
def show_user_files(auth_code):
    try:
        print("Displaying " + auth_code + " files")
        #mem.user.visible["files"] = not mem.user.visible["files"]
        return render_template("user_page.html", user=mem.user, dbx=DbxApi.dbx)
    except:
        flash("Error! Try again please.")
        return index()


@safe_route
@app.route('/user/<string:auth_code>/files/<string:file_name>/delete/')
def delete_file(auth_code, file_name):
    try:
        print("User with auth: " + auth_code + " deletes file " + file_name)
        DbxApi.dbx.files_delete(f"/Binary/{file_name}")
        flash(f"File '{file_name}' successfully deleted!")
        # return render_template("user_page.html", user=mem.user, dbx=DbxApi.dbx)
        return redirect(f'/user/{auth_code}/files/')
    except:
        flash("Error! Try again please.")
        return index()


@safe_route
@app.route('/user/<string:auth_code>/files/upload/', methods=["POST", "GET"])
def upload_file(auth_code):
    try:
        file = request.files["bin_file"]
        if file:
            flash(f"Processing '{file.filename}' file...")
            if mem.user.upload_bin(file):
                flash(f"File '{file.filename}' uploaded correctly!")
            else: flash(f"File must be binary!")
        else: flash("Choose file first!")

        return redirect(f'/user/{auth_code}/files/')
    except:
        flash("Error! Try again please.")
        return index()


if __name__ == "__main__":
    app.run(debug=True)




