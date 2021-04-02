import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5 import uic
from classes.game import Game
from classes.match import Match
from gui.dialog_new_game import DialogNewGame
from gui.pre_match import PreMatch


# Load ui files
uiMainWindow = "gui/start_screen.ui"
formMainWindow, baseMainWindow = uic.loadUiType(uiMainWindow)


class MainWindow(baseMainWindow, formMainWindow):
    def __init__(self):
        super(baseMainWindow, self).__init__()
        self.setupUi(self)
        self.game = Game()
        self.dialog = None
        self.child_window = None

        self.btnNewGame.clicked.connect(self.open_new_game_dialog)
        self.btnLoadGame.clicked.connect(self.open_load_game_dialog)

    def open_new_game_dialog(self):
        self.dialog = DialogNewGame(self.game)
        self.dialog.show()
        # self.dialog.accepted.connect(self.new_window)

    def open_load_game_dialog(self):
        file_path = QFileDialog.getOpenFileName(self, caption='Browse save file', directory='save/',
                                                filter='*.db')
        self.game.load_game(os.path.basename(file_path[0]).split('.')[0])
        self.new_window()

    def new_window(self):
        self.child_window = PreMatch(Match(self.game.clubs[0], self.game.clubs[1]))
        self.child_window.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
