from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import uic, QtWidgets
from PyQt5.QtGui import QBrush, QColor

uiMatch = "gui/match.ui"
formMatch, baseMatch = uic.loadUiType(uiMatch)


class Match(baseMatch, formMatch):
    def __init__(self, parent_window, match):
        super(baseMatch, self).__init__()

        self.setupUi(self)
        self.parent_window = parent_window

        self.match = match
        self.match.create_player_statistics()

        self.home_atk = self.create_dict_home_atk()
        self.home_def = self.create_dict_home_def()
        self.away_atk = self.create_dict_away_atk()
        self.away_def = self.create_dict_away_def()

        update_combobox(self.match.home_players, self.home_atk, self.home_def)
        update_combobox(self.match.away_players, self.away_atk, self.away_def)
        update_table(self.tblPlayerStatsHome, self.match.home_players)
        update_table(self.tblPlayerStatsAway, self.match.away_players)

        self.lblHome.setText(match.home.name)
        self.lblAway.setText(match.away.name)
        self.lblScore.setText(str(self.match.home_goals) + " : " + str(self.match.away_goals))
        self.lblTime.setText(str(self.match.time) + ":00")

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

    def start_match(self):
        if self.match.time == 60:
            self.parent_window.show()
            self.parent_window.child_window = None
            return

        if check_defense_valid(self.home_def) is False:
            return
        if check_defense_valid(self.away_def) is False:
            return

        player_names_h_atk = return_player_names(self.home_atk)
        player_names_h_def = return_player_names(self.home_def)
        player_names_a_atk = return_player_names(self.away_atk)
        player_names_a_def = return_player_names(self.away_def)
        self.match.start_match(player_names_h_atk, player_names_h_def, player_names_a_atk, player_names_a_def)

        update_table(self.tblPlayerStatsHome, self.match.home_players)
        update_table(self.tblPlayerStatsAway, self.match.away_players)

        self.lblScore.setText(str(self.match.home_goals) + " : " + str(self.match.away_goals))
        self.lblTime.setText(str(self.match.time) + ":00")
        if self.match.time == 30:
            self.btnStartMatch.setText("Continue Match")
        elif self.match.time == 60:
            self.btnStartMatch.setText("Finish Match")


def update_combobox(players_sm, pos_atk, pos_def):
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
    set_default_values(pos_def)


def set_default_values(pos_def):
    pos_def["lw"].setCurrentIndex(0)
    pos_def["lb"].setCurrentIndex(2)
    pos_def["cb"].setCurrentIndex(4)
    pos_def["p"].setCurrentIndex(6)
    pos_def["rb"].setCurrentIndex(8)
    pos_def["rw"].setCurrentIndex(10)


def check_defense_valid(pos_def):
    list_unique = []
    if pos_def["gk"].currentText() not in list_unique:
        list_unique.append(pos_def["gk"].currentText())
    if pos_def["lw"].currentText() not in list_unique:
        list_unique.append(pos_def["lw"].currentText())
    if pos_def["lb"].currentText() not in list_unique:
        list_unique.append(pos_def["lb"].currentText())
    if pos_def["cb"].currentText() not in list_unique:
        list_unique.append(pos_def["cb"].currentText())
    if pos_def["p"].currentText() not in list_unique:
        list_unique.append(pos_def["p"].currentText())
    if pos_def["rb"].currentText() not in list_unique:
        list_unique.append(pos_def["rb"].currentText())
    if pos_def["rw"].currentText() not in list_unique:
        list_unique.append(pos_def["rw"].currentText())
    if len(list_unique) < 7:
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setWindowTitle("Warning")
        error_dialog.setText("You can't use same player on more than 1 position!")
        error_dialog.exec_()
        return False
    else:
        return True


def return_player_names(pos):
    return [pos["gk"].currentText().split(' ')[0], pos["lw"].currentText().split(' ')[0],
            pos["lb"].currentText().split(' ')[0], pos["cb"].currentText().split(' ')[0],
            pos["p"].currentText().split(' ')[0], pos["rb"].currentText().split(' ')[0],
            pos["rw"].currentText().split(' ')[0]]


def update_table(table, players_sm):
    table.setRowCount(len(players_sm))
    for row, player_sm in enumerate(players_sm):
        table.setItem(row, 0, QTableWidgetItem(player_sm.player.name))
        table.setItem(row, 1, QTableWidgetItem(str(player_sm.player.age)))
        table.setItem(row, 2, QTableWidgetItem(player_sm.player.position.name))

        item_atk = QTableWidgetItem(str(player_sm.attack_rating))
        item_def = QTableWidgetItem(str(player_sm.defense_rating))

        if player_sm.attack_minutes > 0:
            if player_sm.attack_rating > player_sm.player.attack:
                item_atk.setForeground(QBrush(QColor(0, 255, 0)))
            elif player_sm.attack_rating == player_sm.player.attack:
                item_atk.setForeground(QBrush(QColor(0, 0, 255)))
            else:
                item_atk.setForeground(QBrush(QColor(255, 0, 0)))
            table.setItem(row, 3, item_atk)
        else:
            table.setItem(row, 3, QTableWidgetItem("0"))

        if player_sm.defense_minutes > 0:
            if player_sm.defense_rating > player_sm.player.defense:
                item_def.setForeground(QBrush(QColor(0, 255, 0)))
            elif player_sm.defense_rating == player_sm.player.defense:
                item_def.setForeground(QBrush(QColor(0, 0, 255)))
            else:
                item_def.setForeground(QBrush(QColor(255, 0, 0)))
            table.setItem(row, 4, item_def)
        else:
            table.setItem(row, 4, QTableWidgetItem("0"))

        table.setItem(row, 5, QTableWidgetItem(str(player_sm.attack_minutes + player_sm.defense_minutes)))
        row += 1
