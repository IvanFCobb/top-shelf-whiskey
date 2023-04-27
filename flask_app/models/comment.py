from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import whiskey
from flask_app.models import user
from flask_app.models import rating
from flask_app.models import reply

class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.user_id = data['user_id']
        self.whiskey_id = data['whiskey_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        self.replies = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]



    @classmethod
    def get_comments_by_whiskey_id(cls, data):
        query = """SELECT comments.*, users.id AS user_id, users.username AS username, users.email AS email,
                          users.password AS password, users.created_at AS user_created_at, 
                          users.updated_at AS user_updated_at
                   FROM comments
                   JOIN users ON comments.user_id = users.id
                   WHERE comments.whiskey_id = %(id)s
                   ORDER BY comments.created_at ASC;"""
        results = connectToMySQL("whiskeydb").query_db(query, data)
        comments = []
        for row in results:
            one_comment = cls(row)
            one_whiskeys_creator_info = {
                "id": row['user_id'], 
                "username": row['username'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['user_created_at'],
                "updated_at": row['user_updated_at'],
            }
            creator = user.User(one_whiskeys_creator_info)
            one_comment.creator = creator
            comments.append(one_comment)
            data = {
                "id": one_comment.id
            }
            one_comment.replies = reply.Reply.get_replies_by_comment_id(data)
        return comments


    @classmethod
    def save(cls, data):
        query = """INSERT INTO comments (comment, user_id, whiskey_id)
                   VALUES (%(comment)s, %(user_id)s, %(whiskey_id)s);"""
        return connectToMySQL("whiskeydb").query_db(query, data)



    @classmethod
    def delete(cls, data):
        query = """DELETE FROM comments
                   WHERE comments.id = %(comment_id)s and comments.user_id = %(user_id)s;"""
        return connectToMySQL("whiskeydb").query_db(query, data)


    @classmethod
    def delete_all_whiskey_comments(cls, data):
        query = """DELETE FROM comments
                WHERE comments.whiskey_id = %(id)s;"""
        return connectToMySQL("whiskeydb").query_db(query, data)

