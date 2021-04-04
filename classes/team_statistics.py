class TeamStatistics:
    def __init__(self, club, league, won=0, drawn=0, lost=0, gf=0, ga=0):
        self.club = club
        self.league = league
        self.won = won
        self.drawn = drawn
        self.lost = lost
        self.goals_for = gf
        self.goals_away = ga

    def __str__(self):
        return f"Club: {self.club.name}, League: {self.league.short_name}, W:{self.won} D:{self.drawn} L:{self.lost} " \
               f"GF:{self.goals_for} GA:{self.goals_away} "

    def played(self):
        return self.won + self.drawn + self.lost

    def goal_diff(self):
        return self.goals_for - self.goals_away

    def points(self):
        return self.won * 2 + self.drawn
