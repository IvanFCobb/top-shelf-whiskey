from app.config.mysqlconnection import connectToMySQL
from flask import flash
from app.models import user


class Whiskey:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.category = data['category']
        self.distillery = data['distillery']
        self.age = data['age']
        self.abv = '{0:.1f}'.format(data['abv'])
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.rating = data['rating']
        self.creator = None
        self.users_who_rated = []
        self.number_of_ratings = []
        


    
    
    
    @classmethod
    def get_all_rated_whiskeys(cls, data):
        query = f"select * from ratings join whiskeys on whiskeys.id = whiskey_id  join users on whiskeys.user_id = users.id where ratings.User_id = {data['id']} ORDER BY rating {data['sort_order']};"
        results = connectToMySQL('whiskeydb').query_db(query, data)
        all_whiskeys = []
        for row in results:
            row["id"] = row["whiskey_id"]
            one_whiskey = cls(row)
            one_whiskeys_creator_info = {
                "id": row['user_id'], 
                "username": row['username'],
                "email": row['email'],
                "password": row['password'],
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at'],
            }
            creator = user.User(one_whiskeys_creator_info)
            one_whiskey.creator = creator
            all_whiskeys.append(one_whiskey)
        return all_whiskeys
    



    @classmethod
    def get_by_id_with_creator(cls, id):
        query = "SELECT * FROM whiskeys JOIN users ON whiskeys.user_id = users.id LEFT JOIN ratings on ratings.whiskey_id = whiskeys.id WHERE whiskeys.id = '{}';".format(id)
        results = connectToMySQL('whiskeydb').query_db(query)
        whiskey = cls(results[0])
        whiskey_creator_info = {
                "id": results[0]["user_id"], 
                "first_name": results[0]["first_name"],
                "last_name": results[0]["last_name"],
                "email": results[0]["email"],
                "password": results[0]["password"],
                "created_at": results[0]["users.created_at"],
                "updated_at": results[0]["users.updated_at"]
            }
        for row in results:
            if row['whiskey_id'] == None:
                break
            data = {
            "whiskey_id": row['whiskey_id'],
            "user_id": row['User_id']
            }
            whiskey.number_of_ratings.append(data)
        creator = user.User(whiskey_creator_info)
        whiskey.creator = creator
        return whiskey
    
    
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO whiskeys ( title, description, price, quantity, user_id, created_at, updated_at ) VALUES ( %(title)s, %(description)s, %(price)s, %(quantity)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL('whiskeydb').query_db(query, data)
    
    
    
    @classmethod
    def edit(cls, data):
        query = "UPDATE whiskeys SET title = %(title)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s, updated_at = now() WHERE (id = {});".format(
            data["id"])
        return connectToMySQL('whiskeydb').query_db(query, data)
    
    
    
    @classmethod
    def delete(cls, num):
        query_ratings = "DELETE FROM ratings WHERE (whiskey_id = {});".format(
            num)
        query = "DELETE FROM whiskeys WHERE (id = {});".format(
            num)
        connectToMySQL('whiskeys').query_db(query_ratings)
        return connectToMySQL('whiskeydb').query_db(query)
       
    

    @staticmethod
    def is_valid_whiskey(data):
        is_valid = True
        if len(data['title']) < 2:
            flash("Title must be at least 2 characters", "whiskey")
            is_valid = False
        if len(data['description']) < 9:
            flash("Description must be at least 10 characters", "whiskey")
            is_valid = False
        if len(data['price']) < 1:
            flash("Price Required", "whiskey")
            is_valid = False
        if len(data['price']) > 0:
            if float(data['price']) <= 0:
                flash("Price must be greater than 0", "whiskey")
                is_valid = False
        if len(data['quantity']) < 1:
            flash("Quantity Required", "whiskey")
            is_valid = False
        if len(data['quantity']) > 0:
            if float(data['quantity']) <= 0:
                flash("Quantity must be greater than 0", "whiskey")
                is_valid = False
        return is_valid

    

