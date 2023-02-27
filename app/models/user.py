from app.config.mysqlconnection import connectToMySQL
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

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users_login').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_by_email(cls, email):
        query = "SELECT * FROM users WHERE email = '{}';".format(email)
        results = connectToMySQL('users_login').query_db(query)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM users WHERE id = '{}';".format(id)
        results = connectToMySQL('users_login').query_db(query)
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email, password, created_at, updated_at) VALUES ( %(fname)s, %(lname)s, %(email)s, %(password)s, NOW() , NOW() );"
        return connectToMySQL('users_login').query_db(query, data)
