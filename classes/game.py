import shutil
from random import randint, choice
from classes.database import Database
from classes.player import Player
from classes.player import Position
from classes.contract_offer import Status
from classes.player_statistics_competition import PlayerStatisticsCompetition


class Game:
    def __init__(self):
        self.name = None
        self.season = 1
        self.week = 1
        self.countries = []
        self.leagues = []
        self.clubs = []
        self.players = []
        self.retired_players = []
        self.schedule = []
        self.calendar = []
        self.contract_offers = []

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

    def new_season(self):
        self.update_players_attributes()
        self.retire_players()
        self.season += 1
        self.week = 1

        for league in self.leagues:
            league.next_season()
            for match in league.schedule:
                self.schedule.append(match)

        for club in self.clubs:
            club.players = []

        for player in self.players:
            player.age += 1
            if player.club is not None:
                for club in self.clubs:
                    if player.club.get_id() == club.get_id():
                        club.players.append(player)

        for club in self.clubs:
            club.money -= sum([player.salary for player in club.players])

    def decrease_contract_lengths(self):
        for player in self.players:
            player.contract_length -= 1

    def create_new_players(self):
        positions_cnt = {"GK": 0, "LW": 0, "LB": 0, "CB": 0, "P": 0, "RB": 0, "RW": 0}
        current_player_names = [player.name for player in self.players]

        db = Database(self.name)
        db.open_connection()
        db.cursor.execute("select max(id) from person")
        max_id = db.cursor.fetchall()[0][0]
        db.close_connection()
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
                player = Player(max_id + 1, player_name, age, position, attack, defense, loyalty, league.country,
                                None, 0, 0, 0)
                max_id += 1
                print(player)
                self.players.append(player)

            break   # Only one active league

    def update_contract_offers_list(self):
        for offer in self.contract_offers:
            if offer.status == Status.Accepted:
                offer.player.club = offer.club
                offer.player.salary = offer.salary
                offer.player.contract_length = offer.length

        self.contract_offers = [offer for offer in self.contract_offers if offer.status == Status.Pending]

    def update_players_attributes(self):
        players_sc = []
        for league in self.leagues:
            for player_sc in league.players_sc:
                players_sc.append(player_sc)

        for player in self.players:
            for player_sc in players_sc:
                if player_sc.player.get_id() == player.get_id():
                    player.update_attributes(player_sc)
                    break
            else:
                player.update_attributes(PlayerStatisticsCompetition(player, player.club.league))

    def retire_players(self):
        for player in self.players:
            if player.contract_length == 0:
                player.club = None
                player.salary = 0
                player.injury_length = 0

        self.retired_players = [player for player in self.players if player.club is None and player.age >= 34]
        for player in self.retired_players:
            print(player)

        self.players = [player for player in self.players if player not in self.retired_players]
