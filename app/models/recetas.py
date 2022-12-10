from app.config.connections import MySQLConnection, connectToMySQL
from flask import flash
import re	
from app import app
import pdb
from flask_bcrypt import Bcrypt        
import datetime
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_cooked = data['date_cooked']
        self.under_thirty = data['under_thirty']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        
    @classmethod
    def get_all(cls):
        
        query = 'SELECT * FROM recipes'

        results = connectToMySQL('recetas').query_db('select * from recipes')
        
        recipes = []

        for recipe in results:
            recipes.append(cls(recipe))
        
        return recipes


    @staticmethod
    def validate_recipe(cls,form_data):
        pass

        
    @classmethod
    def create_new(cls,form_data):
        
        date = datetime.datetime.strptime(form_data['date'], "%d-%m-%Y").strftime("%Y-%m-%d")

        query = '''
                INSERT INTO recipes ( name , description ,date_cooked, under_thirty, instructions , created_at, updated_at,user_id ) 
                VALUES ( %(name)s , %(description)s ,%(date_cooked)s, %(under_thirty)s, %(instructions)s , NOW() , NOW(), %(user_id)s);
                '''

        data = {
                "name": form_data["name"],
                "description" : form_data["description"],
                "instructions" : form_data["instructions"],
                "date_cooked" : date,
                "under_thirty" : form_data["under_thirty"],
                "user_id" : form_data["user_id"],
            }

        return connectToMySQL('recetas').query_db(query,data) #ID DE LA RECETA

    @classmethod
    def get_one(cls,id):
        
        query = '''SELECT * FROM recipes where id = %(id)s '''

        data = {
            "id": id
        }
        results = connectToMySQL('recetas').query_db(query,data)
        
        if len(results) == 0:
            print('no recipe matches id')
            return False
        recipe = results[0]
        
        return cls(recipe)

    @classmethod
    def get_all(cls):
        query = '''
                select * from recipes
                join users on users.id = recipes.user_id;
                '''
        
        results = connectToMySQL('recetas').query_db(query)
        print(results)
        return results

    @classmethod
    def update_recipe(cls,recipe_id,form_data):
        print(form_data)
        query = '''
                UPDATE recipes 
                SET name=%(name)s,
                description=%(description)s,
                instructions=%(instructions)s,
                under_thirty=%(under_thirty)s
                where id =%(id)s;
                '''
        data = {
            'name': form_data['name'],
            'description': form_data['description'],
            'instructions': form_data['instructions'],
            'under_thirty': form_data['under_thirty'],
            'id': recipe_id
        }

        connectToMySQL('recetas').query_db(query,data)

        return

    @classmethod
    def delete(cls,id):
        query = '''DELETE FROM recipes where id = %(id)s; '''

        data = {
            "id": id
        }
        return connectToMySQL('recetas').query_db(query,data)
        