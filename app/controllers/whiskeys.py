import os
from app.models.user import User
from app.models.whiskey import Whiskey
from app import app
from PIL import Image
from flask import render_template, redirect, request, session, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename


# Configure upload settings and allowed file extensions
app.config['UPLOAD_FOLDER'] = 'app/static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Helper function to check if the file has an allowed extension
def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Route for displaying top whiskeys
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
            
    # Prepare data for the query
    data = {
        "id": session['user_id'],
        "sort_order": sort_order
    }
    
    # Set filters for the whiskey list
    filters = {
        "category" : request.args.get("category", "all"),
        "distillery" : "all"
    }

    categories = ["All", "Bourbon", "Scotch", "Irish", "Japanese", "Canadian", "Other"]
    search = request.args.get('search', None)
    whiskeys = Whiskey.get_whiskeys(data, filters, search)
    user = User.get_by_id(data)
    
    return render_template("top_whiskey.html", sort_by_rating=sort_by_rating, whiskeys=whiskeys, user=user, categories = categories)


# Route for displaying user's whiskey shelf
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

    categories = ["All", "Bourbon", "Scotch", "Irish", "Japanese", "Canadian", "Other"]

    recent = Whiskey.get_recently_rated_whiskeys(data)
    whiskeys = Whiskey.get_all_rated_whiskeys(data, filters)
    user = User.get_by_id(data)
    
    return render_template("myshelf.html", sort_by_rating=sort_by_rating, whiskeys=whiskeys, user=user, recent = recent, categories = categories)

# Route for displaying the form to create a new whiskey entry
@app.route('/whiskeys/new')
def create_whiskey_view():
    if 'user_id' not in session:
        return redirect ("/")
    data = {
        "id": session['user_id']
    }
    user = User.get_by_id(data)
    return render_template("create_whiskey.html", user=user)


# Route for displaying a single whiskey entry
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


# Route for displaying the form to edit a whiskey entry
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


# Route for deleting a whiskey entry
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


# Route for creating a new whiskey entry with form data
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
            flash('No selected file', "register")
            return redirect("/whiskeys/new")
        
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
            
            # Save the uploaded image file to the specified path
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{file_name}.{file_type}")
            file.save(file_path)
            
            # Compress and save the image
            compress_and_save_image(file_path)
            
            # Redirect to the user's whiskey shelf
            return redirect('/myshelf')
        else:
            # If the file has an invalid format, display an error message and redirect to the whiskey creation form
            flash('Invalid file format', "register")
            return redirect('/whiskeys/new')
    else: 
        # If the form data is invalid, redirect to the whiskey creation form
        return redirect('/whiskeys/new')
    


# Route for serving uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    
    
# Route for editing a whiskey entry with form data
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


