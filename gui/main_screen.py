import logging
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from gui.pre_match import PreMatch
from gui.contract_offers import ContractOffers
from gui.injury_update import InjuryUpdate


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
        self.setup_window()
        # self.update_table_league()

        self.cbLeague.currentTextChanged.connect(self.update_table_league)
        self.cbSchedule.currentTextChanged.connect(self.update_table_schedule)
        self.cbTeam.currentTextChanged.connect(self.update_table_team)
        self.btnNext.clicked.connect(self.next)
        self.actSaveGame.triggered.connect(self.game.save_game)

    def setup_window(self):
        self.check_if_next_week()
        self.lblWeek.setText("Week: " + str(self.game.week))
        self.update_table_league()

    def fill_combobox_league(self):
        print("fill_combobox_league")
        for league in self.game.leagues:
            self.cbLeague.addItem(league.name)
        print("fill_combobox_league executed")

    def update_table_league(self):
        print("update_table_league")
        for league in self.game.leagues:
            if league.name == self.cbLeague.currentText():
                print("->update_combobox_team")
                self.update_combobox_team(league)
                print("->update_combobox_schedule")
                self.update_combobox_schedule(league)

                self.tblLeague.setRowCount(len(league.standings))
                for row, team_s in enumerate(league.standings):
                    self.tblLeague.setItem(row, 0, QTableWidgetItem(team_s.team.name))
                    self.tblLeague.setItem(row, 1, QTableWidgetItem(str(team_s.played())))
                    self.tblLeague.setItem(row, 2, QTableWidgetItem(str(team_s.won)))
                    self.tblLeague.setItem(row, 3, QTableWidgetItem(str(team_s.drawn)))
                    self.tblLeague.setItem(row, 4, QTableWidgetItem(str(team_s.lost)))
                    self.tblLeague.setItem(row, 5, QTableWidgetItem(str(team_s.goals_for)))
                    self.tblLeague.setItem(row, 6, QTableWidgetItem(str(team_s.goals_away)))
                    self.tblLeague.setItem(row, 7, QTableWidgetItem(str(team_s.goal_diff())))
                    self.tblLeague.setItem(row, 8, QTableWidgetItem(str(team_s.points())))
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
        print("update_table_league executed")

    def update_combobox_team(self, league):
        print("update_combobox_team, arg", league.name)
        self.cbTeam.clear()
        league.standings.sort(key=lambda x: [x.points(), x.goal_diff(), x.goals_for], reverse=True)
        for team_sc in league.standings:
            for team in league.teams:
                if team_sc.team == team:
                    print("update_combobox_team", team.name)
                    self.cbTeam.addItem(team.name)
                    break
        self.cbTeam.setMaxVisibleItems(len(league.standings))
        print("->update_table_team")
        self.update_table_team()
        print("update_combobox_team executed")

    def update_table_team(self):
        print("update_table_team")
        if self.cbTeam.count() == 0:
            return
        self.tblTeam.setRowCount(0)
        for league in self.game.leagues:
            if league.name == self.cbLeague.currentText():
                for club in league.teams:
                    if self.cbTeam.currentText() == club.name:
                        self.tblTeam.setRowCount(len(club.players))
                        break
                row = 0
                for player_sc in league.players_sc:
                    if player_sc.player.club.name == self.cbTeam.currentText():
                        self.tblTeam.setItem(row, 0, QTableWidgetItem(player_sc.player.name))
                        self.tblTeam.setItem(row, 1, QTableWidgetItem(str(player_sc.player.age)))
                        self.tblTeam.setItem(row, 2, QTableWidgetItem(player_sc.player.position.name))
                        self.tblTeam.setItem(row, 3, QTableWidgetItem(str(player_sc.games)))
                        self.tblTeam.setItem(row, 4, QTableWidgetItem(str(player_sc.attack_games)))
                        self.tblTeam.setItem(row, 5, QTableWidgetItem(str(player_sc.attack_rating)))
                        self.tblTeam.setItem(row, 6, QTableWidgetItem(str(player_sc.attack_minutes)))
                        self.tblTeam.setItem(row, 7, QTableWidgetItem(str(player_sc.defense_games)))
                        self.tblTeam.setItem(row, 8, QTableWidgetItem(str(player_sc.defense_rating)))
                        self.tblTeam.setItem(row, 9, QTableWidgetItem(str(player_sc.defense_minutes)))
                        row += 1
                        if row == len(league.players_sc):
                            break
                if len(league.players_sc) > 0:
                    header = self.tblTeam.horizontalHeader()
                    header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
                    header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
                    header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
                    header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
                    header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
                    header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
                    header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
                    header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
                    header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)
                    header.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)
                    break
                break
        print("update_table_team executed")

    def update_combobox_schedule(self, league):
        print("update_table_team")
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
        print("->update_table_schedule")
        self.update_table_schedule()
        print("update_table_team executed")

    def update_table_schedule(self):
        print("update_table_schedule")
        for league in self.game.leagues:
            if league.name == self.cbLeague.currentText():
                self.tblSchedule.setRowCount(len(league.teams) // 2)
                row = 0
                for match in league.schedule:
                    if match.round == self.cbSchedule.currentIndex() + 1:
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
        print("update_table_schedule executed")

    def next(self):
        if self.btnNext.text() == "Next Match":
            self.next_match()
        elif self.btnNext.text() == "Next Week":
            self.update_injuries()
            self.game.week += 1
            self.lblWeek.setText("Week: " + str(self.game.week))
            if self.game.week == 29:
                for league in self.game.leagues:
                    league.payout()
            self.check_if_next_week()
        elif self.btnNext.text() == "Contract Offers":
            self.contract_offers()

    def next_match(self):
        self.game.schedule.sort(key=lambda x: [x.round, x.competition.get_id()])
        for match in self.game.schedule:
            if match.time == 0:
                self.child_window = PreMatch(self, match)
                self.child_window.show()
                self.hide()
                break

    def check_if_next_week(self):
        is_transfer_window_open = True if 30 <= self.game.week <= 38 else False

        is_finished = True
        for event in self.game.calendar:
            if self.game.week == event[0]:
                for match in self.game.schedule:
                    if match.round == event[2] and match.time == 0:
                        is_finished = False
                        break
        if is_transfer_window_open:
            self.game.create_new_players()
            self.btnNext.setText("Contract Offers")
        elif is_finished:
            self.btnNext.setText("Next Week")
        else:
            self.btnNext.setText("Next Match")

    def update_injuries(self):
        self.child_window = InjuryUpdate(self, self.game)
        self.child_window.show()

    def contract_offers(self):
        self.child_window = ContractOffers(self, self.game)
        self.child_window.show()
        self.hide()
