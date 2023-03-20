from database import db
import requests
import json

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    encounter_locations = db.Column(db.String(255))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    types = db.Column(db.String(255))
    moves = db.Column(db.String(255))
    sprites = db.Column(db.String(255))
    
    def __init__(self, id):
        self.url = 'https://pokeapi.co/api/v2/pokemon/'
        self.fetchData(id)

    def formatEncounterLocations(self, encounterURL):
        encounterURL = 'https://pokeapi.co' + str(encounterURL)
        #add request code

    def formatTypes(self, list_):
        types = []
        for tp in list_[0]:
            types.append(tp['type']['name'])
        typesStr = json.dumps(types)
        return typesStr

    def formatMoves(self, list_):
        moves = []
        for move in list_:
            moves.append(move['move']['name'])
        movesStr = json.dumps(moves)
        return movesStr

    def formatSprites(self, dict):
        sprites = []
        sprites.append(dict['front_default'])
        sprites.append(dict['front_shiny'])
        spritesStr = json.dumps(sprites)
        return spritesStr

    def fetchData(self, id):
        self.url = self.url + str(id)
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            self.id = data.id
            self.name = data.name
            self.height = data.height
            self.weight = data.weight
            self.encounter_locations = self.formatEncounterLocations(data.location_area_encounters)
            self.types = self.formatTypes(data.types)
            self.moves = self.formatMoves(data.moves)
            self.sprites = self.formatSprites(data.sprites)
        else:
            return None
    
    def getInformation(self):
        info = dict()
        info['id'] = self.id
        info['name'] = self.name
        info['height'] = self.height
        info['weight'] = self.weight
        info['encounter_locations'] = self.encounter_locations
        info['types'] = self.types
        info['moves'] = self.moves
        info['sprites'] = self.sprites
        return info

    def setInformation(self, info):
        self.id = info['id']
        self.name = info['name']
        self.height = info['height']
        self.weight = info['weight']
        self.encounter_locations = info['encounter_locations']
        self.types = info['types']
        self.moves = info['moves']
        self.sprites = info['sprites']
        self.pushToDB()

    def pushToDB(self):
        db.session.add(self)
        db.session.commit()
        return 'Pokemon added'



