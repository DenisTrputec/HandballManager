from classes.nation import Nation


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
               f" Club: {self.club}, Contract: {self.contract}, Cost: {self.cost}"


if __name__ == "__main__":
    nat = Nation("Croatia", "Croatian")
    person_list = [Person(1, "D.Trputec", 28, 3, nat, "Zagreb", None, None),
                   Person(2, "K.Trputec", 23, 2, nat, "Dinamo", None, None)]
    for p in person_list:
        print(p)
