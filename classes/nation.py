class Nation:
    def __init__(self, nation_id, name, nationality):
        self.__id = nation_id
        self.name = name
        self.nationality = nationality

    def __repr__(self):
        return f"<Nation> id: {self.__id}"

    def __str__(self):
        return f"Nation: {self.name}, Nationality: {self.nationality}"
