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

        self.home_atk = self.create_dict_home_atk()
        self.home_def = self.create_dict_home_def()
        self.away_atk = self.create_dict_away_atk()
        self.away_def = self.create_dict_away_def()

        self.update_combobox(self.match.home_players, self.home_atk, self.home_def)
        self.update_combobox(self.match.away_players, self.away_atk, self.away_def)

        self.lblHome.setText(match.home.name)
        self.lblAway.setText(match.away.name)

        self.btnStartMatch.clicked.connect(self.start_match)

    def create_dict_home_atk(self):
        return {
            "gk": self.cbAtkGkH,
            "lw": self.cbAtkLwH,
            "lb": self.cbAtkLbH,
            "cb": self.cbAtkCbH,
            "p": self.cbAtkPH,
            "rb": self.cbAtkRbH,
            "rw": self.cbAtkRwH
        }

    def create_dict_home_def(self):
        return {
            "gk": self.cbDefGkH,
            "lw": self.cbDefLwH,
            "lb": self.cbDefLbH,
            "cb": self.cbDefCbH,
            "p": self.cbDefPH,
            "rb": self.cbDefRbH,
            "rw": self.cbDefRwH
        }

    def create_dict_away_atk(self):
        return {
            "gk": self.cbAtkGkA,
            "lw": self.cbAtkLwA,
            "lb": self.cbAtkLbA,
            "cb": self.cbAtkCbA,
            "p": self.cbAtkPA,
            "rb": self.cbAtkRbA,
            "rw": self.cbAtkRwA
        }

    def create_dict_away_def(self):
        return {
            "gk": self.cbDefGkA,
            "lw": self.cbDefLwA,
            "lb": self.cbDefLbA,
            "cb": self.cbDefCbA,
            "p": self.cbDefPA,
            "rb": self.cbDefRbA,
            "rw": self.cbDefRwA
        }

    def update_combobox(self, players_sm, pos_atk, pos_def):
        for player_sm in players_sm:
            if player_sm.player.position.value != 1:
                for key in pos_def.keys():
                    pos_def[key].addItem(player_sm.player.name + " " + str(player_sm.player.defense))
            if player_sm.player.position.value == 1:
                pos_atk["gk"].addItem(player_sm.player.name + " " + str(player_sm.player.defense))
                pos_def["gk"].addItem(player_sm.player.name + " " + str(player_sm.player.defense))
            elif player_sm.player.position.value == 2:
                pos_atk["lw"].addItem(player_sm.player.name + " " + str(player_sm.player.attack))
            elif player_sm.player.position.value == 3:
                pos_atk["lb"].addItem(player_sm.player.name + " " + str(player_sm.player.attack))
            elif player_sm.player.position.value == 4:
                pos_atk["cb"].addItem(player_sm.player.name + " " + str(player_sm.player.attack))
            elif player_sm.player.position.value == 5:
                pos_atk["p"].addItem(player_sm.player.name + " " + str(player_sm.player.attack))
            elif player_sm.player.position.value == 6:
                pos_atk["rb"].addItem(player_sm.player.name + " " + str(player_sm.player.attack))
            elif player_sm.player.position.value == 7:
                pos_atk["rw"].addItem(player_sm.player.name + " " + str(player_sm.player.attack))
        self.set_default_values(pos_def)

    @staticmethod
    def set_default_values(pos_def):
        pos_def["lw"].setCurrentIndex(0)
        pos_def["lb"].setCurrentIndex(2)
        pos_def["cb"].setCurrentIndex(4)
        pos_def["p"].setCurrentIndex(6)
        pos_def["rb"].setCurrentIndex(8)
        pos_def["rw"].setCurrentIndex(10)

    def start_match(self):
        self.check_defense_valid_and_substitutions()
        self.match.play(self.cbAtkLwH.currentText())

    def check_defense_valid_and_substitutions(self):
        list_unique = []
        if self.cbDefGkA.currentText() not in list_unique:
            list_unique.append(self.cbDefGkA.currentText().split(' ')[0])
        if self.cbDefLwA.currentText() not in list_unique:
            list_unique.append(self.cbDefLwA.currentText().split(' ')[0])
        if self.cbDefLbA.currentText() not in list_unique:
            list_unique.append(self.cbDefLbA.currentText().split(' ')[0])
        if self.cbDefCbA.currentText() not in list_unique:
            list_unique.append(self.cbDefCbA.currentText().split(' ')[0])
        if self.cbDefPA.currentText() not in list_unique:
            list_unique.append(self.cbDefPA.currentText().split(' ')[0])
        if self.cbDefRbA.currentText() not in list_unique:
            list_unique.append(self.cbDefRbA.currentText().split(' ')[0])
        if self.cbDefRwA.currentText() not in list_unique:
            list_unique.append(self.cbDefRwA.currentText().split(' ')[0])
        if len(list_unique) < 7:
            print(False)
            return
        subs_away = self.count_substitutions(list_unique)
        print(subs_away)

    def count_substitutions(self, list_unique):
        subs = 7
        if self.cbDefGkA.currentText().split(' ')[0] in list_unique:
            subs -= 1
        if self.cbAtkLwA.currentText().split(' ')[0] in list_unique:
            subs -= 1
        if self.cbAtkLbA.currentText().split(' ')[0] in list_unique:
            subs -= 1
        if self.cbAtkCbA.currentText().split(' ')[0] in list_unique:
            subs -= 1
        if self.cbAtkPA.currentText().split(' ')[0] in list_unique:
            subs -= 1
        if self.cbAtkRbA.currentText().split(' ')[0] in list_unique:
            subs -= 1
        if self.cbAtkRwA.currentText().split(' ')[0] in list_unique:
            subs -= 1
        return subs
