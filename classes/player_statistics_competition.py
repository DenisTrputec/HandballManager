from classes.player_statistics import PlayerStatistics


class PlayerStatisticsCompetition(PlayerStatistics):
    def __init__(self, player, competition, games=0, atk_gam=0, atk_rat=0, atk_min=0, def_gam=0, def_rat=0, def_min=0):
        super().__init__(player, games, atk_gam, atk_rat, atk_min, def_gam, def_rat, def_min)
        self.competition = competition
