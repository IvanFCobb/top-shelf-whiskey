from app.models.user import User
from app.models.whiskey import Whiskey
from app.models.rating import Rating


from app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)





@app.route('/')
def index():
    if 'user_id' in session:
        logged_in = True
    else:
        logged_in = False
    return render_template("index.html", logged_in=logged_in)



@app.route('/login')
def login():
    return render_template("login.html")



@app.route('/login_user', methods=['POST'])
def login_user():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data["email"])
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/login')
    session['user_id'] = user_in_db.id
    return redirect("/myshelf")



@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")



@app.route('/register')
def register():
    return render_template("register.html")



@app.route('/register_user', methods=["POST"])
def register_user():       
    if User.is_valid_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
        "username": request.form['username'],
        "email": request.form['email'],
        "password": pw_hash,
        }
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect("/myshelf")
    else:
        return redirect('/register')


