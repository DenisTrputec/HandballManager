from classes.competition import Competition
from classes.match import Match
import random


class League(Competition):
    def __init__(self, competition_id, name, short_name, country, level):
        super().__init__(competition_id, name, short_name, country)
        self.level = level
        self.teams = []
        self.standings = []
        self.schedule = []

    def __repr__(self):
        return f"<Competition> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Country: {self.country.name}, Number of teams: {len(self.teams)}"

    def create_schedule(self):
        random.shuffle(self.teams)

        for i in range((len(self.teams) - 1) * 2):
            mid = len(self.teams) // 2
            list1 = self.teams[:mid]
            list2 = self.teams[mid:]
            list2.reverse()

            for j in range(mid):
                # Switch sides after each round
                if i % 2 == 0:
                    self.schedule.append(Match(self, i + 1, list1[j], list2[j]))
                else:
                    self.schedule.append(Match(self, i + 1, list2[j], list1[j]))
            self.teams.insert(1, self.teams.pop())

    def save_match_result(self, match):
        for team_s in self.standings:

            if team_s.club.name == match.home.name:
                if match.home_goals > match.away_goals:
                    team_s.won += 1
                elif match.home_goals < match.away_goals:
                    team_s.lost += 1
                team_s.goals_for += match.home_goals
                team_s.goals_away += match.away_goals

            if team_s.club.name == match.away.name:
                if match.home_goals > match.away_goals:
                    team_s.lost += 1
                elif match.home_goals < match.away_goals:
                    team_s.won += 1
                team_s.goals_for += match.away_goals
                team_s.goals_away += match.home_goals

        self.update_player_statistics(match.home_players)
        self.update_player_statistics(match.away_players)
