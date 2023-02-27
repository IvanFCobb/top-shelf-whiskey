from app.models.user import User
from app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)


@app.route('/', methods=['get'])
def register_login():
    return render_template("index.html")


@app.route('/dashboard', methods=['get'])
def dashboard():
    try:
        user = User.get_by_id(session['user_id'])
        return render_template("dashboard.html", user=user)
    except KeyError:
        return redirect('/')


@app.route('/login', methods=['POST'])
def login():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data["email"])
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    # never render on a post!!!
    return redirect("/dashboard")


@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect("/")


@app.route('/create_user', methods=["POST"])
def register():
    try:
        is_valid = True
        if request.form['password'] != request.form['password_confirm']:
            flash("Confrim Password Does Not Match", "register")
            is_valid = False
        if len(request.form['password']) < 4:
            flash("Password Must Be More Than 5 Characters", "register")
            is_valid = False
        if len(request.form['fname']) < 2:
            flash("First Name must be at least 2 characters.", "register")
            is_valid = False
        if len(request.form['lname']) < 2:
            flash("Last Name must be at least 2 characters.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(request.form['email']):
            flash("Invalid email address!", "register")
            is_valid = False
        if is_valid == False:
            return redirect('/')
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        print(pw_hash)
        data = {
            "fname": request.form['fname'],
            "lname": request.form['lname'],
            "email": request.form['email'],
            "password": pw_hash,
        }
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect("/dashboard")
    except:
        return redirect("/")
