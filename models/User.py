from database import db
import requests
import json
import ast

class User(db.Model):
  username = db.Column(db.String(255), primary_key=True)
  password = db.Column(db.String(255))
  pokemon_collection = db.Column(db.Text())

  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.pokemon_collection = '[]'
    self.pushToDB()
  
  def pushToDB(self):
    db.session.add(self)
    db.session.commit()
    return 'User added'
  
  def addPokemon(self, pokemon):
    pokemons = json.loads(self.pokemon_collection)
    if pokemon not in pokemons:
      pokemons.append(pokemon)
    self.pokemon_collection = json.dumps(pokemons)
    self.pushToDB()