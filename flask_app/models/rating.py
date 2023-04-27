from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import whiskey
from flask_app.models import user
from flask_app.models import comment


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
    def save(cls, data):
        query = "INSERT INTO ratings ( rating, user_id, whiskey_id) VALUES ( %(rating)s, %(user_id)s, %(whiskey_id)s);"
        return connectToMySQL('whiskeydb').query_db(query, data)

    @classmethod
    def edit(cls, data):
        query = "UPDATE ratings SET rating = %(rating)s WHERE whiskey_id = %(whiskey_id)s;"
        return connectToMySQL('whiskeydb').query_db(query, data)


    @classmethod
    def delete_all_for_one_whiskey(cls, data):
        query = """DELETE FROM ratings
                WHERE ratings.whiskey_id = %(id)s;"""
        return connectToMySQL("whiskeydb").query_db(query, data)