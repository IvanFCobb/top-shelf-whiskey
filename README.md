# Top Shelf Whiskey

Top Shelf Whiskey is a Flask-based web application that allows users to keep track of their favorite whiskeys, rate them, and discover new top-rated whiskeys. Users can register, log in, and manage their whiskey collections by creating, editing, and deleting whiskey entries. The app also supports image uploads and serves them from a specified directory.

## Features

- User Registration, Login, and Logout
- User Authentication
- File Upload for Whiskey Images
- Top Whiskeys Page with Sorting, Filtering, and Searching
- My Whiskey Shelf Page with Sorting, Filtering, and Recent Ratings
- Create, View, Edit, and Delete Whiskey Entries
- Image Serving from a Specified Directory

## Installation

1. Clone the repository:

```
git clone https://github.com/yourusername/top-shelf-whiskey.git
```

2. Create a virtual environment and activate it:

```
python3 -m venv venv
source venv/bin/activate
```

3. Install the required dependencies:

```
pip install -r requirements.txt
pip install pillow
```

4. Run the application:

```
python server.py
```

The application will be available at `http://127.0.0.1:5000/`.

## Usage

1. Register for an account or log in using an existing one.
2. Upload images of your favorite whiskey bottles.
3. Add new whiskey entries with details such as name, category, distillery, age, and ABV.
4. Rate and manage your whiskey collection on your whiskey shelf.
5. Discover top-rated whiskeys and filter them based on your preferences.

## Contributing

Contributions are welcome! Please create an issue to discuss proposed changes or submit a pull request.

1. Fork the repository.
2. Create a new branch for your changes: `git checkout -b feature/name-of-feature`.
3. Commit your changes: `git commit -m "Add some feature"`.
4. Push the branch: `git push origin feature/name-of-feature`.
5. Create a pull request.
