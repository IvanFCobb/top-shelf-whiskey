import os
from app.models.user import User
from app.models.whiskey import Whiskey
from app.models.rating import Rating
from app.models.comment import Comment
from app.models.reply import Reply
from app import app
from PIL import Image
from flask import render_template, redirect, request, session, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename


@app.route('/comment/<int:whiskey_id>', methods=['POST'])
def add_comment(whiskey_id):
    if 'user_id' not in session:
        return redirect ("/")
        
    data = {
        "comment": request.form['comment'],
        "user_id": session['user_id'],
        "whiskey_id": whiskey_id
    }
    
    Comment.save(data)
    return redirect(url_for('one_whiskey', num=whiskey_id))

@app.route('/comment/delete/<int:whiskey_id>/<int:comment_id>')
def remove_comment(comment_id, whiskey_id):
    if 'user_id' not in session:
        return redirect ("/")
        
    data = {
        "comment_id": comment_id,
        "user_id": session['user_id']
    }
    Reply.delete_comment(data)
    Comment.delete(data)
    return redirect(url_for('one_whiskey', num=whiskey_id))




