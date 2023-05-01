from database import db
import requests
import json
from models.Pokemon import Pokemon
from models.Location import Location

class Region():
  def __init__(self, region):
    self.url = "https://pokeapi.co/api/v2/region/"+region
    self.fetchData()
  
  def fetchData(self):
    res = requests.get(self.url)
    data = res.json()
    if res.status_code == 200:
      self.id = data['id']
      self.name = data['name']
      self.locations = data['locations']
      self.pokedexes = data['pokedexes']
      self.create_locations()
      self.create_pokedexes()
    else:
      return None
    
  def create_locations(self):
    for location in self.locations:
      self.create_location(location)
  
  def create_location(self,loc):
    name = loc['name']
    url = loc['url']
    Location(name, url)
  
  def create_pokedexes(self):
    for pokedex in self.pokedexes:
      self.create_pokedex(pokedex)
    
  def create_pokedex(self, pokedex):
    res = requests.get(pokedex['url'])
    data = res.json()
    for entry in data['pokemon_entries']:
      Pokemon(entry['entry_number'], entry['pokemon_species']['name'])