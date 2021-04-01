from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5 import uic, QtCore
import sys

uiPreMatch = "gui/pre-match.ui"
formPreMatch, basePreMatch = uic.loadUiType(uiPreMatch)


class PreMatch(basePreMatch, formPreMatch):
    def __init__(self, match):
        super(basePreMatch, self).__init__()

        self.setupUi(self)
        self.match = match
        self.update_table()

    def update_table(self):
        players = self.match.home.players
        players.sort(key=lambda x: x.position.value)
        self.tblPlayers.setRowCount(len(players))
        for row, player in enumerate(players):
            self.tblPlayers.setItem(row, 0, QTableWidgetItem(player.name))
            self.tblPlayers.setItem(row, 1, QTableWidgetItem(str(player.age)))
            self.tblPlayers.setItem(row, 2, QTableWidgetItem(player.position.name))
            self.tblPlayers.setItem(row, 3, QTableWidgetItem(str(player.attack)))
            self.tblPlayers.setItem(row, 4, QTableWidgetItem(str(player.defense)))
            is_selected = QTableWidgetItem("")
            is_selected.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            is_selected.setCheckState(QtCore.Qt.Unchecked)
            self.tblPlayers.setItem(row, 5, is_selected)
            row += 1
