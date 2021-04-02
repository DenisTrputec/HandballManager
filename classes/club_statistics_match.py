from classes.club_statistics import ClubStatistics


class ClubStatisticsMatch(ClubStatistics):
    def __init__(self, club, match):
        super().__init__(club)
        self.match = match
