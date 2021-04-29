class PlayerStatistics:
    def __init__(self, player, games=0, atk_gam=0, atk_rat=0, atk_min=0, def_gam=0, def_rat=0, def_min=0):
        self.player = player
        self.games = games
        self.attack_games = atk_gam
        self.attack_rating = atk_rat
        self.attack_minutes = atk_min
        self.defense_games = def_gam
        self.defense_rating = def_rat
        self.defense_minutes = def_min

    def __str__(self):
        return f"Player: {self.player.name}, Games: {self.games}, AtkRat:{self.attack_rating}, " \
               f"AtkMin:{self.attack_minutes}, DefRat:{self.defense_rating}, DefMin:{self.defense_minutes}"
