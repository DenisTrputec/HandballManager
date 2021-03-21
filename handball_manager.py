from classes.nation import Nation
from classes.league import League
from classes.club import Club
from classes.player import Player
from classes.player import Position

if __name__ == "__main__":
    nation_list = [Nation(1, "Croatia", "Croatian"),
                   Nation(2, "Germany", "German")]
    league_list = [League(1, "1. HRL", nation_list[0]),
                   League(2, "Bundesliga", nation_list[1])]
    club_list = [Club(1, "Zagreb", nation_list[0], nation_list[0], 70),
                 Club(2, "Nexe", nation_list[0], nation_list[0], 55)]
    player_list = [Player(1, "D.Trputec", 28, Position.CB, 3, 2, 3, nation_list[0], club_list[0], None, None, 1),
                   Player(2, "K.Trputec", 23, Position.LB, 4, 1, 2, nation_list[0], club_list[1], None, None, 0)]

    for x in nation_list:
        print(x)
    for x in league_list:
        print(x)
    for x in club_list:
        print(x)
    for x in player_list:
        print(x)
