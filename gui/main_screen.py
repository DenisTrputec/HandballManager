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
        self.cbSchedule.currentTextChanged.connect(self.update_table_schedule)
        self.btnNextMatch.clicked.connect(self.next_match)

    def fill_combobox_league(self):
        for league in self.game.leagues:
            self.cbLeague.addItem(league.name)

    def update_table_league(self):
        for league in self.game.leagues:
            if league.name == self.cbLeague.currentText():
                self.update_combobox_team(league)
                self.update_combobox_schedule(league)
                league.standings.sort(key=lambda x: [x.points(), x.goal_diff(), x.goals_for], reverse=True)

                self.tblLeague.setRowCount(len(league.standings))
                for row, team_s in enumerate(league.standings):
                    self.tblLeague.setItem(row, 0, QTableWidgetItem(team_s.club.name))
                    self.tblLeague.setItem(row, 1, QTableWidgetItem(str(team_s.played())))
                    self.tblLeague.setItem(row, 2, QTableWidgetItem(str(team_s.won)))
                    self.tblLeague.setItem(row, 3, QTableWidgetItem(str(team_s.drawn)))
                    self.tblLeague.setItem(row, 4, QTableWidgetItem(str(team_s.lost)))
                    self.tblLeague.setItem(row, 5, QTableWidgetItem(str(team_s.goals_for)))
                    self.tblLeague.setItem(row, 6, QTableWidgetItem(str(team_s.goals_away)))
                    self.tblLeague.setItem(row, 7, QTableWidgetItem(str(team_s.goal_diff())))
                    self.tblLeague.setItem(row, 8, QTableWidgetItem(str(team_s.points())))
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

    def update_combobox_schedule(self, league):
        self.cbSchedule.clear()
        for i in range(len(league.schedule) // len(league.teams) * 2):
            self.cbSchedule.addItem("Round " + str(i + 1))

        cnt = index = 0
        for match in league.schedule:
            if match.time == 0:
                cnt += 1
                if cnt == 1:
                    index = match.round - 1
                if cnt == len(league.teams) // 2:
                    self.cbSchedule.setCurrentIndex(index)
                    break
            else:
                cnt = 0
        self.update_table_schedule()

    def update_table_schedule(self):
        for league in self.game.leagues:
            if league.name == self.cbLeague.currentText():
                self.tblSchedule.setRowCount(len(league.teams) // 2)
                row = 0
                for match in league.schedule:
                    if match.round == self.cbSchedule.currentIndex() + 1:
                        print(match)
                        self.tblSchedule.setItem(row, 0, QTableWidgetItem(match.home.name))
                        self.tblSchedule.setItem(row, 1, QTableWidgetItem(match.away.name))
                        if match.time == 60:
                            self.tblSchedule.setItem(row, 2, QTableWidgetItem(
                                str(match.home_goals) + ":" + str(match.away_goals)))
                        else:
                            self.tblSchedule.setItem(row, 2, QTableWidgetItem(""))
                        row += 1
                    if row == len(league.teams) // 2:
                        break
                header = self.tblSchedule.horizontalHeader()
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
                header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
                break

    def next_match(self):
        self.game.schedule.sort(key=lambda x: [x.round, x.competition.get_id()])
        for match in self.game.schedule:
            if match.time == 0:
                self.child_window = PreMatch(self, match)
                self.child_window.show()
                self.hide()
                break
