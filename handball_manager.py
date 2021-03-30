from classes.game import Game
from classes.country import Country
from classes.league import League
from classes.club import Club
from classes.player import Player
from classes.player import Position
from classes import database

if __name__ == "__main__":
    game = Game()
    game.load_game("denis")
    game.save_game()
