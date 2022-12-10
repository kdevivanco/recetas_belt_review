from flask import Flask, render_template, request, redirect, Blueprint,session
from app.models.users import User
from app.models.recetas import Recipe
import json
import pdb

recetas = Blueprint('recetas', __name__, template_folder='templates')

@recetas.route('/create')
def show_create():
    if session['user'] == None:
        log = 'login'
        return redirect('/')
    else:
        user_id = session['user']
        log = 'logout'
    
    return render_template('create.html',log=log, id = user_id)



@recetas.route('/create', methods=['POST'])
def create_recipe():
    print(request.form)
    id_receta = Recipe.create_new(request.form)
    
    return redirect('/welcome')


@recetas.route('/recipes/<id>')
def single_recipe(id):
    if session['user'] == None:
        log = 'login'
        return redirect('/')
    else:
        username = User.get_one(session['user']).first_name
        log = 'logout'
    return render_template('single_recipe.html',log = log,username=username)


@recetas.route('/edit/<id>')
def show_edit(id):
    if session['user'] == None:
        log = 'login'
        return redirect('/')
    log = 'logout'
    receta = Recipe.get_one(id)

    return render_template('edit.html',log=log,recipe = receta)

@recetas.route('/edit/<recipe_id>',methods=['POST'])
def edit_recipe(recipe_id):
    if session['user'] == None:
        log = 'login'
        return redirect('/')
    form_data = request.form

    Recipe.update_recipe(recipe_id,form_data)

    return redirect('/welcome') 
    
@recetas.route('/show/<id>')
def show_recipe(id):
    if session['user'] == None:
        log = 'login'
        return redirect('/')
    
    username = User.get_one(session['user']).first_name
    log = 'logout'
    receta = Recipe.get_one(id)
    author = User.get_one(receta.user_id).first_name

    return render_template('single_recipe.html',log=log,recipe = receta,username = username,author=author)

@recetas.route('/delete/<id>')
def delete_recipe(id):
    if session['user'] == None:
        log = 'login'
        return redirect('/')
    
    Recipe.delete(int(id))
    return redirect('/welcome')



