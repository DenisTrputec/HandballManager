class Person:
    def __init__(self, person_id, name, age, loyalty, country, club, contract_len, salary):
        self.__id = person_id
        self.name = name
        self.age = age
        self.loyalty = loyalty
        self.country = country
        self.club = club
        self.contract_length = contract_len
        self.salary = salary

    def __repr__(self):
        return f"<Person> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Loyalty: {self.loyalty}, Nationality: {self.country.nationality}," \
               f" Club: {self.club.name}, Contract: {self.contract_length}, Cost: {self.salary}"

    def get_id(self):
        return self.__id
