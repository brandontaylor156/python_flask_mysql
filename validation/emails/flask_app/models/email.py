from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import email
from flask_app import flash
import re, pprint

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
DATABASE = 'emails_schema'

class Email:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']

    @classmethod
    def select_all(cls):
        query = "SELECT * FROM emails;"
        results = connectToMySQL(DATABASE).query_db(query)
        emails = []
        for result in results:
            emails.append( Email(result) )
        return emails

    @classmethod
    def insert_one(cls, data):
        query = "INSERT INTO emails (name) VALUES (%(name)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @staticmethod
    def validate_email(email):
        is_valid = True
        if not EMAIL_REGEX.match(email['name']):
            flash("Email is not valid!")
            is_valid = False
        else:
            flash(f"The email address you added ({email['name']}) is a VALID email address! Thank you!")
        return is_valid


        

        

