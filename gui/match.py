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

        self.btnStartMatch.clicked.connect(self.start_match)

    def start_match(self):
        pass
