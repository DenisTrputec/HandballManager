import shutil
import os
import classes.database as db


class Game:
    def __init__(self):
        self.name = None
        self.season = 0
        self.week = 0
        self.countries = []
        self.leagues = []
        self.clubs = []
        self.players = []

    def new_game(self, save_name):
        self.name = save_name
        self.season = 1
        self.week = 1
        shutil.copy2("database/default.db", "save/" + save_name + ".db")

    def save_game(self):
        db.save_game(self)

    def load_game(self, save_name):
        self.name = save_name
        db.load_game(self)
