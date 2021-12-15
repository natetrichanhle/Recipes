from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__ (self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query = 'INSERT INTO users (first_name,last_name,email,password) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);'
        result = connectToMySQL('recipes_schema').query_db(query,data)
        return result

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        if results:    
            return cls(results[0])

    @staticmethod
    def validate_registration(user):
        is_valid = True
        if len(user['first_name']) < 2:
            flash('First name must be atleast 2 characters.','register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash('Last name must be atleast 2 characters.','register')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be atleast 8 characters.','register')
            is_valid = False
        if (user['password'] != user['confirm_password']):
            flash('Passwords do not match','register')
            is_valid = False
        if (User.get_by_email({'email': user['email']})):
            flash('Email already exists')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address!','register')
            is_valid = False
        return is_valid

