from app.config.mysqlconnection import connectToMySQL
from app.models import whiskey
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')



class User:
    def __init__(self, data):
        self.id = data['id']
        self.fname = data['first_name']
        self.lname = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.whiskeys_who_purchased = []



    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = '{}';".format(email)
        results = connectToMySQL('whiskeys').query_db(query)
        if len(results) < 1:
            return False
        return cls(results[0])



    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * from users left join purchases on purchases.User_id = users.id WHERE users.id = %(id)s"
        results = connectToMySQL('whiskeys').query_db(query, data)
        user = cls(results[0])
        for row in results:
            data = row['whiskey_id']

            user.whiskeys_who_purchased.append(data)
        return user



    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email, password, created_at, updated_at) VALUES ( %(fname)s, %(lname)s, %(email)s, %(password)s, NOW() , NOW() );"
        return connectToMySQL('whiskeys').query_db(query, data)


    
    @classmethod
    def add_purchase(cls, data):
        query = "INSERT INTO purchases (user_id, whiskey_id) VALUES ( %(user_id)s, %(whiskey_id)s);"
        return connectToMySQL('whiskeys').query_db(query, data)
    

    
    
    @staticmethod
    def is_valid_user(data):
        is_valid = True
        query = "SELECT * from users WHERE email = %(email)s;"
        results = connectToMySQL('whiskeys').query_db(query, data)
        if data['password'] != data['password_confirm']:
            flash("Confirm Password Does Not Match", "register")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password Must Be More Than 8 Characters", "register")
            is_valid = False
        if len(data['fname']) < 2:
            flash("First Name must be at least 2 characters.", "register")
            is_valid = False
        if len(data['lname']) < 2:
            flash("Last Name must be at least 2 characters.", "register")
            is_valid = False
        if len(results) > 0:
            flash("Email is already taken", "register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "register")
            is_valid = False
        return is_valid

