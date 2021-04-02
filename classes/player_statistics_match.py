from classes.player_statistics import PlayerStatistics


class PlayerStatisticsMatch(PlayerStatistics):
    def __init__(self, player, match):
        super().__init__(player)
        self.match = match
