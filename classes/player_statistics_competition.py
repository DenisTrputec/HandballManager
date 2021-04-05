from classes.player_statistics import PlayerStatistics


class PlayerStatisticsCompetition(PlayerStatistics):
    def __init__(self, player, competition):
        super().__init__(player)
        self.competition = competition
