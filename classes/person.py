class Person:
    def __init__(self, person_id, name, age, loyalty, nation, club, contract, cost):
        self.__id = person_id
        self.name = name
        self.age = age
        self.loyalty = loyalty
        self.nation = nation
        self.club = club
        self.contract = contract
        self.cost = cost

    def __repr__(self):
        return f"<Person> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Loyalty: {self.loyalty}, Nationality: {self.nation.nationality}," \
               f" Club: {self.club.name}, Contract: {self.contract}, Cost: {self.cost}"
