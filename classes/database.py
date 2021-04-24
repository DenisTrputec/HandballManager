import sqlite3
from classes.country import Country
from classes.league import League
from classes.club import Club
from classes.player import Player
from classes.team_statistics import TeamStatistics
from classes.match import Match


class Database:
    def __init__(self, game_name):
        self.game_name = game_name
        self.db_name = "save/" + game_name + ".db"
        self.connection = None
        self.cursor = None

    def open_connection(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()

    def close_connection(self):
        self.connection.close()

    def commit(self):
        self.connection.cursor()

    def new_game(self):
        self.open_connection()
        self.cursor.execute("UPDATE calendar SET game_name='" + self.game_name + "' WHERE game_name LIKE 'default'")
        self.close_connection()

    def load_game(self, game):
        self.open_connection()

        self.cursor.execute("SELECT * FROM calendar")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            if game.name == t[0]:
                game.season = t[1]
                game.week = t[2]

        self.cursor.execute("SELECT * FROM country")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            game.countries.append(Country(t[0], t[1], t[2]))

        self.cursor.execute("SELECT * FROM v_league")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            for country in game.countries:
                if country.get_id() == t[3]:
                    game.leagues.append(League(t[0], t[1], t[2], country, t[4]))

        self.cursor.execute("SELECT * FROM v_club")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            for country in game.countries:
                if country.get_id() == t[2]:
                    for league in game.leagues:
                        if league.get_id() == t[3]:
                            game.clubs.append(Club(t[0], t[1], country, league, t[4]))

        self.cursor.execute("SELECT * FROM v_player")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            for country in game.countries:
                if country.get_id() == t[7]:
                    for club in game.clubs:
                        if club.get_id() == t[8]:
                            game.players.append(
                                Player(t[0], t[1], t[2], t[3], t[4], t[5], t[6], country, club, t[9], t[10], t[11]))

        self.cursor.execute("SELECT * FROM team_statistics")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            if game.season == t[2]:
                for league in game.leagues:
                    if league.get_id() == t[1]:
                        for club in game.clubs:
                            if club.get_id() == t[0]:
                                game.team_statistics.append(TeamStatistics(club, league, t[3], t[4], t[5], t[6], t[7]))

        self.cursor.execute("SELECT * FROM match")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            for league in game.leagues:
                if league.get_id() == t[0]:
                    home = None
                    away = None
                    for team in game.clubs:
                        if team.get_id() == t[2]:
                            home = team
                        if team.get_id() == t[3]:
                            away = team
                    game.schedule.append(Match(league, t[1], home, away, t[4], t[5], t[6]))

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
            for match in game.schedule:
                if league.get_id() == match.competition.get_id():
                    league.schedule.append(match)

        self.commit()
        self.close_connection()

    def save_game(self, game):
        self.open_connection()

        for club in game.clubs:
            self.cursor.execute("UPDATE club"
                                " SET league_id=" + str(club.league.get_id()) + ", money=" + str(club.money) +
                                " WHERE team_id = " + str(club.get_id()))

        for player in game.players:
            self.cursor.execute("UPDATE person"
                                " SET age=" + str(player.age) + ", loyalty=" + str(player.loyalty) +
                                ", country_id=" + str(player.country.get_id()) + ", club_id=" + str(player.team.get_id()) +
                                ", contract_length=" + str(player.contract_length) + ", salary=" + str(player.salary) +
                                " WHERE id = " + str(player.get_id()))
            self.cursor.execute("UPDATE player"
                                " SET attack=" + str(player.attack) + ", defense=" + str(player.defense) +
                                ", injury_length=" + str(player.injury_length) +
                                " WHERE person_id = " + str(player.get_id()))

        # Update player_statistics
        self.cursor.execute("SELECT * FROM player_statistics")
        tuple_list = self.cursor.fetchall()
        player_sc_database = [t[0] for t in tuple_list]

        for league in game.leagues:
            # Update match
            for match in league.schedule:
                self.cursor.execute("UPDATE match"
                                    " SET time=" + str(match.time) + ", home_goals=" + str(match.home_goals) +
                                    ", away_goals=" + str(match.away_goals) +
                                    " WHERE competition_id = " + str(league.get_id()) +
                                    " AND round = " + str(match.round) +
                                    " AND home_id = " + str(match.home.get_id()) +
                                    " AND away_id = " + str(match.away.get_id()))

            # Update team_statistics
            for team_s in league.standings:
                self.update_team_statistics(team_s, game)

            # Update player_statistics
            for player_sc in league.players_sc:
                if player_sc.player.get_id() not in player_sc_database:
                    self.insert_player_statistics(player_sc, game.season)
                else:
                    self.update_player_statistics(player_sc, game.season)

        self.commit()
        self.close_connection()

    def update_calendar(self, game):
        self.cursor.execute("UPDATE calendar "
                            "SET game_name='" + game.name +
                            "', season=" + str(game.season) +
                            ", week=" + str(game.week) +
                            "WHERE game_name='default' OR game_name='" + game.name + "'")

    def insert_team_statistics(self, team_s, game_season):
        self.cursor.execute("INSERT INTO team_statistics" +
                            " (team_id, competition_id, season, won, drawn, lost, goals_for, goals_away)" +
                            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (team_s.team.get_id(), team_s.competition.get_id(), game_season, team_s.won,
                             team_s.drawn, team_s.lost, team_s.goals_for, team_s.goals_away))

    def update_team_statistics(self, team_s, game):
        self.cursor.execute("UPDATE team_statistics"
                            " SET won=" + str(team_s.won) +
                            ", drawn=" + str(team_s.drawn) +
                            ", lost=" + str(team_s.lost) +
                            ", goals_for=" + str(team_s.goals_for) +
                            ", goals_away=" + str(team_s.goals_away) +
                            " WHERE team_id= " + str(team_s.team.get_id()) +
                            " AND competition_id= " + str(team_s.competition.get_id()) +
                            " AND season=" + str(game.season))

    def insert_player_statistics(self, player_sc, game_season):
        self.cursor.execute("INSERT INTO player_statistics" +
                            " (player_id, competition_id, season, games,"
                            " attack_rating, attack_minutes, defense_rating, defense_minutes)" +
                            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (player_sc.player.get_id(), player_sc.competition.get_id(), game_season, player_sc.games,
                             player_sc.attack_rating, player_sc.attack_minutes,
                             player_sc.defense_rating, player_sc.defense_minutes))

    def update_player_statistics(self, player_sc, game):
        self.cursor.execute("UPDATE player_statistics"
                            " SET games=" + str(player_sc.games) +
                            ", attack_rating=" + str(player_sc.attack_rating) +
                            ", attack_minutes=" + str(player_sc.attack_minutes) +
                            ", defense_rating=" + str(player_sc.defense_rating) +
                            ", defense_minutes=" + str(player_sc.defense_minutes) +
                            " WHERE player_id= " + str(player_sc.player.get_id()) +
                            " AND competition_id= " + str(player_sc.competition.get_id()) +
                            " AND season=" + str(game.season))

    def insert_match(self, game):
        self.open_connection()

        for league in game.leagues:
            for match in league.schedule:
                self.cursor.execute("INSERT INTO match" +
                                    " (competition_id, round, home_id, away_id, time, home_goals, away_goals)" +
                                    " VALUES (?, ?, ?, ?, ?, ?, ?)",
                                    (league.get_id(), match.round, match.home.get_id(), match.away.get_id(),
                                     match.time, match.home_goals, match.away_goals))

        self.commit()
        self.close_connection()

    def load_schedule(self, game):
        self.open_connection()

        self.cursor.execute("SELECT * FROM match")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            for league in game.leagues:
                if league.get_id() == t[0]:
                    home = None
                    away = None
                    for team in game.clubs:
                        if team.get_id() == t[2]:
                            home = team
                        if team.get_id() == t[3]:
                            away = team
                    game.schedule.append(Match(league, t[1], home, away, t[4], t[5], t[6]))

        for league in game.leagues:
            for match in game.schedule:
                if league.get_id() == match.competition.get_id():
                    league.schedule.append(match)

        self.commit()
        self.close_connection()







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
