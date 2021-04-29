from classes.player_statistics_competition import PlayerStatisticsCompetition


class Competition:
    def __init__(self, competition_id, name, short_name, country):
        self.__id = competition_id
        self.name = name
        self.short_name = short_name
        self.country = country
        self.players_sc = []

    def __repr__(self):
        return f"<Competition> id: {self.__id}"

    def __str__(self):
        return f"Name: {self.name}, Nation: {self.country.name}"

    def get_id(self):
        return self.__id

    def update_player_statistics(self, match_players):
        for player_sm in match_players:
            for player_sc in self.players_sc:
                if player_sm.player.get_id() == player_sc.player.get_id():
                    player_sc.games += 1
                    player_sc.attack_games += player_sm.attack_games
                    player_sc.attack_rating += player_sm.attack_rating
                    player_sc.attack_minutes += player_sm.attack_minutes
                    player_sc.defense_games += player_sm.defense_games
                    player_sc.defense_rating += player_sm.defense_rating
                    player_sc.defense_minutes += player_sm.defense_minutes
                    break
            else:
                self.players_sc.append(PlayerStatisticsCompetition(player_sm.player, self, 1, player_sm.attack_games,
                                                                   player_sm.attack_rating, player_sm.attack_minutes,
                                                                   player_sm.defense_games, player_sm.defense_rating,
                                                                   player_sm.defense_minutes))
