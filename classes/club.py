from classes.nation import Nation
from classes.player import Player
from classes.player import Position


class Club:
    def __init__(self, club_id, name, nation, league, players, money):
        self.__id = club_id
        self.name = name
        self.nation = nation
        self.league = league
        self.players = players
        self.money = money

    def __repr__(self):
        return f"<Club> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Nation: {self.nation.name}, League: {self.league}, Number of players: " \
               f"{len(self.players)}, Money: {self.money}, Costs: {self.costs()}"

    def costs(self):
        return sum([player.cost for player in self.players])


if __name__ == "__main__":
    nat = Nation(1, "Croatia", "Croatian")
    player_list = [Player(1, "D.Trputec", 28, Position.CB, 3, 2, 3, nat, "Zagreb", 1, 6, 1),
                   Player(2, "K.Trputec", 23, Position.LB, 4, 1, 2, nat, "Dinamo", 1, 5, 0)]
    club_list = [Club(1, "Zagreb", nat, "1.HRL", player_list, 70),
                 Club(2, "Nexe", nat, "1.HRL", [], 55)]
    for c in club_list:
        print(c)