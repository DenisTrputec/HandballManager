from enum import Enum
from classes.person import Person
from classes.nation import Nation


class Position(Enum):
    GK = 1
    LW = 2
    LB = 3
    CB = 4
    P = 5
    RB = 6
    RW = 7


class Player(Person):
    def __init__(self, person_id, name, age, position, attack, defense, loyalty, nation, club, contract, cost,
                 injury):
        super().__init__(person_id, name, age, loyalty, nation, club, contract, cost)
        self.position = position
        self.attack = attack
        self.defense = defense
        self.injury = injury

    def __repr__(self):
        return f"<Player(Person)> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Position: {self.position.name}, Attack: {self.attack}, " \
               f"Defense: {self.defense}, Loyalty: {self.loyalty}, Nationality: {self.nation.nationality}, Club: " \
               f"{self.club}, Contract: {self.contract}, Cost: {self.cost}, Injury: {self.injury}"


if __name__ == "__main__":
    nat = Nation(1, "Croatia", "Croatian")
    player_list = [Player(1, "D.Trputec", 28, Position.CB, 3, 2, 3, nat, "Zagreb", None, None, 1),
                   Player(2, "K.Trputec", 23, Position.LB, 4, 1, 2, nat, "Dinamo", None, None, 0)]
    for p in player_list:
        print(p)
