class ContractOffer:
    def __init__(self, player, club, club_reputation, salary, length, week):
        self.player = player
        self.club = club
        self.club_reputation = club_reputation
        self.salary = salary
        self.length = length
        self.week_offered = week

    def __str__(self):
        return f"Player: {self.player.name}\tWeek offered:{self.week_offered}\nClub: {self.club.name}\tReputation: {self.club_reputation}\nSalary: {self.salary}\tLength: {self.length}"
