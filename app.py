from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from database import db
from flask_bootstrap import Bootstrap
from models.Pokemon import Pokemon
from models.Location import Location
from models.Region import Region
from models.User import User
from urllib.parse import unquote as urllib_unquote
import json
import ast
import numpy as np
import os


app = Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myapp.db'
db.init_app(app)

user = None

def check_user():
  global user
  user = db.session.query(User).first()


@app.template_filter('unquote')
def unquote(url):
    safe = app.jinja_env.filters['safe']
    return safe(urllib_unquote(url))

@app.template_filter()
def formatlocation(word):
  if 'kalos-' in word:
    word = word.replace('kalos-', '')
  word = word.replace('-', ' ').title()
  return word

@app.template_filter()
def formatpokemon(word):
  word = word.replace('-', ' ').title()
  return word

@app.template_filter()
def formatname(word):
  word = word.replace('-', ' ').title()
  return word

@app.template_filter()
def formattype(word):
  return url_for('static', filename='Image/'+word+'.gif')

@app.template_filter()
def formatmove(word):
  word = word.replace('-', ' ').title()
  return word

@app.template_filter()
def check_in_collection(word):
  collection = json.loads(user.pokemon_collection)
  if word in collection:
    return True
  else:
    return False


@app.route('/')
def index():
    return redirect(url_for('map'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    check_user()
    global user
    if request.method == 'GET':
      return render_template('login.html')
    else:
      username = request.form['username']
      password = request.form['password']
      usr = db.session.query(User).where(User.username == username).first()
      if usr is None:
        user = User(username, password)
        return redirect(url_for('map'))
      if usr.password == password:
        user = usr
        return redirect(url_for('map'))
      else:
        return redirect(url_for('login'))

@app.route('/add/<pokemon>', methods=['POST'])
def add(pokemon):
  check_user()
  global user
  user.addPokemon(pokemon)
  user = db.session.query(User).where(User.username == user.username).first()
  return 'Pokemon added'

@app.route('/my_collection', methods=['GET'])
def my_collection():
  check_user()
  pokemons = ast.literal_eval(user.pokemon_collection)
  pokemons = db.session.query(Pokemon).where(Pokemon.name.in_(pokemons)).all()
  pokemons_split = []
  temp = []
  count = 0
  for pokemon in pokemons:
    pokemon.sprites = ast.literal_eval(pokemon.sprites)
    temp.append(pokemon)
    
    if count == 4:
      pokemons_split.append(temp)
      temp = []
      count = 0
    count += 1
  if len(temp) != 0:
    pokemons_split.append(temp)
  return render_template('my_collection.html', pokemons=pokemons_split)

@app.route('/map')
def map():
  check_user()
  locations = db.session.query(Location).all()
  location_names = [location.name for location in locations]
  location_names = json.dumps(location_names)
  pokemons = db.session.query(Pokemon).where(Pokemon.encounter_locations != '[]').all()
  pokemon_names = {pokemon.name:ast.literal_eval(pokemon.encounter_locations) for pokemon in pokemons}
  return render_template('map.html', locations=location_names, pokemons=pokemon_names, type='None')

@app.route('/map_filter', methods=['POST'])
def map_filter():
  check_user()
  type_ = request.form['type']
  locations = db.session.query(Location).all()
  location_names = [location.name for location in locations]
  location_names = json.dumps(location_names)
  pokemons = db.session.query(Pokemon).where(Pokemon.encounter_locations != '[]').where(Pokemon.types.contains(type_)).all()
  pokemon_names = {pokemon.name:ast.literal_eval(pokemon.encounter_locations) for pokemon in pokemons}
  return render_template('map.html', locations=location_names, pokemons=pokemon_names, type=type_)

@app.route('/configure_region', methods=['GET','POST'])
def configure_region():
  check_user()
  if request.method == 'POST':
    region = request.form['region']
    Region(region.lower())
    return render_template('config_successful.html', region=region.capitalize())
  else:
    return render_template('config.html')

@app.route('/pokedex', methods=['GET'])
def pokedex():
  check_user()
  pokemons = db.session.query(Pokemon).order_by(Pokemon.id).all()
  for pokemon in pokemons:
    pokemon.encounter_locations = ast.literal_eval(pokemon.encounter_locations)
    pokemon.moves = ast.literal_eval(pokemon.moves)
    pokemon.sprites = ast.literal_eval(pokemon.sprites)
    pokemon.types = ast.literal_eval(pokemon.types)
  pokemons_split = np.array_split(pokemons, int(len(pokemons)/4))
  
  return render_template('pokedex.html', pokemons=pokemons_split, len=int(len(pokemons)/4))

@app.route('/pokemon/<name>', methods=['GET'])
def pokemon(name):
  check_user()
  pokemon = db.session.query(Pokemon).where(Pokemon.name == name).first()
  pokemon.encounter_locations = ast.literal_eval(pokemon.encounter_locations)
  pokemon.moves = ast.literal_eval(pokemon.moves)
  pokemon.sprites = ast.literal_eval(pokemon.sprites)
  pokemon.types = ast.literal_eval(pokemon.types)
  return render_template('pokemon.html', pokemon=pokemon)

@app.route('/search', methods=['GET', 'POST'])
def search():
  check_user()
  if request.method == 'POST':
    query = request.form['search']
    pokemon = query.lower()
    pokemons = db.session.query(Pokemon).where(Pokemon.name.contains(pokemon)).limit(20).all()
    if len(pokemons) == 0:
      return "No pokemon found"
    else:
      names = []
      for p in pokemons:
        names.append(p.name)
      return names
  else:
    return render_template('search.html')

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run()