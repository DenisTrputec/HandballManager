from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem

uiInjuryUpdate = "gui/injury_update.ui"
formInjuryUpdate, baseInjuryUpdate = uic.loadUiType(uiInjuryUpdate)


class InjuryUpdate(baseInjuryUpdate, formInjuryUpdate):
    def __init__(self, parent, game):
        super(baseInjuryUpdate, self).__init__()
        self.setupUi(self)
        self.parent_window = parent
        self.game = game

        self.returned_from_injury = []
        self.new_injuries = []
        self.update_injuries()
        self.fill_combobox_league()

    def update_injuries(self):
        for club in self.game.clubs:
            injury_ret, injury_new = club.generate_injury()
            for player in injury_ret:
                self.returned_from_injury.append(player)
            for player in injury_new:
                self.new_injuries.append(player)
        print("\nReturned from injury")
        for player in self.returned_from_injury:
            print(player.club.name, player.name)
        print("\nNew injuries")
        for player in self.new_injuries:
            print(player.club.name, player.name, player.injury_length)

    def fill_combobox_league(self):
        for league in self.game.leagues:
            self.cbLeague.addItem(league.name)
        self.update_table_players()

    def update_table_players(self):
        print("update_table_players")
        for league in self.game.leagues:
            print(league.name)
            if league.name == self.cbLeague.currentText():
                returned_from_injury = [player for player in self.returned_from_injury if player.club.league.name == league.name]
                new_injuries = [player for player in self.new_injuries if player.club.league.name == league.name]
                self.tblPlayers.setRowCount(max(len(returned_from_injury), len(new_injuries)))
                print(4)
                for row, player in enumerate(returned_from_injury):
                    self.tblPlayers.setItem(row, 0, QTableWidgetItem(player.club.name))
                    self.tblPlayers.setItem(row, 1, QTableWidgetItem(player.name))
                for row, player in enumerate(new_injuries):
                    self.tblPlayers.setItem(row, 3, QTableWidgetItem(player.club.name))
                    self.tblPlayers.setItem(row, 4, QTableWidgetItem(player.name))
                    self.tblPlayers.setItem(row, 5, QTableWidgetItem(str(player.injury_length)))
                header = self.tblPlayers.horizontalHeader()
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
                break
        print("update_table_league executed")
