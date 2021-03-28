from classes.competition import Competition


class League(Competition):
    def __init__(self, competition_id, name, short_name, country, level):
        super().__init__(competition_id, name, short_name, country)
        self.level = level
        self.teams = []
        self.schedule = []

    def __repr__(self):
        return f"<Competition> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Country: {self.country.name}, Number of teams: {len(self.teams)}"
