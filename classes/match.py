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
        print(str(self.home_goals) + ":" + str(self.away_goals))
        self.home_goals += 15 - max(0, (home_subs - away_subs) * 2)
        self.away_goals += 14 - max(0, (away_subs - home_subs) * 2)
        while (self.home_goals + self.away_goals) > self.time + 30 and self.home_goals > 4 and self.away_goals > 4:
            self.home_goals -= 1
            self.away_goals -= 1
        self.home_goals = max(self.home_goals, 5 + self.time // 6)
        self.away_goals = max(self.away_goals, 5 + self.time // 6)
        print(str(self.home_goals) + ":" + str(self.away_goals))

        self.time += 30

    def finish_match(self):
        self.competition.save_match_result(self)


def play_atk(player_sm):
    if player_sm.attack_minutes == 0 and player_sm.player.position.value != 1:
        rating = random.randint(1, 5)
        if rating <= 1:
            player_sm.attack_rating = player_sm.player.attack - 1
        elif rating >= 5:
            player_sm.attack_rating = player_sm.player.attack + 1
        else:
            player_sm.attack_rating = player_sm.player.attack
    player_sm.attack_minutes += 15
    return player_sm.attack_rating


def play_def(player_sm):
    if player_sm.defense_minutes == 0:
        rating = random.randint(1, 5)
        if rating <= 1:
            player_sm.defense_rating = player_sm.player.defense - 1
        elif rating >= 5:
            player_sm.defense_rating = player_sm.player.defense + 1
        else:
            player_sm.defense_rating = player_sm.player.defense
    player_sm.defense_minutes += 15
    return player_sm.defense_rating
