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
        self.team_statistics = []
        self.schedule = []

    def new_game(self, save_name):
        self.name = save_name
        shutil.copy2("database/default.db", "save/" + save_name + ".db")
        db.new_game(self)
        db.load_game(self)
        for league in self.leagues:
            league.create_schedule()
        db.insert_match(self)

    def save_game(self):
        db.save_game(self)

    def load_game(self, save_name):
        self.name = save_name
        db.load_game(self)
