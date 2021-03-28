class Competition:
    def __init__(self, competition_id, name, short_name, country):
        self.__id = competition_id
        self.name = name
        self.short_name = short_name
        self.country = country

    def __repr__(self):
        return f"<Competition> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Nation: {self.country.name}"
