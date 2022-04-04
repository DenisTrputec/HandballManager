from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5 import uic, QtCore, QtWidgets
from classes.contract_offer import ContractOffer
from classes.contract_offer import Status

uiPreMatch = "gui/contract_offers.ui"
formPreMatch, basePreMatch = uic.loadUiType(uiPreMatch)


def get_offer_value(offer):
    # Calculate main offer value
    value = offer.salary + offer.club_reputation
    if offer.player.club is not None and offer.club.get_id() == offer.player.club.get_id():
        value += offer.player.loyalty
    if offer.salary < offer.player.salary:
        value -= offer.player.salary - offer.salary
    return value


def tie_break(offer):
    value = 0

    # Combo between salary and length
    if offer.salary > (offer.player.attack + offer.player.defense):
        value += offer.length
    elif offer.salary < (offer.player.attack + offer.player.defense):
        value += offer.length * (-1) + 4
    else:
        value += 2 if offer.length == 2 else 1

    # Combo between age and length
    if offer.player.age <= 21:
        value += offer.length * (-1) + 4
    elif offer.player.age >= 33:
        value += offer.length
    else:
        value += 2 if offer.length == 2 else 1

    return value


class ContractOffers(basePreMatch, formPreMatch):
    def __init__(self, parent_window, game):
        super(basePreMatch, self).__init__()

        self.setupUi(self)
        self.parent_window = parent_window
        self.game = game
        self.players = [player for player in self.game.players if player.contract_length == 0]
        self.players.sort(key=lambda x: x.position.value)
        self.league_cnt = 0
        self.club_cnt = 0
        self.current_club = self.game.leagues[self.league_cnt].standings[self.club_cnt]
        self.current_offers = []
        self.next_club()
        self.btnConfirm.clicked.connect(self.confirm)
        self.btnNext.clicked.connect(self.next)

    def next_club(self):
        # Get current league and club
        self.current_club = self.game.leagues[self.league_cnt].standings[self.club_cnt].team
        self.lblClub.setText("Club: " + self.current_club.name)
        player_cnt = len([player for player in self.current_club.players if player.contract_length > 0])
        self.lblPlayers.setText("Players: " + str(player_cnt))
        self.lblBudget.setText("Budget: " + str(self.current_club.budget()))
        self.update_table()

    def update_table(self):
        self.tblPlayers.setRowCount(len(self.players))
        for row, player in enumerate(self.players):
            item_player_name = QTableWidgetItem(player.name)
            item_club_name = QTableWidgetItem(player.club.name if player.club is not None else "")
            is_selected = QTableWidgetItem("")
            is_selected.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            is_selected.setCheckState(QtCore.Qt.Unchecked)

            self.tblPlayers.setItem(row, 0, item_player_name)
            self.tblPlayers.setItem(row, 1, QTableWidgetItem(str(player.age)))
            self.tblPlayers.setItem(row, 2, QTableWidgetItem(player.position.name))
            self.tblPlayers.setItem(row, 3, QTableWidgetItem(str(player.attack)))
            self.tblPlayers.setItem(row, 4, QTableWidgetItem(str(player.defense)))
            self.tblPlayers.setItem(row, 5, item_club_name)
            self.tblPlayers.setItem(row, 6, is_selected)
            self.tblPlayers.setItem(row, 7, QTableWidgetItem(""))
            self.tblPlayers.setItem(row, 8, QTableWidgetItem(""))
            row += 1

        if len(self.players) > 0:
            header = self.tblPlayers.horizontalHeader()
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)
            header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)

    def confirm(self):
        self.current_offers = []
        for row, player in enumerate(self.players):
            if self.tblPlayers.item(row, 6).checkState():
                if self.is_offer_valid(row, player):
                    salary = int(self.tblPlayers.item(row, 7).text())
                    contract_len = int(self.tblPlayers.item(row, 8).text())
                    reputation = self.game.leagues[self.league_cnt].standings[self.club_cnt].points() / 3
                    contract_offer = ContractOffer(player, self.current_club, reputation, salary,
                                                   contract_len, self.game.week, Status.Pending)
                    self.current_offers.append(contract_offer)

    def next(self):
        cost = sum([offer.salary for offer in self.current_offers])
        cnt = len(self.current_offers)

        qm = QtWidgets.QMessageBox
        message = "Club: " + self.current_club.name + "\nNumber of players: " + str(cnt) + "\nCost: " + str(cost)
        ans = qm.question(self, "Are you sure?", message, qm.Yes | qm.No)
        if ans == qm.No:
            return

        for offer in self.current_offers:
            self.game.contract_offers.append(offer)

        self.club_cnt += 1
        if self.club_cnt < len(self.current_club.league.teams):
            self.next_club()
        else:
            self.league_cnt += 1
            self.club_cnt = 0

        if self.league_cnt >= 1 or self.club_cnt > 11 or self.game.week == 38:
            self.finish_week()

    def is_offer_valid(self, row, player):
        error_dialog = QtWidgets.QMessageBox()
        error_dialog.setWindowTitle("Warning")
        try:
            salary = int(self.tblPlayers.item(row, 7).text())
            if salary < 1:
                error_dialog.setText(player.name + " must have salary higher than 0")
                error_dialog.exec_()
                return False
        except ValueError:
            error_dialog.setText(player.name + " has invalid salary")
            error_dialog.exec_()
            return False
        try:
            contract_len = int(self.tblPlayers.item(row, 8).text())
            if contract_len < 1 or contract_len > 3:
                error_dialog.setText(player.name + " must have contract length between 1 and 3 years")
                error_dialog.exec_()
                return False
        except ValueError:
            error_dialog.setText(player.name + " has invalid contract length")
            error_dialog.exec_()
            return False
        return True

    def finish_week(self):
        for main_offer in self.game.contract_offers:

            # Check if offer salary is to low
            diff = 1 if self.game.week < 34 else 2
            if main_offer.player.position.value == 0:
                diff -= 1
            if (main_offer.player.attack + main_offer.player.defense - main_offer.salary) > diff:
                main_offer.status = Status.Rejected

            # Compare it with other offers
            if main_offer.status == Status.Pending:
                # Calculate main offer value
                mo_value = get_offer_value(main_offer)

                for other_offer in self.game.contract_offers:
                    # Only if same player, different offer and other offer status is Pending
                    if main_offer.player.get_id() == other_offer.player.get_id() and main_offer != other_offer \
                            and other_offer.status == Status.Pending:

                        # Calculate other offer value
                        oo_value = get_offer_value(other_offer)

                        # Direct comparison between two offers
                        if mo_value > oo_value:
                            other_offer.status = Status.Rejected

                        elif mo_value == oo_value:
                            mo_value += tie_break(main_offer)
                            oo_value += tie_break(other_offer)
                            if mo_value > oo_value:
                                other_offer.status = Status.Rejected
                            elif mo_value < oo_value:
                                main_offer.status = Status.Rejected
                            else:
                                if main_offer.salary >= other_offer.salary:
                                    other_offer.status = Status.Rejected
                                else:
                                    main_offer.status = Status.Rejected
                        else:
                            main_offer.status = Status.Rejected

            # If no better offer in last 2 weeks accept it
            if self.game.week - main_offer.week_offered >= 1 and main_offer.status == Status.Pending:
                main_offer.status = Status.Accepted

            print(main_offer)

        # Update contract offers list
        self.game.update_contract_offers_list()

        # Return to main screen
        self.parent_window.show()
        self.parent_window.setup_window()
        self.parent_window.btnNext.setText("Next Week")
        self.parent_window.child_window = None
