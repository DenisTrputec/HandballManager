from classes.team import Team


class Club(Team):
    def __init__(self, team_id, name, nation, league, money):
        super().__init__(team_id, name, nation)
        self.league = league
        self.money = money

    def __repr__(self):
        return f"<Club(Team)> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Nation: {self.nation.name}, League: {self.league.name}, Number of players: " \
               f"{len(self.players)}, Money: {self.money}, Costs: {self.costs()}"

    def costs(self):
        return sum([player.cost for player in self.players])
