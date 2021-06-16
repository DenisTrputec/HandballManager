import sqlite3
import logging
from classes.country import Country
from classes.league import League
from classes.club import Club
from classes.player import Player
from classes.team_statistics import TeamStatistics
from classes.player_statistics_competition import PlayerStatisticsCompetition
from classes.match import Match
from classes.contract_offer import ContractOffer


class Database:
    def __init__(self, game_name):
        self.game_name = game_name
        self.db_name = "save/" + game_name + ".db"
        self.connection = None
        self.cursor = None

    def open_connection(self):
        logging.debug("Database.open_connection()")
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        logging.debug("Database.open_connection() Executed")

    def close_connection(self):
        logging.debug("Database.close_connection()")
        self.connection.close()
        logging.debug("Database.close_connection() Executed")

    def commit(self):
        logging.debug("Database.commit()")
        self.connection.commit()
        logging.debug("Database.commit() Executed")

    def new_game(self, game):
        logging.debug("Database.new_game()")
        self.open_connection()
        self.update_game_info(game)
        self.commit()
        self.close_connection()

        self.load_game(game)

        self.open_connection()
        for league in game.leagues:
            league.create_schedule()
        self.insert_match(game)
        self.load_schedule(game)
        self.commit()
        self.close_connection()
        logging.debug("Database.new_game() Executed")

    def load_game(self, game):
        logging.debug("Database.load_game()")
        self.open_connection()

        self.cursor.execute("SELECT * FROM game_info")
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
                            club = Club(t[0], t[1], country, league, t[4])
                            game.clubs.append(club)
                            league.teams.append(club)

        self.cursor.execute("SELECT * FROM v_player")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            for country in game.countries:
                if country.get_id() == t[7]:
                    for club in game.clubs:
                        if club.get_id() == t[8]:
                            player = Player(t[0], t[1], t[2], t[3], t[4], t[5], t[6], country, club, t[9], t[10], t[11])
                            game.players.append(player)
                            club.players.append(player)
                            break
                    else:
                        player = Player(t[0], t[1], t[2], t[3], t[4], t[5], t[6], country, None, t[9], t[10], t[11])
                        game.players.append(player)

        self.cursor.execute("SELECT * FROM team_statistics")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            if game.season == t[2]:
                for league in game.leagues:
                    if league.get_id() == t[1]:
                        for club in game.clubs:
                            if club.get_id() == t[0]:
                                league.standings.append(TeamStatistics(club, league, t[3], t[4], t[5], t[6], t[7]))

        self.cursor.execute("SELECT * FROM player_statistics")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            if game.season == t[2]:
                for league in game.leagues:
                    if league.get_id() == t[1]:
                        for player in game.players:
                            if player.get_id() == t[0]:
                                league.players_sc.append(
                                    PlayerStatisticsCompetition(player, league, t[3], t[4], t[5], t[6], t[7], t[8], t[9]))

        self.cursor.execute("SELECT * FROM contract_offer")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            p = c = None
            for player in game.players:
                if player.get_id() == t[0]:
                    p = player
            for club in game.clubs:
                if club.get_id() == t[1]:
                    c = club
            game.contract_offers.append(ContractOffer(p, c, t[2], t[3], t[4], t[5], 0))

        self.cursor.execute("SELECT * FROM calendar")
        tuple_list = self.cursor.fetchall()
        for t in tuple_list:
            for league in game.leagues:
                if league.get_id() == t[1]:
                    game.calendar.append((t[0], league, t[2]))

        self.load_schedule(game)

        self.commit()
        self.close_connection()
        logging.debug("Database.load_game() Executed")

    def save_game(self, game):
        logging.debug("Database.save_game()")
        self.open_connection()

        # Update table game_info
        self.update_game_info(game)

        # Update table club
        self.update_club(game)

        # Update tables person and player
        self.cursor.execute("SELECT * FROM v_player")
        tuple_list = self.cursor.fetchall()
        player_database = [t[0] for t in tuple_list]
        for player in game.players:
            if player.get_id() not in player_database:
                logging.info("Database.insert_player()")
                self.insert_player(player)
            else:
                logging.info("Database.update_player()")
                self.update_player(player)

        # Update table player_statistics part 1
        logging.info("SELECT * FROM player_statistics")
        self.cursor.execute("SELECT * FROM player_statistics")
        tuple_list = self.cursor.fetchall()
        player_s_database = [t[0] for t in tuple_list]

        # Update table team_statistics part 1
        logging.info("SELECT * FROM team_statistics")
        self.cursor.execute("SELECT * FROM team_statistics")
        tuple_list = self.cursor.fetchall()
        team_s_database = [t[0] for t in tuple_list]

        # Update table match part 1
        logging.info("SELECT * FROM match")
        self.cursor.execute("SELECT * FROM match")
        tuple_list = self.cursor.fetchall()
        match_database = [(t[0], t[1], t[2], t[3]) for t in tuple_list]

        for league in game.leagues:
            # Update table player_statistics part 2
            for player_sc in league.players_sc:
                if player_sc.player.get_id() not in player_s_database:
                    self.insert_player_statistics(player_sc, game.season)
                else:
                    self.update_player_statistics(player_sc, game)

            # Update table team_statistics part 2
            for team_sc in league.standings:
                if team_sc.team.get_id() not in team_s_database:
                    self.insert_team_statistics(team_sc, game.season)
                else:
                    self.update_team_statistics(team_sc, game)

            # Update table match
            self.update_match(league)

        # Update table contract_offer
        self.cursor.execute("DELETE FROM contract_offer")
        for offer in game.contract_offers:
            self.insert_contract_offer(offer)

        self.commit()
        self.close_connection()
        logging.debug("Database.save_game() Executed")

    def update_game_info(self, game):
        logging.debug("Database.update_game_info()")
        logging.debug(game.name + " " + str(game.season) + " " + str(game.week))
        self.cursor.execute("UPDATE game_info "
                            "SET game_name='" + game.name +
                            "', season=" + str(game.season) +
                            ", week=" + str(game.week) +
                            " WHERE game_name LIKE 'default' OR game_name LIKE '" + game.name + "'")
        logging.debug("Database.update_game_info() Executed")

    def update_club(self, game):
        logging.debug("Database.update_club()")
        for club in game.clubs:
            self.cursor.execute("UPDATE club"
                                " SET league_id=" + str(club.league.get_id()) +
                                ", money=" + str(club.money) +
                                " WHERE team_id = " + str(club.get_id()))
        logging.debug("Database.update_club() Executed")

    def insert_player(self, player):
        logging.debug("Database.insert_player()")
        club = player.club.get_id() if player.club is not None else None
        self.cursor.execute("INSERT INTO person" +
                            " (id, name, age, loyalty, country_id, club_id, contract_length, salary)" +
                            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (player.get_id(), player.name, player.age, player.loyalty, player.country.get_id(), club,
                             player.contract_length, player.salary))
        self.cursor.execute("INSERT INTO player" +
                            " (person_id, position_id, attack, defense, injury_length)" +
                            " VALUES(?, ?, ?, ?, ?)",
                            (player.get_id(), player.position.value, player.attack, player.defense, player.injury_length))
        logging.debug("Database.insert_player() Executed")

    def update_player(self, player):
        logging.debug("Database.update_player()")
        self.cursor.execute("UPDATE person"
                            " SET age=" + str(player.age) + ", loyalty=" + str(player.loyalty) +
                            ", country_id=" + str(player.country.get_id()) + ", club_id=" + str(player.club.get_id()) +
                            ", contract_length=" + str(player.contract_length) + ", salary=" + str(player.salary) +
                            " WHERE id = " + str(player.get_id()))
        self.cursor.execute("UPDATE player"
                            " SET attack=" + str(player.attack) + ", defense=" + str(player.defense) +
                            ", injury_length=" + str(player.injury_length) +
                            " WHERE person_id = " + str(player.get_id()))
        logging.debug("Database.update_player() Executed")

    def insert_team_statistics(self, team_s, game_season):
        logging.debug("Database.insert_team_statistics()")
        self.cursor.execute("INSERT INTO team_statistics" +
                            " (team_id, competition_id, season, won, drawn, lost, goals_for, goals_away)" +
                            " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                            (team_s.team.get_id(), team_s.league.get_id(), game_season, team_s.won,
                             team_s.drawn, team_s.lost, team_s.goals_for, team_s.goals_away))
        logging.debug("Database.insert_team_statistics() Executed")

    def update_team_statistics(self, team_s, game):
        logging.debug("Database.update_team_statistics()")
        self.cursor.execute("UPDATE team_statistics"
                            " SET won=" + str(team_s.won) +
                            ", drawn=" + str(team_s.drawn) +
                            ", lost=" + str(team_s.lost) +
                            ", goals_for=" + str(team_s.goals_for) +
                            ", goals_away=" + str(team_s.goals_away) +
                            " WHERE team_id= " + str(team_s.team.get_id()) +
                            " AND competition_id= " + str(team_s.league.get_id()) +
                            " AND season=" + str(game.season))
        logging.debug("Database.update_team_statistics() Executed")

    def insert_player_statistics(self, player_sc, game_season):
        logging.debug("Database.insert_player_statistics()")
        self.cursor.execute("INSERT INTO player_statistics" +
                            " (player_id, competition_id, season, games, attack_games, attack_rating,"
                            " attack_minutes, defense_games, defense_rating, defense_minutes)" +
                            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (player_sc.player.get_id(), player_sc.competition.get_id(), game_season, player_sc.games,
                             player_sc.attack_games, player_sc.attack_rating, player_sc.attack_minutes,
                             player_sc.defense_games, player_sc.defense_rating, player_sc.defense_minutes))
        logging.debug("Database.insert_player_statistics() Executed")

    def update_player_statistics(self, player_sc, game):
        logging.debug("Database.update_player_statistics()")
        self.cursor.execute("UPDATE player_statistics" +
                            " SET games=" + str(player_sc.games) +
                            ", attack_games=" + str(player_sc.attack_games) +
                            ", attack_rating=" + str(player_sc.attack_rating) +
                            ", attack_minutes=" + str(player_sc.attack_minutes) +
                            ", defense_games=" + str(player_sc.defense_games) +
                            ", defense_rating=" + str(player_sc.defense_rating) +
                            ", defense_minutes=" + str(player_sc.defense_minutes) +
                            " WHERE player_id= " + str(player_sc.player.get_id()) +
                            " AND competition_id= " + str(player_sc.competition.get_id()) +
                            " AND season=" + str(game.season))
        logging.debug("Database.update_player_statistics() Executed")

    def insert_match(self, game):
        logging.debug("Database.insert_match()")
        for league in game.leagues:
            for match in league.schedule:
                self.cursor.execute("INSERT INTO match" +
                                    " (competition_id, round, home_id, away_id, time, home_goals, away_goals)" +
                                    " VALUES (?, ?, ?, ?, ?, ?, ?)",
                                    (league.get_id(), match.round, match.home.get_id(), match.away.get_id(),
                                     match.time, match.home_goals, match.away_goals))
        logging.debug("Database.insert_match() Executed")

    def update_match(self, league):
        logging.debug("Database.update_match()")
        for match in league.schedule:
            self.cursor.execute("UPDATE match" +
                                " SET time=" + str(match.time) + ", home_goals=" + str(match.home_goals) +
                                ", away_goals=" + str(match.away_goals) +
                                " WHERE competition_id = " + str(league.get_id()) +
                                " AND round = " + str(match.round) +
                                " AND home_id = " + str(match.home.get_id()) +
                                " AND away_id = " + str(match.away.get_id()))
        logging.debug("Database.update_match() Executed")

    def insert_contract_offer(self, offer):
        logging.debug("Database.insert_contract_offer()")
        self.cursor.execute("INSERT INTO contract_offer" +
                            " (player_id, club_id, club_reputation, salary, length, week_offered)" +
                            " VALUES (?, ?, ?, ?, ?, ?)",
                            (offer.player.get_id(), offer.club.get_id(), offer.club_reputation, offer.salary,
                             offer.length, offer.week_offered))
        logging.debug("Database.insert_contract_offer() Executed")

    def load_schedule(self, game):
        logging.debug("Database.load_schedule()")
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
                    match = Match(league, t[1], home, away, t[4], t[5], t[6])
                    game.schedule.append(match)
                    league.schedule.append(match)
        logging.debug("Database.load_schedule() Executed")

    def return_names(self, country_id):
        logging.debug("Database.return_first_names()")
        self.open_connection()

        self.cursor.execute("SELECT * FROM person_name WHERE country_id=" + str(country_id) + " and type LIKE 'first'")
        first_names = self.cursor.fetchall()
        self.cursor.execute("SELECT * FROM person_name WHERE country_id=" + str(country_id)
                            + " and type LIKE 'last' AND id > 201")
        last_names = self.cursor.fetchall()

        self.commit()
        self.close_connection()
        logging.debug("Database.return_first_names() Executed")

        first_names = [t[1] for t in first_names][0]
        last_names = [t[1] for t in last_names]
        return first_names, last_names







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
