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
               f"Defense: {self.defense}, Loyalty: {self.loyalty}, Nationality: {self.country.nationality}, Club: " \
               f"{self.club.name}, Contract: {self.contract_length}, Cost: {self.salary}, Injury: {self.injury_length}"

    def generate_injury(self, chance=18):
        inj = random.randint(1, chance)
        while inj == 1:
            self.injury_length += 1
            inj = random.randint(1, 2)

    def update_ratings(self, stats, minutes_acquired=442, games_acquired=10):
        """
        :param stats: PlayerStatistics
        :param minutes_acquired: 70% of a season (age: <24)
        :param games_acquired: 50% of a season (age: 24-33)
        :return: null
        """
        attack_before = self.attack
        defense_before = self.defense

        if self.position == Position.GK:
            if self.age <= 35:
                self.defense += self.check_mid(self.defense, stats.defense_rating, stats.defense_games, games_acquired)
            else:
                if self.check_over33(self.defense, stats.defense_rating, stats.defense_games, games_acquired):
                    self.defense -= 1
            print(self.name, "Defense before:", defense_before, "Defense now:", self.defense)

        elif self.age < 24:
            if self.check_under24(self.attack, stats.attack_rating, stats.attack_minutes, minutes_acquired):
                self.attack += 1
            print(self.name, "Attack before:", attack_before, "Attack now:", self.attack)

            if self.age - self.attack - self.defense < 13:
                print(self.name, "Defense before:", defense_before, "Defense now:",  self.defense)
                return

            if self.check_under24(self.defense, stats.defense_rating, stats.defense_minutes, minutes_acquired):
                self.defense += 1
            print(self.name, "Defense before:", defense_before, "Defense now:",  self.defense)

        elif 24 <= self.age <= 33:
            self.attack += self.check_mid(self.attack, stats.attack_rating, stats.attack_games, games_acquired)
            self.defense += self.check_mid(self.defense, stats.defense_rating, stats.defense_games, games_acquired)
            print(self.name, "Attack before:", attack_before, "Attack now:", self.attack)
            print(self.name, "Defense before:", defense_before, "Defense now:", self.defense)

        elif self.age > 33:
            if self.check_over33(self.attack, stats.attack_rating, stats.attack_games, games_acquired):
                self.attack -= 1
            print(self.name, "Attack before:", attack_before, "Attack now:", self.attack)

            if self.check_over33(self.defense, stats.defense_rating, stats.defense_games, games_acquired):
                self.defense -= 1
            print(self.name, "Defense before:", defense_before, "Defense now:", self.defense)

    def check_under24(self, player_current_rating, player_rating, player_minutes, minutes_acquired):
        if player_rating == 5:
            return False

        # Scale minutes to stats.attack_minutes >= 442 equals 1
        minutes = 1 if player_minutes >= minutes_acquired else player_minutes / minutes_acquired
        age = 1 if self.age < 21 else 0.5
        rating = player_rating - player_current_rating + 1

        chance_up = round(minutes * age * rating * 100)
        chance = random.randint(1, 200)
        print(self.name, minutes, rating, chance_up, chance)
        if chance_up >= chance:
            return True
        else:
            return False

    def check_mid(self, player_current_rating, player_rating, player_games, games_acquired):
        if player_games >= games_acquired:
            if player_rating >= player_current_rating:
                chance_up = 100 - round(player_rating - player_current_rating * 100)
                chance_down = 0
            else:
                chance_up = 0
                chance_down = round(player_current_rating - player_rating * 100)
        else:
            chance_up = 95
            chance_down = 5

        if player_current_rating == 5:
            chance_up = 100
        elif player_current_rating == 1:
            chance_down = 0

        chance = random.randint(1, 100)
        print(self.name, player_games, chance_up, chance_down, chance)
        if chance > chance_up:
            return 1
        elif chance <= chance_down:
            return -1
        else:
            return 0

    def check_over33(self, player_current_rating, player_rating, player_games, games_acquired):
        if player_rating == 1:
            return False

        if player_games >= games_acquired:
            chance_down = round(player_current_rating + 1 - player_rating * 100)
        else:
            chance_down = 120

        chance = random.randint(1, 100)
        print(self.name, player_games, chance_down, chance)
        if chance <= chance_down:
            return True
        else:
            return False
