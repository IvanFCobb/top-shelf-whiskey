from app.config.mysqlconnection import connectToMySQL
from app.models import whiskey
from app.models import user
from app.models import rating


class Reply:
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.user_id = data['user_id']
        self.comment_id = data['comment_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None




    @classmethod
    def get_replies_by_comment_id(cls, data):
        query = """SELECT replies.*, users.id AS user_id, users.username AS username, users.email AS email,
                   users.password AS password, users.created_at AS user_created_at, users.updated_at AS user_updated_at, replies.user_id as reply_creator
                   FROM replies
                   JOIN users ON replies.user_id = users.id
                   JOIN comments ON replies.comment_id = comments.id
                   WHERE comments.id = %(id)s
                   ORDER BY comments.created_at ASC;"""
                   
        results = connectToMySQL("whiskeydb").query_db(query, data)
        replies = []
        for row in results:
            one_reply = cls(row)
            one_reply_creator_info = {
                "id": row['reply_creator'], 
                "username": row['username'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['user_created_at'],
                "updated_at": row['user_updated_at'],
            }
            creator = user.User(one_reply_creator_info)
            one_reply.creator = creator
            replies.append(one_reply)
        return replies


    @classmethod
    def save(cls, data):
        query = """INSERT INTO replies (content, user_id, comment_id)
                   VALUES (%(content)s, %(user_id)s, %(comment_id)s);"""
        return connectToMySQL("whiskeydb").query_db(query, data)



    @classmethod
    def delete_comment(cls, data):
        query = """DELETE FROM replies
                   WHERE comment_id = %(comment_id)s;"""
        return connectToMySQL("whiskeydb").query_db(query, data)
    
    
    @classmethod
    def delete(cls, data):
        query = """DELETE FROM replies
                   WHERE replies.id = %(reply_id)s and replies.user_id = %(user_id)s;"""
        return connectToMySQL("whiskeydb").query_db(query, data)


