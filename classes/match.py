from classes.club_statistics_match import ClubStatisticsMatch
from classes.player_statistics_match import PlayerStatisticsMatch


class Match:
    def __init__(self, home_club, away_club):
        self.home = home_club
        self.away = away_club
        self.time = 0
        self.home_goals = 0
        self.away_goals = 0
        self.home_players = []
        self.away_players = []
        self.home_statistics = ClubStatisticsMatch(self.home, self)
        self.away_statistics = ClubStatisticsMatch(self.away, self)

    def create_player_statistics(self):
        self.home_players = [PlayerStatisticsMatch(player, self) for player in self.home_players]
        self.away_players = [PlayerStatisticsMatch(player, self) for player in self.away_players]

    def play(self, player_name):
        print(player_name)
