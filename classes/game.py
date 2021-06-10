import shutil
from random import randint, choice
from classes.database import Database
from classes.player import Player
from classes.player import Position


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

    def decrease_contract_lengths(self):
        for player in self.players:
            player.contract_length -= 1

    def create_new_players(self):
        positions_cnt = {"GK": 0, "LW": 0, "LB": 0, "CB": 0, "P": 0, "RB": 0, "RW": 0}
        current_player_names = [player.name for player in self.players]

        db = Database(self.name)
        for league in self.leagues:
            first_names, last_names = db.return_names(league.country.get_id())
            for i in range(len(league.teams)):
                # Set player name
                while True:
                    player_name = choice(first_names) + '.' + choice(last_names)
                    if player_name not in current_player_names:
                        current_player_names.append(player_name)
                        break

                # Set player position
                while True:
                    position = choice(list(Position))
                    for key in positions_cnt.keys():
                        if position.name == key and positions_cnt[key] < 2:
                            positions_cnt[key] += 1
                            break
                    else:
                        continue  # only executed if the inner loop did NOT break
                    break

                age = 17
                if position == Position.GK:
                    attack = 0
                    defense = randint(1, 2)
                else:
                    attack = randint(1, 2)
                    defense = randint(1, 2)
                loyalty = randint(1, 5)
                player = Player(None, player_name, age, position, attack, defense, loyalty, league.country, None, 0, 0, 0)
                print(player)
                self.players.append(player)

            break   # Only one active league

