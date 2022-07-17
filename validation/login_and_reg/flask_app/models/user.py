from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask_app import app, flash
from pprint import pprint
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
PASSWORD_REGEX = re.compile(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$")
DATABASE = 'login_and_reg'

class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def select_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        users = []
        for result in results:
            users.append( User(result) )
        return users

    @classmethod
    def insert_one(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def select_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query, data)
        
        if len(result) < 1:
            return False
        
        return User(result[0])
    
    @staticmethod
    def validate_user(user):
        is_valid = True

        if len(user['first_name']) < 3:
            flash("First name must be at least 3 characters.", 'first_name')
            is_valid = False
        if user['first_name'].isalpha() == False:
            flash("First name must be letters.", 'first_name')
            is_valid = False

        if len(user['last_name']) < 3:
            flash("Last name must be at least 3 characters.", 'last_name')
            is_valid = False
        if user['last_name'].isalpha() == False:
            flash("Last name must be letters.", 'last_name')

        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'email')
            is_valid = False

        users = User.select_all()
        for user_iterator in users:
            if user_iterator.email == user['email']:
                flash("Email already being used.", 'email')
                is_valid = False

        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", 'password')
            is_valid = False

        if user['password'] != user['confirm']:
            flash("Passwords do not match.", 'confirm')
            is_valid = False

        if not PASSWORD_REGEX.match(user['password']):
            flash("Password must contain at least one digit, one uppercase letter, one lowercase letter, and one special character.", 'password')
            is_valid = False
        

        return is_valid

    # @classmethod
    # def get_all_relationships(cls, data):
    #     query = "SELECT * FROM users LEFT JOIN favorites ON users.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE users.id = %(id)s"

    #     results = connectToMySQL(DATABASE).query_db(query, data)

    #     author = Author(results[0])

    #     for result in results:
    #         book_dict = {
    #             'id': result['books.id'], 
    #             'title': result['title'], 
    #             'num_of_pages': result['num_of_pages'],
    #             'created_at': result['books.created_at'], 
    #             'updated_at': result['books.updated_at']
    #         }
    #         author.books.append(book.Book(book_dict))
    #     return author
        