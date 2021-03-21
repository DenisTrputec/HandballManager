class Nation:
    def __init__(self, name, nationality):
        self.name = name
        self.nationality = nationality

    def __repr__(self):
        return "<Nation>"

    def __str__(self):
        return f"Nation: {self.name}, Nationality: {self.nationality}"


if __name__ == "__main__":
    nation_list = [Nation("Croatia", "Croatian"),
                   Nation("Germany", "German")]
    for n in nation_list:
        print(n)
