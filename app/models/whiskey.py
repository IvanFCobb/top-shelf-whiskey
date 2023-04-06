from app.config.mysqlconnection import connectToMySQL
from flask import flash
from app.models import user
from app.models import rating
from app.models import comment


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
        self.creator = None
        self.rating = None
        
    
    
    @classmethod
    def get_whiskeys(cls, data, filters, search=None ):
        query_conditions = []

        # Iterate over the filters and add them to the query_conditions list
        if filters:
            for key, value in filters.items():
                if value and value.lower() != 'all':
                    query_conditions.append(f"{key} = '{value}'")

        # If a search term is provided, add a LIKE condition to the query_conditions list
        if search:
            search_term = f"%{search}%"
            query_conditions.append(f"whiskeys.name LIKE '{search_term}'")

        # If there are any conditions in the query_conditions list, create the SQL query with the conditions
        if query_conditions:
            query_conditions_str = ' AND '.join(query_conditions)
            query = f"SELECT round(avg(rating), 1) rating, whiskey_id, whiskeys.name, whiskeys.category, whiskeys.distillery, whiskeys.age, whiskeys.created_at, whiskeys.updated_at, whiskeys.user_id, whiskeys.abv, whiskeys.id FROM whiskeys LEFT JOIN ratings ON whiskey_id = whiskeys.id WHERE {query_conditions_str} GROUP BY whiskeys.id ORDER BY rating {data['sort_order']};"
        else:
            query = f"SELECT round(avg(rating), 1) rating, whiskey_id, whiskeys.name, whiskeys.category, whiskeys.distillery, whiskeys.age, whiskeys.created_at, whiskeys.updated_at, whiskeys.user_id, whiskeys.abv, whiskeys.id FROM whiskeys LEFT JOIN ratings ON whiskey_id = whiskeys.id GROUP BY whiskeys.id ORDER BY rating {data['sort_order']};"

        results = connectToMySQL('whiskeydb').query_db(query) 
        all_whiskeys = []
        for row in results:
            one_whiskey = cls(row)
            one_whiskeys_rating_info = {
                "id": row['id'], 
                "rating": row['rating'], 
                "whiskey_id": row['whiskey_id'],
                "user_id": row['user_id'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at'],
            }
            userRating = rating.Rating(one_whiskeys_rating_info)
            one_whiskey.rating = userRating
            all_whiskeys.append(one_whiskey)
        return all_whiskeys
    
    
    
    @classmethod
    def get_all_rated_whiskeys(cls, data, filters, search=None):
        query_conditions = []

        # Iterate over the filters and add them to the query_conditions list
        if filters:
            for key, value in filters.items():
                if value and value.lower() != 'all':
                    query_conditions.append(f"{key} = '{value}'")

        # If a search term is provided, add a LIKE condition to the query_conditions list
        if search:
            search_term = f"%{search}%"
            query_conditions.append(f"whiskeys.name LIKE '{search_term}'")

        # If there are any conditions in the query_conditions list, create the SQL query with the conditions
        if query_conditions:
            query_conditions_str = ' AND '.join(query_conditions)
            query = f"SELECT * from ratings JOIN whiskeys on whiskeys.id = whiskey_id  JOIN users on whiskeys.user_id = users.id WHERE ratings.User_id = {data['id']} AND {query_conditions_str} ORDER BY rating {data['sort_order']};"
        else:
            query = f"SELECT * from ratings JOIN whiskeys on whiskeys.id = whiskey_id  JOIN users on whiskeys.user_id = users.id WHERE ratings.User_id = {data['id']} ORDER BY rating {data['sort_order']};"

        results = connectToMySQL('whiskeydb').query_db(query) 
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
            one_whiskeys_rating_info = {
                "id": row['id'], 
                "rating": row['rating'], 
                "whiskey_id": row['whiskey_id'],
                "user_id": row['user_id'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at'],
            }
            userRating = rating.Rating(one_whiskeys_rating_info)
            one_whiskey.rating = userRating
            creator = user.User(one_whiskeys_creator_info)
            one_whiskey.creator = creator
            all_whiskeys.append(one_whiskey)
        return all_whiskeys
    
    
    
    
    @classmethod
    def get_recently_rated_whiskeys(cls, data):
        query = f"select * from ratings join whiskeys on whiskeys.id = whiskey_id  join users on whiskeys.user_id = users.id where ratings.User_id = {data['id']} ORDER BY ratings.updated_at DESC LIMIT 4;"
        results = connectToMySQL('whiskeydb').query_db(query, data)
        recent_whiskeys = []
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
            one_whiskeys_rating_info = {
                "id": row['id'], 
                "rating": row['rating'], 
                "whiskey_id": row['whiskey_id'],
                "user_id": row['user_id'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at'],
            }
            userRating = rating.Rating(one_whiskeys_rating_info)
            one_whiskey.rating = userRating
            recent_whiskeys.append(one_whiskey)
        return recent_whiskeys 
    
    
    @classmethod
    def get_whiskey_with_user_rating(cls, data, whiskey_data):
        query = f"select *, ratings.user_id as rater_id , whiskeys.id as current_whiskey_id, whiskeys.user_id as whiskey_creator  from whiskeys left join ratings on whiskeys.id = whiskey_id AND ratings.user_id = {data['id']} left join users on users.id = ratings.user_id where whiskeys.id = {whiskey_data['id']};"
        results = connectToMySQL('whiskeydb').query_db(query, data)
        results[0]["id"] = results[0]["current_whiskey_id"]
        one_whiskey = cls(results[0])
        one_whiskeys_creator_info = {
            "id": results[0]['whiskey_creator'], 
            "username": results[0]['username'],
            "email": results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at'],
        }
        one_whiskeys_rating_info = {
            "id": results[0]['user_id'], 
            "rating": results[0]['rating'],
            "user_id": results[0]['user_id'],
            "whiskey_id": results[0]['whiskey_id'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at'],
        }
        creator = user.User(one_whiskeys_creator_info)
        one_whiskey.creator = creator
        userRating = rating.Rating(one_whiskeys_rating_info)
        one_whiskey.rating = userRating
        

        return  one_whiskey

    
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO whiskeys ( name, category, distillery, age, abv, user_id) VALUES ( %(name)s, %(category)s, %(distillery)s, %(age)s, %(abv)s, %(user_id)s);"
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
        if len(data['name']) < 1:
            flash("Title must be at least 2 characters", "whiskey")
            is_valid = False
        if len(data['category']) < 1:
            flash("Description must be at least 10 characters", "whiskey")
            is_valid = False
        if len(data['distillery']) < 1:
            flash("Price Required", "whiskey")
            is_valid = False
        if len(data['age']) > 0:
            if float(data['age']) <= 0:
                flash("Price must be greater than 0", "whiskey")
                is_valid = False
        if len(data['abv']) < 1:
            flash("Quantity Required", "whiskey")
            is_valid = False
        if len(data['rating']) > 0:
            if float(data['rating']) <= 0:
                flash("Quantity must be greater than 0", "whiskey")
                is_valid = False
        return is_valid

    

