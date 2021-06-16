from enum import Enum


class Status(Enum):
    Pending = 0
    Rejected = 1
    Accepted = 2


class ContractOffer:
    def __init__(self, player, club, club_reputation, salary, length, week, status):
        self.player = player
        self.club = club
        self.club_reputation = club_reputation
        self.salary = salary
        self.length = length
        self.week_offered = week
        self.status = status

    def __str__(self):
        return f"\nPlayer: {self.player.name}\tWeek offered:{self.week_offered}\nClub: {self.club.name}\tReputation: " \
               f"{self.club_reputation}\nSalary: {self.salary}\tLength: {self.length}\nStatus: {self.status.name}"
