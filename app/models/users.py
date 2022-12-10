from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
import pdb
from flask_bcrypt import Bcrypt        
import json
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all(cls):
        
        query = 'SELECT * FROM users'

        results = connectToMySQL('recetas').query_db('select * from users')
        
        users = []

        for user in results:
            users.append(cls(user))
        
        return users

    @classmethod
    def is_valid(cls,email):
        pass

    @staticmethod
    def validate_user(form_data):
        is_valid = True
        if len(form_data['first_name']) < 2:
            flash("Name must be at least 2 characters.",'email')
            is_valid = False
        if len(form_data['last_name']) < 2:
            flash("Last name must be at least 2 characters.",'email')
            is_valid = False
        if not EMAIL_REGEX.match(form_data['email']): 
            flash("Invalid email address!",'email')
            is_valid = False
        if len(form_data['password']) < 8:
            flash("Password must be at least 8 characters.",'email')
            is_valid = False
        if form_data["password"] != form_data["confirm_password"]:
            flash('Passwords must match!','error')
            is_valid = False
        flash('User created!', 'success')
        return is_valid

    @classmethod
    def email_free(cls,form_data):
        query = '''
                SELECT * FROM users where email = %(email)s
        '''
        
        data = {
            'email' : form_data['email']
        }

        results = connectToMySQL('recetas').query_db(query, data)
        
        if len(results) == 0:
            return True
        else:
            flash("Email already in database",'email')
            print( 'Email not available')
            return False


        
    @classmethod
    def create_new(cls,form_data):

        #HASH THE PASSWORD
        password = bcrypt.generate_password_hash(form_data["password"])
        print(password)


        query = '''
                INSERT INTO users ( first_name ,last_name, email , password , created_at, updated_at ) 
                VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s , NOW() , NOW());
                '''

        data = {
                "first_name": form_data["first_name"],
                "last_name":form_data["last_name"],
                "email" : form_data["email"],
                "password" : password
            }
        
        
        flash('Register  succesful!','success')

        return  connectToMySQL('recetas').query_db(query,data)

    @classmethod
    def login(cls,form_data):
        print(form_data['email'])
        query = '''
                SELECT * FROM users where email = %(email)s;
                '''
        
        data = {
            "email":form_data['email']
        }

        results= connectToMySQL('recetas').query_db(query,data)

        if len(results) == 0:
            flash('User not registered','error')
            print('User not in database')
            return False

        user =cls(results[0])
        print(user)
        result = bcrypt.check_password_hash(user.password,form_data['password'])

        if result == True:
            return user
        else:
            flash('Invalid credentials','error')
            return False

    @classmethod
    def get_one(cls,user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        data = {
            'id' : user_id
        }
        results = connectToMySQL('recetas').query_db(query,data)

        if len(results) == 0:
            return False 
        return (cls(results[0]))
