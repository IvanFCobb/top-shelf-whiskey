import os
from flask_app.models.user import User
from flask_app.models.whiskey import Whiskey
from flask_app.models.rating import Rating
from flask_app.models.comment import Comment
from flask_app.models.reply import Reply
from flask_app import app
from PIL import Image
from flask import render_template, redirect, request, session, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename



# Configure upload settings and allowed file extensions
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}



# Helper function to check if the whiskey image exists
def image_exists(image_path):
    return os.path.isfile(image_path)



# Function to handle file upload
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'svg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Helper function to find the correct image file with an allowed extension
def find_image_with_extension(image_folder, image_name):
    for ext in ALLOWED_EXTENSIONS:
        file_path = os.path.join(image_folder, f"{image_name}.{ext}")
        if os.path.isfile(file_path):
            return file_path
    return None




@app.route('/topwhiskey', methods=['GET', 'POST'])
def topwhiskey():
    if 'user_id' not in session:
        return redirect ("/")
    
    # Set sorting order for the whiskey list
    sort_by_rating = request.args.get("sort", "desc") == "desc"    
    if sort_by_rating:
        sort_order = "DESC"
    else:
        sort_order = "ASC"
        
    # Set sorting order based on form input
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
    
    filters = {
        "category" : request.args.get("category", "all"),
        "distillery" : "all"
    }

    categories = ["All", "Bourbon", "Rye", "Scotch", "Irish", "Japanese", "Canadian", "American", "Tennessee", "Other"]
    search = request.args.get('search', None)
    whiskeys = Whiskey.get_whiskeys(data, filters, search)
    user = User.get_by_id(data)
    image_urls = {}
    
    for whiskey in whiskeys:
        print(whiskey.category)
        whiskey_id_str = str(whiskey.id)
        image_folder = os.path.join('flask_app', 'static', 'uploads')
        image_path = find_image_with_extension(image_folder, whiskey_id_str)
        if image_path:
            image_ext = image_path.split('.')[-1]
            image_urls[whiskey.id] = url_for('static', filename=f'uploads/{whiskey_id_str}.{image_ext}')
        else:
            image_urls[whiskey.id] = url_for('static', filename='images/placeholder_whiskey.png')

    return render_template("top_whiskey.html", sort_by_rating=sort_by_rating, whiskeys=whiskeys, user=user, categories = categories, image_urls = image_urls)



@app.route('/myshelf', methods=['GET', 'POST'])
def myshelf():
    if 'user_id' not in session:
        return redirect ("/")
    sort_by_rating = request.args.get("sort", "desc") == "desc"    
    if sort_by_rating:
        sort_order = "DESC"
    else:
        sort_order = "ASC"
        
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
    
    filters = {
        "category" : request.args.get("category", "all"),
        "distillery" : "all"
    }

    categories = ["All", "Bourbon", "Rye", "Scotch", "Irish", "Japanese", "Canadian", "American", "Tennessee", "Other"]
    recent = Whiskey.get_recently_rated_whiskeys(data)
    search = request.args.get('search', None)
    whiskeys = Whiskey.get_all_rated_whiskeys(data, filters, search)
    user = User.get_by_id(data)
    image_urls = {}
    
    for whiskey in recent:
        whiskey_id_str = str(whiskey.id)
        image_folder = os.path.join('flask_app', 'static', 'uploads')
        image_path = find_image_with_extension(image_folder, whiskey_id_str)
        if image_path:

            image_ext = image_path.split('.')[-1]
            image_urls[whiskey.id] = url_for('static', filename=f'uploads/{whiskey_id_str}.{image_ext}')
        else:
            image_urls[whiskey.id] = url_for('static', filename='images/placeholder_whiskey.png')
    
    for whiskey in whiskeys:
        whiskey_id_str = str(whiskey.id)
        image_folder = os.path.join('flask_app', 'static', 'uploads')
        image_path = find_image_with_extension(image_folder, whiskey_id_str)
        if image_path:
            image_ext = image_path.split('.')[-1]
            image_urls[whiskey.id] = url_for('static', filename=f'uploads/{whiskey_id_str}.{image_ext}')
        else:
            image_urls[whiskey.id] = url_for('static', filename='images/placeholder_whiskey.png')
            
    return render_template("myshelf.html", sort_by_rating=sort_by_rating, whiskeys=whiskeys, user=user, recent=recent, categories=categories, image_urls=image_urls)


@app.route('/usershelf/<int:num>', methods=['GET', 'POST'])
def usershelf(num):
    if 'user_id' not in session:
        return redirect ("/")
    sort_by_rating = request.args.get("sort", "desc") == "desc"    
    if sort_by_rating:
        sort_order = "DESC"
    else:
        sort_order = "ASC"
        
    if request.method == 'POST':
        form_sort_order = request.form.get('sort_order', 'asc')
        if form_sort_order:
            sort_order = 'asc'
        else:
            sort_order = 'desc'
            
    data = {
        "id": num,
        "sort_order": sort_order
    }
    
    filters = {
        "category" : request.args.get("category", "all"),
        "distillery" : "all"
    }

    categories = ["All", "Bourbon", "Rye", "Scotch", "Irish", "Japanese", "Canadian", "American", "Tennessee", "Other"]
    recent = Whiskey.get_recently_rated_whiskeys(data)
    search = request.args.get('search', None)
    whiskeys = Whiskey.get_all_rated_whiskeys(data, filters, search)
    user = User.get_by_id(data)
    image_urls = {}
    
    for whiskey in recent:
        whiskey_id_str = str(whiskey.id)
        image_folder = os.path.join('Flask_app', 'static', 'uploads')
        image_path = find_image_with_extension(image_folder, whiskey_id_str)
        if image_path:

            image_ext = image_path.split('.')[-1]
            image_urls[whiskey.id] = url_for('static', filename=f'uploads/{whiskey_id_str}.{image_ext}')
        else:
            image_urls[whiskey.id] = url_for('static', filename='images/placeholder_whiskey.png')
    
    for whiskey in whiskeys:
        whiskey_id_str = str(whiskey.id)
        image_folder = os.path.join('flask_app', 'static', 'uploads')
        image_path = find_image_with_extension(image_folder, whiskey_id_str)
        if image_path:
            image_ext = image_path.split('.')[-1]
            image_urls[whiskey.id] = url_for('static', filename=f'uploads/{whiskey_id_str}.{image_ext}')
        else:
            image_urls[whiskey.id] = url_for('static', filename='images/placeholder_whiskey.png')
            
    return render_template("user_shelf.html", sort_by_rating=sort_by_rating, whiskeys=whiskeys, user=user, recent=recent, categories=categories, image_urls=image_urls)



@app.route('/whiskeys/new')
def create_whiskey_view():
    if 'user_id' not in session:
        return redirect ("/")
    
    data = {
        "id": session['user_id']
    }
    
    user = User.get_by_id(data)
    return render_template("create_whiskey.html", user=user)



@app.route('/whiskey/<int:num>', methods=['GET', 'POST'])
def one_whiskey(num):
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id": session['user_id']
    }
    
    whiskey_data = {
        "id": num,
    }
    
    user = User.get_by_id(data)
    whiskey = Whiskey.get_whiskey_with_user_rating(data, whiskey_data)
    creator = Whiskey.get_single_whiskey(whiskey_data)
    whiskey_id_str = str(whiskey.id)
    image_urls = {}
    image_path = os.path.join('flask_app', 'static', 'uploads', whiskey_id_str + '.jpg')
    print("image path", image_path)
    whiskey_id_str = str(whiskey.id)
    image_folder = os.path.join('flask_app', 'static', 'uploads')
    image_path = find_image_with_extension(image_folder, whiskey_id_str)
    print("image path", image_path)
    if image_path:
        print("image found")
        image_ext = image_path.split('.')[-1]
        image_urls[whiskey.id] = url_for('static', filename=f'uploads/{whiskey_id_str}.{image_ext}')
    else:
        print("no image")
        image_urls[whiskey.id] = url_for('static', filename='images/placeholder_whiskey.png')
    
    comments = Comment.get_comments_by_whiskey_id(whiskey_data)
    
    if request.method == 'POST':
        whiskey_data = {
            "user_id": session['user_id'],
            "whiskey_id": num
        }
        if 'rating' in request.form:
            whiskey_data["rating"] = request.form['rating']
            if whiskey.rating.rating == None:
                Rating.save(whiskey_data)
            else:
                Rating.edit(whiskey_data)

        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                file_name = num
                file_type = secure_filename(image.filename.rsplit('.', 1)[1].lower())
                
                # Save the uploaded image file to the specified path
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_name}.{file_type}")
                image.save(file_path)
                
                # Compress and save the image
                compress_and_save_image(file_path)

        return redirect(url_for('one_whiskey', num=num))
    return render_template("whiskey.html", user=user, creator=creator, whiskey=whiskey, image_urls=image_urls, comments=comments)







@app.route('/whiskey/edit/<int:whiskey_id>', methods=['POST'])
def whiskey_edit(whiskey_id):
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id": session['user_id']
    }
    whiskey_data = {
        "id": whiskey_id
        }
    user = User.get_by_id(data)
    whiskey = Whiskey.get_whiskey_with_user_rating(data, whiskey_data)

    
    session["whiskey_id"] = whiskey_id
    return render_template("edit_whiskey.html", user=user, whiskey=whiskey)


@app.route('/whiskeys/delete/<int:num>')
def whiskey_delete(num):
    if 'user_id' not in session:
        return redirect ("/")
    Whiskey.delete(num)
    return redirect("/whiskeys")


# Function to compress and save an image
def compress_and_save_image(file_path):
    img = Image.open(file_path)
    img.thumbnail((800, 800))
    img.save(file_path)


@app.route('/create_whiskey', methods=["POST"])
def new_whiskey():
    # Check if the user is logged in
    if 'user_id' not in session:
        return redirect ("/")
    
    # Validate form data for the whiskey entry
    if Whiskey.is_valid_whiskey(request.form):
        # If valid, check if an image file was submitted
        if 'image' not in request.files:
            flash('No file part', "register")
            return redirect("/whiskeys/new")
        
        # Get the submitted image file
        file = request.files['image']
        
        # Check if a file was selected
        if file.filename == '':
            data = {
                "name": request.form['name'],
                "category": request.form['category'],
                "distillery": request.form['distillery'],
                "age": request.form['age'],
                "abv": request.form['abv'],
                "user_id": session['user_id']
            }
            whiskey_id = Whiskey.save(data)
            rating_data = {
                "whiskey_id": whiskey_id,
                "rating" : request.form['rating'],
                "user_id" : session['user_id']
            }
            Rating.save(rating_data)
            return redirect("/myshelf")
        
        
        # If a file was selected and it has an allowed file extension, proceed with saving the entry
        if file and allowed_file(file.filename):
            # Prepare data for saving the whiskey entry
            data = {
                "name": request.form['name'],
                "category": request.form['category'],
                "distillery": request.form['distillery'],
                "age": request.form['age'],
                "abv": request.form['abv'],
                "user_id": session['user_id']
            }
            
            
            
            # Save the whiskey entry and get the generated file name
            file_name = Whiskey.save(data)
            file_type = secure_filename(file.filename.rsplit('.', 1)[1].lower())
            
            rating_data = {
                "whiskey_id": file_name,
                "rating" : request.form['rating'],
                "user_id" : session['user_id']
            }
            
            Rating.save(rating_data)
            
            # Save the uploaded image file to the specified path
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_name}.{file_type}")
            file.save(file_path)
            
            # Compress and save the image
            compress_and_save_image(file_path)
            
            return redirect('/myshelf')
        else:
            flash('Invalid file format', "register")
            return redirect('/whiskeys/new')
    else: 
        return redirect('/whiskeys/new')
    


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    
    
@app.route('/whiskey/<int:whiskey_id>/edit', methods=["POST"])
def edit_whiskey(whiskey_id):
    if 'user_id' not in session:
        return redirect ("/")
    if Whiskey.is_valid_whiskey(request.form): 
        data = {
                "id": whiskey_id,
                "name": request.form['name'],
                "category": request.form['category'],
                "distillery": request.form['distillery'],
                "age": request.form['age'],
                "abv": request.form['abv'],
                "user_id": session['user_id']
            }
        Whiskey.edit(data)
        session.pop('whiskey_id', default=None)
        return redirect("/whiskey/{}".format(whiskey_id))
    else:
        return redirect("/whiskeys/edit/{}".format(session["whiskey_id"]))


@app.route('/whiskey/<int:whiskey_id>/delete', methods=["POST"])
def remove_whiskey(whiskey_id):
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id": whiskey_id,
        "user_id": session['user_id']
    }
    whiskey = Whiskey.get_whiskey_with_user_rating(data, data)
    if session['user_id'] != whiskey.creator.id:
        return redirect ("/topwhiskey")
    data = {
        "id": whiskey_id,
        "user_id": session['user_id']
    }
    comments = Comment.get_comments_by_whiskey_id(data)
    for comment in comments:
        comment_data = {
            "comment_id": comment.id
            }
        Reply.delete_comment(comment_data)
    Comment.delete_all_whiskey_comments(data)
    Rating.delete_all_for_one_whiskey(data)
    Whiskey.delete(data)
    return redirect("/topwhiskey")




