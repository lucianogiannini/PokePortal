from database import db
import requests
import json

class Location(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(255))
  pokemon_encounters = db.Column(db.String(255))
  url = db.Column(db.String(255))

  def __init__(self, name, url):
    self.url = url
    self.name = name
    self.pokemon_encounters = []
    self.fetchData()
    self.pushToDB()

  def fetchData(self):
    res = requests.get(self.url)
    data = res.json()
    if res.status_code == 200:
      self.id = data['id']
      areas = data['areas']
      for area in areas:
        self.get_pokemon_encounters(area)
      self.pokemon_encounters = json.dumps(self.pokemon_encounters)
    else:
      return None

  def get_pokemon_encounters(self, area):
    res = requests.get(area['url'])
    data = res.json()
    if res.status_code == 200:
      for encounter in data['pokemon_encounters']:
        self.pokemon_encounters.append(encounter['pokemon']['name'])
    else:
      return None
  
  def pushToDB(self):
    if not db.session.query(Location).where(Location.id == self.id).first():
      db.session.add(self)
    print(self.id)
    db.session.commit()
    return 'Location added'