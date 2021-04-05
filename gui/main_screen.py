from PyQt5.QtWidgets import QApplication, QTableWidgetItem
from PyQt5 import uic, QtCore, QtWidgets
from PyQt5.QtGui import QBrush, QColor
from gui.pre_match import PreMatch
import sys

uiMainScreen = "gui/main_screen.ui"
formMainScreen, baseMainScreen = uic.loadUiType(uiMainScreen)


class MainScreen(baseMainScreen, formMainScreen):
    def __init__(self, parent_window, game):
        super(baseMainScreen, self).__init__()

        self.setupUi(self)
        self.parent_window = parent_window
        self.child_window = None
        self.game = game
        self.fill_combobox_league()
        self.update_table_league()

        self.cbLeague.currentTextChanged.connect(self.update_table_league)
        self.btnNextMatch.clicked.connect(self.next_match)

    def fill_combobox_league(self):
        for league in self.game.leagues:
            self.cbLeague.addItem(league.name)

    def update_table_league(self):
        for league in self.game.leagues:
            if league.name == self.cbLeague.currentText():
                self.update_combobox_team(league)
                league.standings.sort(key=lambda x: [x.points(), x.goal_diff(), x.goals_for], reverse=True)

                self.tblLeague.setRowCount(len(league.standings))
                for row, club_s in enumerate(league.standings):
                    self.tblLeague.setItem(row, 0, QTableWidgetItem(club_s.club.name))
                    self.tblLeague.setItem(row, 1, QTableWidgetItem(str(club_s.played())))
                    self.tblLeague.setItem(row, 2, QTableWidgetItem(str(club_s.won)))
                    self.tblLeague.setItem(row, 3, QTableWidgetItem(str(club_s.drawn)))
                    self.tblLeague.setItem(row, 4, QTableWidgetItem(str(club_s.lost)))
                    self.tblLeague.setItem(row, 5, QTableWidgetItem(str(club_s.goals_for)))
                    self.tblLeague.setItem(row, 6, QTableWidgetItem(str(club_s.goals_away)))
                    self.tblLeague.setItem(row, 7, QTableWidgetItem(str(club_s.goal_diff())))
                    self.tblLeague.setItem(row, 8, QTableWidgetItem(str(club_s.points())))
                    row += 1
                header = self.tblLeague.horizontalHeader()
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
                break

    def update_combobox_team(self, league):
        self.cbTeam.clear()
        for team in league.teams:
            self.cbTeam.addItem(team.name)

    def next_match(self):
        self.game.schedule.sort(key=lambda x: [x.round, x.competition.get_id()])
        for match in self.game.schedule:
            if match.time == 0:
                self.child_window = PreMatch(self, match)
                self.child_window.show()
                self.hide()
                break
