class TeamStatistics:
    def __init__(self, club, league, won=0, drawn=0, lost=0, gf=0, ga=0):
        self.club = club
        self.league = league
        self.won = won
        self.drawn = drawn
        self.lost = lost
        self.goals_for = gf
        self.goals_away = ga
