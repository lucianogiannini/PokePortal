from flask import Flask, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from database import db
from flask_bootstrap import Bootstrap
from models.Message import Message
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


@app.route('/')
def index():
    messages = Message.query.all()
    return render_template('index.html', messages=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global user
    if request.method == 'GET':
      return render_template('login.html', error='')
    else:
      username = request.form['username']
      password = request.form['password']
      usr = db.session.query(User).where(User.username == username).first()
      if usr is None:
        user = User(username, password)
        return render_template('map.html', username=username)
      if usr.password == password:
        user = usr
        return render_template('map.html', username=username)
      else:
        return render_template('login.html', error='Invalid username or password')
@app.route('/submit', methods=['POST'])
def submit():
    content = request.form['content']
    message = Message(content=content)
    db.session.add(message)
    db.session.commit()
    return 'Message added'

@app.route('/map')
def map():
  locations = db.session.query(Location).all()
  location_names = [location.name for location in locations]
  location_names = json.dumps(location_names)
  pokemons = db.session.query(Pokemon).where(Pokemon.encounter_locations != '[]').all()
  pokemon_names = {pokemon.name:ast.literal_eval(pokemon.encounter_locations) for pokemon in pokemons}
  #pokemon_names = json.dumps(pokemon_names)


  
  return render_template('map.html', locations=location_names, pokemons=pokemon_names)

@app.route('/configure_region', methods=['GET','POST'])
def configure_region():
  if request.method == 'POST':
    region = request.form['region']
    Region(region.lower())
    return render_template('config_successful.html', region=region.capitalize())
  else:
    return render_template('config.html')

@app.route('/pokedex', methods=['GET'])
def pokedex():
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
  pokemon = db.session.query(Pokemon).where(Pokemon.name == name).first()
  pokemon.encounter_locations = ast.literal_eval(pokemon.encounter_locations)
  pokemon.moves = ast.literal_eval(pokemon.moves)
  pokemon.sprites = ast.literal_eval(pokemon.sprites)
  pokemon.types = ast.literal_eval(pokemon.types)
  return render_template('pokemon.html', pokemon=pokemon)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    app.run()