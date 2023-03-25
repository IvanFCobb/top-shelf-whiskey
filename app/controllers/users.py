from app.models.user import User
from app import app
from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/myshelf', methods=['GET', 'POST'])
def myshelf():
    cards = list(range(1, 16))
    sort_order = request.form.get('sort_order', 'asc')
    if request.method == 'POST':
        sort_order = request.form.get('sort_order', 'asc')
        if sort_order == 'asc':
            cards.sort()
        elif sort_order == 'desc':
            cards.sort(reverse=True)
    return render_template("myshelf.html", cards=cards, sort_order=sort_order)



@app.route('/login_user', methods=['POST'])
def login_user():
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data["email"])
    if not user_in_db:
        flash("Invalid Email/Password", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", "login")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/whiskeys")



@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")



@app.route('/register_user', methods=["POST"])
def register_user():       
    if User.is_valid_user(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email'],
        "password": pw_hash,
        }
        user_id = User.save(data)
        session['user_id'] = user_id
        return redirect("/whiskeys")
    else:
        return redirect('/')
    
    
    
@app.route('/purchase', methods=["POST"])
def purchase():
    data = {
        'user_id': session['user_id'],
        'whiskey_id': request.form['whiskey_id']
    }
    User.add_purchase(data)
    return redirect("/whiskeys")



