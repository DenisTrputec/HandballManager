from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QBrush, QColor
import sys

uiPreMatch = "gui/pre-match.ui"
formPreMatch, basePreMatch = uic.loadUiType(uiPreMatch)


class PreMatch(basePreMatch, formPreMatch):
    def __init__(self, match):
        super(basePreMatch, self).__init__()

        self.setupUi(self)
        self.match = match
        self.update_table()
        self.btnConfirm.clicked.connect(self.update_combobox)

    def update_table(self):
        players = self.match.home.players
        players.sort(key=lambda x: x.position.value)
        self.tblPlayers.setRowCount(len(players))
        for row, player in enumerate(players):
            item_player_name = QTableWidgetItem(player.name)
            is_selected = QTableWidgetItem("")
            if player.injury_length > 0:
                item_player_name.setForeground(QBrush(QColor(255, 0, 0)))
            else:
                is_selected.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                is_selected.setCheckState(QtCore.Qt.Unchecked)
            self.tblPlayers.setItem(row, 0, item_player_name)
            self.tblPlayers.setItem(row, 1, QTableWidgetItem(str(player.age)))
            self.tblPlayers.setItem(row, 2, QTableWidgetItem(player.position.name))
            self.tblPlayers.setItem(row, 3, QTableWidgetItem(str(player.attack)))
            self.tblPlayers.setItem(row, 4, QTableWidgetItem(str(player.defense)))
            self.tblPlayers.setItem(row, 5, is_selected)
            row += 1

    def update_combobox(self):
        for row in range(len(self.match.home.players)):
            for player in self.match.home.players:
                if self.tblPlayers.item(row, 0).text() == player.name and self.tblPlayers.item(row, 5).checkState():
                    if player.position.value == 1:
                        self.cbAtkGk.addItem(player.name)
                    elif player.position.value == 2:
                        self.cbAtkLw.addItem(player.name)
                    elif player.position.value == 3:
                        self.cbAtkLb.addItem(player.name)
                    elif player.position.value == 4:
                        self.cbAtkCb.addItem(player.name)
                    elif player.position.value == 5:
                        self.cbAtkP.addItem(player.name)
                    elif player.position.value == 6:
                        self.cbAtkRb.addItem(player.name)
                    elif player.position.value == 7:
                        self.cbAtkRw.addItem(player.name)
                    break

