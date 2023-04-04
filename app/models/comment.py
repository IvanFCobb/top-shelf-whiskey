from app.config.mysqlconnection import connectToMySQL
from app.models import whiskey
from app.models import user
from app.models import rating


class Rating:
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['rating']
        self.user_id = data['user_id']
        self.whiskey_id = data['whiskey_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.users_who_rated = []



    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments ( comment, user_id, whiskey_id) VALUES ( %(comment)s, %(user_id)s, %(whiskey_id)s);"
        return connectToMySQL('whiskeydb').query_db(query, data)

    @classmethod
    def edit(cls, data):
        query = "UPDATE comments SET comment = %(comment)s WHERE id = %(id)s;"
        return connectToMySQL('whiskeydb').query_db(query, data)


