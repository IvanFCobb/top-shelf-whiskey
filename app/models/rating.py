from app.config.mysqlconnection import connectToMySQL
from app.models import whiskey
from app.models import user
from flask import flash



class Rating:
    def __init__(self, data):
        self.id = data['id']
        self.rating = data['rating']
        self.user_id = data['user_id']
        self.whiskey_id = data['whiskey_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_who_rated = []



    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = '{}';".format(email)
        results = connectToMySQL('whiskeydb').query_db(query)
        if len(results) < 1:
            return False
        return cls(results[0])



    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * from users left join ratings on ratings.User_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL('whiskeydb').query_db(query, data)
        user = cls(results[0])
        for row in results:
            data = row['whiskey_id']
            user.whiskeys_who_rated.append(data)
        return user



    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( username, email, password) VALUES (%(username)s, %(email)s, %(password)s);"
        return connectToMySQL('whiskeydb').query_db(query, data)


    
    @classmethod
    def add_rating(cls, data):
        query = "INSERT INTO rates (user_id, whiskey_id) VALUES ( %(user_id)s, %(whiskey_id)s);"
        return connectToMySQL('whiskeydb').query_db(query, data)
    

    
    
    @staticmethod
    def is_valid_user(data):
        is_valid = True
        query = "SELECT * from users WHERE email = %(email)s;"
        results = connectToMySQL('whiskeydb').query_db(query, data)
        if data['password'] != data['password_confirm']:
            flash("Confirm Password Does Not Match", "register")
            is_valid = False
        if len(data['password']) < 3:
            flash("Password Must Be More Than 3 Characters", "register")
            is_valid = False
        if len(data['username']) < 3:
            flash("username must be at least 3 characters.", "register")
            is_valid = False
        if len(results) > 0:
            flash("Email is already taken", "register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "register")
            is_valid = False
        return is_valid

