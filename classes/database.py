import sqlite3
from classes.country import Country
from classes.league import League
from classes.club import Club
from classes.player import Player


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

    for club in game.clubs:
        for player in game.players:
            if club.get_id() == player.club.get_id():
                club.players.append(player)

    for league in game.leagues:
        for club in game.clubs:
            if league.get_id() == club.league.get_id():
                league.teams.append(club)

    connection.commit()
    connection.close()

