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
        self.update_table(self.match.home.players)
        self.btnConfirm.clicked.connect(self.update_combobox)

    def update_table(self, team_players):
        players = team_players
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
        players_selected = []
        self.clear_all_comboboxes()
        for row in range(self.tblPlayers.rowCount()):
            for player in self.match.home.players:
                if self.tblPlayers.item(row, 0).text() == player.name and self.tblPlayers.item(row, 5).checkState():
                    # if player.position.value != 1:
                    #     players_selected.append(player.name + " " + str(player.defense))
                    if player.position.value != 1:
                        self.cbDefLw.addItem(player.name + " " + str(player.defense))
                        self.cbDefLb.addItem(player.name + " " + str(player.defense))
                        self.cbDefCb.addItem(player.name + " " + str(player.defense))
                        self.cbDefP.addItem(player.name + " " + str(player.defense))
                        self.cbDefRb.addItem(player.name + " " + str(player.defense))
                        self.cbDefRw.addItem(player.name + " " + str(player.defense))
                    if player.position.value == 1:
                        self.cbAtkGk.addItem(player.name + " " + str(player.defense))
                        self.cbDefGk.addItem(player.name + " " + str(player.defense))
                    elif player.position.value == 2:
                        self.cbAtkLw.addItem(player.name + " " + str(player.attack))
                    elif player.position.value == 3:
                        self.cbAtkLb.addItem(player.name + " " + str(player.attack))
                    elif player.position.value == 4:
                        self.cbAtkCb.addItem(player.name + " " + str(player.attack))
                    elif player.position.value == 5:
                        self.cbAtkP.addItem(player.name + " " + str(player.attack))
                    elif player.position.value == 6:
                        self.cbAtkRb.addItem(player.name + " " + str(player.attack))
                    elif player.position.value == 7:
                        self.cbAtkRw.addItem(player.name + " " + str(player.attack))
                    break
        self.set_default_values()
        # self.defense_combobox(players_selected)

    def clear_all_comboboxes(self):
        self.cbAtkGk.clear()
        self.cbAtkLw.clear()
        self.cbAtkLb.clear()
        self.cbAtkCb.clear()
        self.cbAtkP.clear()
        self.cbAtkRb.clear()
        self.cbAtkRw.clear()
        self.cbDefGk.clear()
        self.cbDefLw.clear()
        self.cbDefLb.clear()
        self.cbDefCb.clear()
        self.cbDefP.clear()
        self.cbDefRb.clear()
        self.cbDefRw.clear()

    def set_default_values(self):
        # self.cbDefLw.setCurrentIndex(self.cbDefLw.findText(self.cbAtkLw.currentText().split(' ')[0]))
        # self.cbDefLb.setCurrentIndex(self.cbDefLb.findText(self.cbAtkLb.currentText().split(' ')[0]))
        # self.cbDefCb.setCurrentIndex(self.cbDefCb.findText(self.cbAtkCb.currentText().split(' ')[0]))
        # self.cbDefP.setCurrentIndex(self.cbAtkP.findText(self.cbAtkP.currentText().split(' ')[0]))
        # self.cbDefRb.setCurrentIndex(self.cbAtkRb.findText(self.cbAtkRb.currentText().split(' ')[0]))
        # self.cbDefRw.setCurrentIndex(self.cbAtkRw.findText(self.cbAtkRw.currentText().split(' ')[0]))
        self.cbDefLw.setCurrentIndex(0)
        self.cbDefLb.setCurrentIndex(2)
        self.cbDefCb.setCurrentIndex(4)
        self.cbDefP.setCurrentIndex(6)
        self.cbDefRb.setCurrentIndex(8)
        self.cbDefRw.setCurrentIndex(10)

    def defense_combobox(self, players):
        list1 = [player for player in players]
        self.cbDefLw.addItems(list1)
        list2 = [player for player in list1 if player != self.cbDefLw.currentText()]
        self.cbDefLb.addItems(list2)
        list3 = [player for player in list2 if player != self.cbDefLb.currentText()]
        self.cbDefCb.addItems(list3)
        list4 = [player for player in list3 if player != self.cbDefCb.currentText()]
        self.cbDefP.addItems(list4)
        list5 = [player for player in list4 if player != self.cbDefP.currentText()]
        self.cbDefRb.addItems(list5)
        list6 = [player for player in list5 if player != self.cbDefRb.currentText()]
        self.cbDefRw.addItems(list6)
        for i in range(5):
            self.cbDefLw.removeItem(1)
