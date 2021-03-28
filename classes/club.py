from classes.team import Team


class Club(Team):
    def __init__(self, team_id, name, country, league, money):
        super().__init__(team_id, name, country)
        self.league = league
        self.money = money

    def __repr__(self):
        return f"<Club(Team)> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Nation: {self.country.name}, League: {self.league.name}, Number of players: " \
               f"{len(self.players)}, Money: {self.money}, Costs: {self.costs()}"

    def costs(self):
        return sum([player.salary for player in self.players])
