import os
from app.models.user import User
from app.models.whiskey import Whiskey
from app.models.rating import Rating
from app.models.comment import Comment
from app.models.reply import Reply
from app import app
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






