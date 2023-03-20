from database import db
import requests

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    encounter_locations = db.Column(db.String(255))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    types = db.Column(db.String(255))
    abilities = db.Column(db.String(255))
    moves = db.Column(db.String(255))
    sprites = db.Column(db.String(255))
    url = 'https://pokeapi.co/api/v2/pokemon/'


    def formatEncounterLocations(self, encounterURL):
        encounterURL = 'https://pokeapi.co' + str(encounterURL)
        #add resquest code

    def formatTypes(self, list_):
        types = []
        for tp in list_[0]:
            types.append(tp['type']['name'])
        typesStr = types.json()
        return typesStr

    def getInformation(self, id):
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
            self.abilites = self.formatAbilites(data.abilities)
            self.moves = self.formatMoves(data.moves)
            self.sprites = self.formatSprites(data.sprites)
        else:
            return None
    
    


