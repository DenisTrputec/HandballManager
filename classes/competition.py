class Competition:
    def __init__(self, competition_id, name, nation):
        self.__id = competition_id
        self.name = name
        self.nation = nation

    def __repr__(self):
        return f"<Competition> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Nation: {self.nation.name}"
