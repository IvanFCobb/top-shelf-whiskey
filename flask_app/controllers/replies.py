import os
from flask_app.models.user import User
from flask_app.models.whiskey import Whiskey
from flask_app.models.rating import Rating
from flask_app.models.comment import Comment
from flask_app.models.reply import Reply
from flask_app import app
from flask import render_template, redirect, request, session, flash, url_for, send_from_directory




@app.route('/reply/<int:whiskey_id>/<int:comment_id>', methods=['POST'])
def add_reply(comment_id, whiskey_id):
    if 'user_id' not in session:
        return redirect ("/")
        
    data = {
        "content": request.form['content'],
        "user_id": session['user_id'],
        "comment_id": comment_id
    }
    
    Reply.save(data)
    return redirect(url_for('one_whiskey', num=whiskey_id))




@app.route('/reply/delete/<int:whiskey_id>/<int:reply_id>')
def remove_reply(reply_id, whiskey_id):
    if 'user_id' not in session:
        return redirect ("/")
        
    data = {
        "reply_id": reply_id,
        "user_id": session['user_id']
    }
    Reply.delete(data)
    return redirect(url_for('one_whiskey', num=whiskey_id))






