import os
from PyQt5 import QtWidgets
from PyQt5 import uic


uiDialogNewGame = "gui/dialog_new_game.ui"
formDialogNewGame, baseDialogNewGame = uic.loadUiType(uiDialogNewGame)


class DialogNewGame(baseDialogNewGame, formDialogNewGame):
    def __init__(self, game):
        super(baseDialogNewGame, self).__init__()
        self.setupUi(self)
        self.game = game
        self.lblInfo.setText("")

    def accept(self):
        if os.path.exists("save/" + self.tbSaveName.text() + ".db"):
            self.lblInfo.setText("Save file with that name already exists!")
            self.open()
        elif self.tbSaveName.text().strip() == "":
            self.lblInfo.setText("Invalid name!")
            self.open()
        else:
            self.game.new_game(self.tbSaveName.text())
            super().accept()
