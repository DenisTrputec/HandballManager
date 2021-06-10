from classes.team import Team
import random


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

    def budget(self):
        return self.money - sum([player.salary for player in self.players if player.contract_length > 0])

    def generate_injury(self, chance=18):
        returned_from_injury = []
        new_injuries = []

        random.shuffle(self.players)
        for player in self.players:

            # Player is already injured
            if player.injury_length > 0:
                player.injury_length -= 1
                if player.injury_length == 0:
                    returned_from_injury.append(player)
                continue

            # At least 14 players must stay available
            if len([x for x in self.players if x.injury_length == 0]) <= 14:
                continue

            # At least 1 player on each position must stay available
            if len([x for x in self.players if (x.position == player.position and x.injury_length == 0)]) > 1:
                player.generate_injury()
                if player.injury_length > 0:
                    new_injuries.append(player)

        return returned_from_injury, new_injuries
