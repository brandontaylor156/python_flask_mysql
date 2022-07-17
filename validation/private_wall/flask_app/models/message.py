from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app, flash
from pprint import pprint

DATABASE = 'messages_schema'

class Message:
    def __init__( self , data ):
        self.id = data['id']
        self.message = data['message']
        self.sender_id = data['sender_id']
        self.receiver_id = data['receiver_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def select_all_sent_messages(cls, data):
        query = "SELECT * FROM messages WHERE sender_id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        messages = []
        for result in results:
            messages.append( Message(result) )
        return messages 

    @classmethod
    def insert_message(cls, data):
        query = "INSERT INTO messages (message, sender_id, receiver_id) VALUES (%(message)s, %(sender_id)s, %(receiver_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def delete_message(cls, data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return  

    @staticmethod
    def validate_message(message):
        is_valid = True

        if len(message['message']) < 5:
            flash("Message must be at least 5 characters long.", int(message['contact']))
            is_valid = False

        return is_valid
[]