class Team:
    def __init__(self, team_id, name, country):
        self.__id = team_id
        self.name = name
        self.country = country
        self.players = []

    def __repr__(self):
        return f"<Team> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Nation: {self.country.name}, Number of players: {len(self.players)}"
