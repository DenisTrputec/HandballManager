from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QBrush, QColor
import sys

uiMatch = "gui/match.ui"
formMatch, baseMatch = uic.loadUiType(uiMatch)


class Match(baseMatch, formMatch):
    def __init__(self, match):
        super(baseMatch, self).__init__()

        self.setupUi(self)
        self.match = match
        self.match.create_player_statistics()
        self.update_combobox()

        self.lblHome.setText(match.home.name)
        self.lblAway.setText(match.away.name)

        self.btnStartMatch.clicked.connect(self.start_match)

    def update_combobox(self):
        for player_sm in self.match.home_players:
            if player_sm.player.position.value != 1:
                self.cbDefLwH.addItem(player_sm.player.name + " " + str(player_sm.player.defense))
                self.cbDefLbH.addItem(player_sm.player.name + " " + str(player_sm.player.defense))
                self.cbDefCbH.addItem(player_sm.player.name + " " + str(player_sm.player.defense))
                self.cbDefPH.addItem(player_sm.player.name + " " + str(player_sm.player.defense))
                self.cbDefRbH.addItem(player_sm.player.name + " " + str(player_sm.player.defense))
                self.cbDefRwH.addItem(player_sm.player.name + " " + str(player_sm.player.defense))
            if player_sm.player.position.value == 1:
                self.cbAtkGkH.addItem(player_sm.player.name + " " + str(player_sm.player.defense))
                self.cbDefGkH.addItem(player_sm.player.name + " " + str(player_sm.player.defense))
            elif player_sm.player.position.value == 2:
                self.cbAtkLwH.addItem(player_sm.player.name + " " + str(player_sm.player.attack))
            elif player_sm.player.position.value == 3:
                self.cbAtkLbH.addItem(player_sm.player.name + " " + str(player_sm.player.attack))
            elif player_sm.player.position.value == 4:
                self.cbAtkCbH.addItem(player_sm.player.name + " " + str(player_sm.player.attack))
            elif player_sm.player.position.value == 5:
                self.cbAtkPH.addItem(player_sm.player.name + " " + str(player_sm.player.attack))
            elif player_sm.player.position.value == 6:
                self.cbAtkRbH.addItem(player_sm.player.name + " " + str(player_sm.player.attack))
            elif player_sm.player.position.value == 7:
                self.cbAtkRwH.addItem(player_sm.player.name + " " + str(player_sm.player.attack))

    def start_match(self):
        self.match.play(self.cbAtkLwH.currentText())
