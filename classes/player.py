from enum import Enum
from classes.person import Person


class Position(Enum):
    GK = 1
    LW = 2
    LB = 3
    CB = 4
    P = 5
    RB = 6
    RW = 7


class Player(Person):
    def __init__(self, person_id, name, age, position, attack, defense, loyalty, country, club, contract_length, salary,
                 injury_length):
        super().__init__(person_id, name, age, loyalty, country, club, contract_length, salary)
        self.position = position
        self.attack = attack
        self.defense = defense
        self.injury_length = injury_length

    def __repr__(self):
        return f"<Player(Person)> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Position: {self.position.name}, Attack: {self.attack}, " \
               f"Defense: {self.defense}, Loyalty: {self.loyalty}, Nationality: {self.country.nationality}, Club: " \
               f"{self.club.name}, Contract: {self.contract_length}, Cost: {self.salary}, Injury: {self.injury_length}"
