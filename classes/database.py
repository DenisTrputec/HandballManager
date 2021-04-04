import sqlite3
from classes.country import Country
from classes.league import League
from classes.club import Club
from classes.player import Player
from classes.team_statistics import TeamStatistics


def new_game(game):
    db_name = 'save/' + game.name + '.db'

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("UPDATE calendar SET game_name='" + game.name + "' WHERE game_name LIKE 'default'")

    connection.commit()
    connection.close()


def save_game(game):
    db_name = 'save/' + game.name + '.db'

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    for club in game.clubs:
        cursor.execute("UPDATE club"
                       " SET league_id=" + str(club.league.get_id()) + ", money=" + str(club.money) +
                       " WHERE team_id = " + str(club.get_id()))

    for player in game.players:
        cursor.execute("UPDATE person"
                       " SET age=" + str(player.age) + ", loyalty=" + str(player.loyalty) +
                       ", country_id=" + str(player.country.get_id()) + ", club_id=" + str(player.club.get_id()) +
                       ", contract_length=" + str(player.contract_length) + ", salary=" + str(player.salary) +
                       " WHERE id = " + str(player.get_id()))
        cursor.execute("UPDATE player"
                       " SET attack=" + str(player.attack) + ", defense=" + str(player.defense) +
                       ", injury_length=" + str(player.injury_length) +
                       " WHERE person_id = " + str(player.get_id()))

    connection.commit()
    connection.close()


def load_game(game):
    db_name = 'save/' + game.name + '.db'

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM calendar")
    tuple_list = cursor.fetchall()
    for t in tuple_list:
        if game.name == t[0]:
            game.season = t[1]
            game.week = t[2]

    cursor.execute("SELECT * FROM country")
    tuple_list = cursor.fetchall()
    for t in tuple_list:
        game.countries.append(Country(t[0], t[1], t[2]))

    cursor.execute("SELECT * FROM v_league")
    tuple_list = cursor.fetchall()
    for t in tuple_list:
        for country in game.countries:
            if country.get_id() == t[3]:
                game.leagues.append(League(t[0], t[1], t[2], country, t[4]))

    cursor.execute("SELECT * FROM v_club")
    tuple_list = cursor.fetchall()
    for t in tuple_list:
        for country in game.countries:
            if country.get_id() == t[2]:
                for league in game.leagues:
                    if league.get_id() == t[3]:
                        game.clubs.append(Club(t[0], t[1], country, league, t[4]))

    cursor.execute("SELECT * FROM v_player")
    tuple_list = cursor.fetchall()
    for t in tuple_list:
        for country in game.countries:
            if country.get_id() == t[7]:
                for club in game.clubs:
                    if club.get_id() == t[8]:
                        game.players.append(Player(t[0], t[1], t[2], t[3], t[4], t[5], t[6], country, club, t[9], t[10], t[11]))

    cursor.execute("SELECT * FROM team_statistics")
    tuple_list = cursor.fetchall()
    for t in tuple_list:
        if game.season == t[2]:
            for league in game.leagues:
                if league.get_id() == t[1]:
                    for club in game.clubs:
                        if club.get_id() == t[0]:
                            game.team_statistics.append(TeamStatistics(club, league, t[3], t[4], t[5], t[6], t[7]))

    for club in game.clubs:
        for player in game.players:
            if club.get_id() == player.club.get_id():
                club.players.append(player)

    for league in game.leagues:
        for club in game.clubs:
            if league.get_id() == club.league.get_id():
                league.teams.append(club)
        for club_s in game.team_statistics:
            if league.get_id() == club_s.league.get_id():
                league.standings.append(club_s)

    connection.commit()
    connection.close()


# def new_players():
#     db_name = 'D:\Programiranje\Moje aplikacije\Python\HandballManager\database\default.db'
#     connection = sqlite3.connect(db_name)
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM person_name WHERE country_id = 1 and type LIKE 'last'")
#     last_names = cursor.fetchall()
#     cursor.execute("SELECT * FROM person_name WHERE country_id = 1 and type LIKE 'first'")
#     first_names = cursor.fetchall()
#
#     first_names = first_names[0][1]
#     last_names = [name[1] for name in last_names]
#
#     pid = 0
#     names = []
#     for pos in range(1, 8):
#         for i in range(1, 33):
#             pid += 1
#             player_name = None
#             temp = False
#             while not temp:
#                 player_name = random.choice(first_names) + '.' + random.choice(last_names)
#                 if player_name not in names:
#                     names.append(player_name)
#                     temp = True
#             age = random.randint(18, 36)
#             loyalty = random.randint(1, 5)
#             country_id = 1
#             club = None
#             contract = random.randint(1, 3)
#             salary = None
#
#             attack = random.randint(1, 100) if pos != 1 else 0
#             if attack == 100:
#                 attack = 5
#             elif attack > 90:
#                 attack = 4
#             elif attack > 65:
#                 attack = 3
#             elif attack > 33:
#                 attack = 2
#             else:
#                 attack = 1
#             defense = random.randint(1, 100)
#             if defense == 100:
#                 defense = 5
#             elif defense > 90:
#                 defense = 4
#             elif defense > 65:
#                 defense = 3
#             elif defense > 33:
#                 defense = 2
#             else:
#                 defense = 1
#
#             injury = 0
#             inj = random.randint(1, 10)
#             while inj == 1:
#                 injury += 1
#                 inj = random.randint(1, 2)
#
#             salary = random.randint(attack + defense - 1, attack + defense + 1)
#
#             cursor.execute("INSERT INTO person (id, name, age, loyalty, country_id, contract_length, salary) VALUES (?, ?, ?, ?, ?, ?, ?)", (pid, player_name, age, loyalty, country_id, contract, salary))
#             cursor.execute("INSERT INTO player (person_id, position_id, attack, defense, injury_length) VALUES (?, ?, ?, ?, ?)", (pid, pos, attack, defense, injury))
#
#     connection.commit()
#     connection.close()
