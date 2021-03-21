class Team:
    def __init__(self, team_id, name, nation):
        self.__id = team_id
        self.name = name
        self.nation = nation
        self.players = []

    def __repr__(self):
        return f"<Team> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Nation: {self.nation.name}, Number of players: {len(self.players)}"
