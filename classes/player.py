from enum import Enum
from classes.person import Person
import random


class Position(Enum):
    GK = 1
    LW = 2
    LB = 3
    CB = 4
    P = 5
    RB = 6
    RW = 7


# noinspection SpellCheckingInspection
class Player(Person):
    def __init__(self, person_id, name, age, position, attack, defense, loyalty, country, club, contract_length, salary,
                 injury_length):
        super().__init__(person_id, name, age, loyalty, country, club, contract_length, salary)
        self.position = Position(position)
        self.attack = attack
        self.defense = defense
        self.injury_length = injury_length

    def __repr__(self):
        return f"<Player(Person)> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Position: {self.position.name}, Attack: {self.attack}, " \
               f"Defense: {self.defense}, Nationality: {self.country.nationality}, Club: " \
               f"{self.club.name if self.club is not None else '-'}, Contract: {self.contract_length}, " \
               f"Cost: {self.salary}, Injury: {self.injury_length}"

    def generate_injury(self, chance=18):
        inj = random.randint(1, chance)
        while inj == 1:
            self.injury_length += 1
            inj = random.randint(1, 2)

    def update_attributes(self, stats, minutes_required=442, games_required=10):
        """
        :param stats: PlayerStatistics
        :param minutes_required: 70% of a season (age: <24)
        :param games_required: 50% of a season (age: 24-33)
        :return: null
        """
        print("\n", self.name, "Age:", self.age)
        attack_before = self.attack
        defense_before = self.defense

        if self.age == 17:
            if self.position != Position.GK:
                self.attack += random.randint(0, 1)
            if not (self.attack == 3 or (self.position == Position.GK and self.defense == 2)):
                self.defense += random.randint(0, 1)

        elif self.position == Position.GK:
            if self.age <= 35:
                self.defense += self.check_mid(self.defense, stats.def_avg(), stats.defense_games, games_required)
            else:
                if self.check_over33(self.defense, stats.def_avg(), stats.defense_games, games_required):
                    self.defense -= 1

        elif self.age < 24:
            if self.check_under24(self.attack, stats.atk_avg(), stats.attack_minutes, minutes_required):
                self.attack += 1

            if self.age - self.attack - self.defense < 13:
                return

            if self.check_under24(self.defense, stats.def_avg(), stats.defense_minutes, minutes_required):
                self.defense += 1

        elif 24 <= self.age <= 33:
            self.attack += self.check_mid(self.attack, stats.atk_avg(), stats.attack_games, games_required)
            self.defense += self.check_mid(self.defense, stats.def_avg(), stats.defense_games, games_required)

        elif self.age > 33:
            if self.check_over33(self.attack, stats.atk_avg(), stats.attack_games, games_required):
                self.attack -= 1

            if self.check_over33(self.defense, stats.def_avg(), stats.defense_games, games_required):
                self.defense -= 1

        print("ATK:", attack_before, "->", self.attack, )
        print("DEF:", defense_before, "->", self.defense)

    def check_under24(self, player_current_rating, player_rating, player_minutes, minutes_required):
        if player_rating == 5:
            return False

        # Scale minutes to stats.attack_minutes >= 442 equals 1
        minutes = 1 if player_minutes >= minutes_required else player_minutes / minutes_required
        age = 1 if self.age < 21 else 0.5
        rating = player_rating - player_current_rating + 1

        chance_up = round(minutes * age * rating * 100)
        chance = random.randint(1, 200)
        print("Min:", round(minutes, 2), " Rat:", round(rating, 2), " Up:", chance_up, " Chance:", chance)
        if chance_up >= chance:
            return True
        else:
            return False

    def check_mid(self, player_current_rating, player_rating, player_games, games_required):
        if player_games >= games_required:
            if player_rating >= player_current_rating:
                chance_up = 100 - round((player_rating - player_current_rating) * 100)
                chance_down = 0
            else:
                chance_up = 100
                chance_down = round((player_current_rating - player_rating) * 100)
        else:
            chance_up = 95
            chance_down = 5

        if player_current_rating == 5:
            chance_up = 100
        elif player_current_rating == 1:
            chance_down = 0

        chance = random.randint(1, 100)
        print("Games:", player_games, " Up:", chance_up, " Down:", chance_down, " Chance:", chance)
        if chance > chance_up:
            return 1
        elif chance <= chance_down:
            return -1
        else:
            return 0

    def check_over33(self, player_current_rating, player_rating, player_games, games_required):
        if player_current_rating == 1:
            return False

        if player_games >= games_required:
            chance_down = round((player_current_rating + 1 - player_rating) * 100)
        else:
            chance_down = 120

        chance = random.randint(1, 200)
        print("Games:", player_games, " Down:", chance_down, " Chance:", chance)
        if chance <= chance_down:
            return True
        else:
            return False
