import shutil
from classes.database import Database


class Game:
    def __init__(self):
        self.name = None
        self.season = 1
        self.week = 1
        self.countries = []
        self.leagues = []
        self.clubs = []
        self.players = []
        self.schedule = []
        self.calendar = []

    def new_game(self, save_name):
        self.name = save_name
        db = Database(save_name)
        shutil.copy2("database/default.db", "save/" + save_name + ".db")
        db.new_game(self)

    def save_game(self):
        db = Database(self.name)
        db.save_game(self)

    def load_game(self, save_name):
        self.name = save_name
        db = Database(save_name)
        db.load_game(self)
