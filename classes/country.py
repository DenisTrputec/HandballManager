class Country:
    def __init__(self, country_id, name, nationality):
        self.__id = country_id
        self.name = name
        self.nationality = nationality

    def __repr__(self):
        return f"<Country> id: {self.__id}"

    def __str__(self):
        return f"Country: {self.name}, Nationality: {self.nationality}"

    def get_id(self):
        return self.__id
