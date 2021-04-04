from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QBrush, QColor
import gui.match
import sys

uiMainScreen = "gui/main_screen.ui"
formMainScreen, baseMainScreen = uic.loadUiType(uiMainScreen)


class MainScreen(baseMainScreen, formMainScreen):
    def __init__(self, parent_window, game):
        super(baseMainScreen, self).__init__()

        self.setupUi(self)
        self.parent_window = parent_window
        self.game = game
        self.fill_combobox_league()
        # self.update_table_league()

        self.cbLeague.currentTextChanged.connect(self.update_table_league)

    def fill_combobox_league(self):
        for league in self.game.leagues:
            self.cbLeague.addItem(league.name)

    def update_table_league(self):
        print(self.cbLeague.currentText())
        # for league in self.game.leagues:
        #     if league.name == self.cbLeague.currentText():
        #         self.tblPlayers.setRowCount(len(league.teams))

