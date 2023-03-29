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
    return render_template("index.html")


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/myshelf', methods=['GET', 'POST'])
def myshelf():
    if 'user_id' not in session:
        return redirect ("/")
    sort_by_rating = request.args.get("sort", "desc") == "desc"    
    if sort_by_rating:
        sort_order = "DESC"
    else:
        sort_order = "ASC"
    print(sort_by_rating)
    print(sort_order)
    if request.method == 'POST':
        form_sort_order = request.form.get('sort_order', 'asc')
        if form_sort_order:
            sort_order = 'asc'
        else:
            sort_order = 'desc'
    data = {
        "id": session['user_id'],
        "sort_order": sort_order
    }
    whiskeys = Whiskey.get_all_rated_whiskeys(data)
    user = User.get_by_id(data)
    
    return render_template("myshelf.html", sort_by_rating=sort_by_rating, whiskeys=whiskeys, user=user)



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
    
    
    
@app.route('/purchase', methods=["POST"])
def purchase():
    data = {
        'user_id': session['user_id'],
        'whiskey_id': request.form['whiskey_id']
    }
    User.add_purchase(data)
    return redirect("/whiskeys")



