from database import db
import requests
import json

class User(db.Model):
  username = db.Column(db.String(255), primary_key=True)
  password = db.Column(db.String(255))
  pokemon_collection = db.Column(db.String(255))

  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.pokemon_collection = []
    self.pushToDB()
  
  def pushToDB(self):
    if not db.session.query(User).where(User.username == self.username).first():
      db.session.add(self)
    
    self.pokemon_collection = json.dumps(self.pokemon_collection)
    db.session.commit()
    return 'User added'
  
  def addPokemon(self, pokemon):
    self.pokemon_collection.append(pokemon)
    self.pokemon_collection = json.dumps(self.pokemon_collection)
    self.pushToDB()