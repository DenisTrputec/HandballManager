from classes.player_statistics_match import PlayerStatisticsMatch
import random


class Match:
    def __init__(self, competition, rnd, home_club, away_club, time=0, home_goals=0, away_goals=0):
        self.competition = competition
        self.round = rnd
        self.home = home_club
        self.away = away_club
        self.time = time
        self.home_goals = home_goals
        self.away_goals = away_goals
        self.home_players = []
        self.away_players = []

    def __str__(self):
        return f"Round:{self.round} {self.home.name}-{self.away.name} {self.home_goals}:{self.away_goals}"

    def create_player_statistics(self):
        self.home_players = [PlayerStatisticsMatch(player, self) for player in self.home_players]
        self.away_players = [PlayerStatisticsMatch(player, self) for player in self.away_players]

    def start_match(self, home_atk, home_def, away_atk, away_def):
        if self.time == 0:
            for player_sm in self.home_players + self.away_players:
                player_sm.games += 1

        for player_sm in self.home_players:
            if player_sm.player.name in home_atk:
                self.home_goals += play_atk(player_sm)
            if player_sm.player.name in home_def:
                self.away_goals -= play_def(player_sm)

        for player_sm in self.away_players:
            if player_sm.player.name in away_atk:
                self.away_goals += play_atk(player_sm)
            if player_sm.player.name in away_def:
                self.home_goals -= play_def(player_sm)

        home_subs = len([p for p in home_atk if p not in home_def])
        away_subs = len([p for p in away_atk if p not in away_def])

        print("subs", home_subs, away_subs)
        self.home_goals += 17 - home_subs * 2   # max(0, (home_subs - away_subs) * 2)
        self.away_goals += 16 - away_subs * 2   # max(0, (away_subs - home_subs) * 2)
        print(str(self.home_goals) + ":" + str(self.away_goals))

        self.time += 30

    def finish_match(self):
        self.competition.save_match_result(self)


def play_atk(player_sm):
    if player_sm.attack_rating == 0 and player_sm.player.position.value != 1:
        rating = random.randint(1, 5)
        if rating <= 1:
            player_sm.attack_rating = player_sm.player.attack - 1
        elif rating >= 5:
            player_sm.attack_rating = player_sm.player.attack + 1
        else:
            player_sm.attack_rating = player_sm.player.attack
        print("ATK", player_sm.player.name, player_sm.attack_rating)
    player_sm.attack_minutes += 15
    return player_sm.attack_rating


def play_def(player_sm):
    if player_sm.defense_rating == 0:
        rating = random.randint(1, 5)
        if rating <= 1:
            player_sm.defense_rating = player_sm.player.defense - 1
        elif rating >= 5:
            player_sm.defense_rating = player_sm.player.defense + 1
        else:
            player_sm.defense_rating = player_sm.player.defense
        print("DEF", player_sm.player.name, player_sm.defense_rating)
    player_sm.defense_minutes += 15
    return player_sm.defense_rating
