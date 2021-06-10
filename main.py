from flask import Flask, render_template, request, redirect, flash
from memory import Memory as Mem
from dropbox_serv import DbxService as DbxServ

# Initialize application
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = '/bin'


# Authorization page
@app.route('/')
def index():
    return render_template("index.html", auth_link=DbxServ._authorize_url)


# Authorization process
@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        # Requesting authorizing code
        if request.method == 'POST':
            auth_code = request.form["auth_code"]
            # Processing entered data
            if auth_code != "":
                # User enter something //
                # Trying to load user
                Mem.user.auth(auth_code)
                # Was it loaded correctly
                if Mem.user.active:
                    # Success! User loaded, loading user page
                    return redirect("/user")
                else:
                    # Authorizing code was wrong!
                    flash("Wrong auth code!")
                # \\
            else:
                # When user enter nothing
                flash("Field is empty!")
        # User was not loaded, opening Authorizing page again
        return redirect('/')
    except:
        # Something went wrong, opening Authorizing page again
        flash("Error! Try again please.")
        return redirect('/')


# User page
@app.route('/user')
def user_page():
    try:
        # Loading user page
        Mem.user.load_files()
        return render_template("user_page.html", user=Mem.user)
    except:
        # Something went wrong, opening Authorizing page again
        flash("Error! Try again please.")
        return redirect('/')


# File deleting process
@app.route('/user/<string:file_name>/delete/')
def delete_file(file_name):
    try:
        # Deletes
        Mem.user.delete_bin(file_name)
        flash(f"File '{file_name}' successfully deleted!")
        # Back to user page
        return redirect('/user')
    except:
        # Something went wrong, opening Authorizing page again
        flash("Error! Try again please.")
        return redirect('/')


# File uploading process
@app.route('/user/upload/', methods=["POST", "GET"])
def upload_file():
    try:
        # Requesting file
        file = request.files["bin_file"]
        # Did user choose file
        if file:
            # File chose
            flash(f"Processing '{file.filename}' file...")
            # If file binary uploads
            if Mem.user.upload_bin(file):
                flash(f"File '{file.filename}' uploaded correctly!")
            else:
                # Not binary
                flash("File must be binary!")
        else:
            # User did not choose file
            flash("Choose file first!")
        # Success, back to user page
        return redirect('/user')
    except:
        # Something went wrong, opening Authorizing page again
        flash("Error! Try again please.")
        return redirect('/')


# Log out
@app.route('/user/logout')
def logout():
    try:
        Mem.deactivate_user()
        flash("Logged out!")
        return redirect('/')
    except:
        # Something went wrong, opening Authorizing page again
        flash("Error! Try again please.")
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)






