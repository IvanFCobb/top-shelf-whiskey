from app.models.user import User
from app.models.whiskey import Whiskey
from app import app
from flask import render_template, redirect, request, session, flash




@app.route('/topwhiskey')
def whiskeys():
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id": session['user_id']
    }
    user = User.get_by_id(data)
    whiskeys = Whiskey.get_all_whiskeys_with_creator()
    rated = Whiskey.get_all_rated_whiskeys(session['user_id'])
    return render_template("whiskeys.html", user=user, whiskeys = whiskeys, rated = rated)



@app.route('/whiskeys/new')
def create_whiskey_view():
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id": session['user_id']
    }
    user = User.get_by_id(data)
    return render_template("new_whiskey.html", user=user)


    
@app.route('/whiskeys/<int:num>')
def one_whiskey(num):
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id": session['user_id']
    }
    user = User.get_by_id(data)
    whiskey = whiskey.get_by_id_with_creator(num)
    purchases = len(whiskey.number_of_purchases)
    return render_template("view_whiskey.html", user=user, whiskey=whiskey, purchases = purchases)



@app.route('/whiskeys/edit/<int:num>')
def whiskey_edit(num):
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id": session['user_id']
    }
    user = User.get_by_id(data)
    whiskey = whiskey.get_by_id_with_creator(num)
    if whiskey.user_id != session['user_id']:
        return redirect("/whiskeys") 
    
    session["whiskey_id"] = whiskey.id
    return render_template("edit_whiskey.html", user=user, whiskey=whiskey)



@app.route('/whiskeys/delete/<int:num>')
def whiskey_delete(num):
    if 'user_id' not in session:
        return redirect ("/")
    Whiskey.delete(num)
    return redirect("/whiskeys")



@app.route('/create_whiskey', methods=["POST"])
def new_whiskey():
    if 'user_id' not in session:
        return redirect ("/")
    if Whiskey.is_valid_whiskey(request.form):
        data = {
            "title": request.form['title'],
            "description": request.form['description'],
            "price": request.form['price'],
            "quantity": request.form['quantity'],
            "user_id": session['user_id']
        }
        Whiskey.save(data)
        return redirect("/whiskeys")
    else: 
        return redirect('/whiskeys/new')
    
    

@app.route('/edit_whiskey', methods=["POST"])
def edit_whiskey():
    if 'user_id' not in session:
        return redirect ("/")
    if Whiskey.is_valid_whiskey(request.form): 
        data = {
            "id": session["whiskey_id"],
            "title": request.form['title'],
            "description": request.form['description'],
            "price": request.form['price'],
            "quantity": request.form['quantity'],
            "user_id": session['user_id']
        }
        Whiskey.edit(data)
        session.pop('whiskey_id', default=None)
        return redirect("/whiskeys")
    else:
        return redirect("/whiskeys/edit/{}".format(session["whiskey_id"]))
