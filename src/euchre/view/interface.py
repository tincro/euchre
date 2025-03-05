#!/bin/python3
"""The user interface for the app."""

from PySide6.QtCore import ( 
    Qt,
    Signal,
    Slot,   
)

from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget
)
# import src.euchre as _euchre
import euchre.model.titles as _titles
from euchre.model.cards import Card

ALIGN_CENTER = Qt.AlignmentFlag.AlignCenter
ALIGN_H_CENTER = Qt.AlignmentFlag.AlignHCenter

class EuchreGUI(QMainWindow):
    
    new_game_start_pressed = Signal()
    user_discard_pressed = Signal(Card)
    user_order_pressed = Signal(tuple)
    user_call_pressed = Signal(tuple)
    user_pass_pressed = Signal(tuple)
    user_play_pressed = Signal(int)
    user_game_over_pressed = Signal(str)
    user_quit_pressed = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Euchre Simulator")
        self.setMinimumHeight(480)
        self.setMinimumWidth(960)
        self.plyr_layout_dict = {}

        # Menu
        self.build_menu()

        # Bottom Buttons
        self.new_btn = QPushButton("New Game")
        self.new_btn.clicked.connect(
            lambda: self.new_game_start_pressed.emit()
        )
        
        self.quit_btn = QPushButton("Quit Game")
        self.quit_btn.clicked.connect(
            lambda : self.user_quit_pressed.emit()
        )

        # Window Layout Declaration
        layout = QVBoxLayout()
        self.table_layout = QGridLayout()

        self.build_display()

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.new_btn)
        self.btn_layout.addWidget(self.quit_btn)

        # Build Layout
        layout.addLayout(self.display_layout)
        layout.addLayout(self.table_layout)        
        layout.addLayout(self.btn_layout)
               
        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

    def build_display(self):
        """Build the display message box for the current status of the game."""
        self.display_layout = QHBoxLayout()
        self.display_msg = QLabel("")
        self.display_msg.setAlignment(ALIGN_H_CENTER)
        self.display_layout.addWidget(self.display_msg)

    def build_menu(self):
        """Build the top menu for the GUI."""
        menu = self.menuBar()
        aboutMenu = menu.addMenu("About")
        howto_action = aboutMenu.addAction("How to play")
        howto_action.triggered.connect(self.howto_trigger)
        credits_action = aboutMenu.addAction("View Credits")
        credits_action.triggered.connect(self.credits_trigger)

    @Slot()
    def credits_trigger(self):
        """Reveal the information for the credits for the game application."""
        info = QMessageBox()
        info.setText(_titles.credits())
        info.setWindowTitle("Credits")
        info.exec()

    @Slot()
    def howto_trigger(self):
        """Display the How to Play information."""
        info = QMessageBox()
        info.setText("How to play!")
        info.setWindowTitle("How to Play")
        info.exec()
    
    @Slot()
    def user_discard_view(self, cards):
        """Method to discard a card."""
        # print("Discarding card...")
        # self.user_discard_pressed.emit()
        dialog = QDialog()
        dialog.setWindowTitle("Choose a card to discard...")
        layout = QHBoxLayout()

        for card in cards:
            card_btn = QPushButton()
            card_btn.setText(card.name)
            card_btn.clicked.connect(dialog.accept)
            card_btn.clicked.connect(lambda _, c=card:self.user_discard_pressed.emit(c))
            layout.addWidget(card_btn)

        dialog.setLayout(layout)
        dialog.exec()

    @Slot()
    def user_bidding_view(self):
        """Get the player bidding for this round."""
        bid = QDialog()
        bid.setWindowTitle("Do you order or pass?")
        layout = QVBoxLayout()
        chk_layout = QHBoxLayout()
        btn_layout = QHBoxLayout()

        box = QCheckBox("Going alone?")
        box.setCheckable(True)
        chk_layout.addWidget(box)
        layout.addLayout(chk_layout)

        order_btn = QPushButton("Order")
        order_btn.clicked.connect(bid.accept)
        bid.accepted.connect(
            lambda x=order_btn.text(),
                a=box.isChecked: self.user_order_pressed.emit((x, a())))
        btn_layout.addWidget(order_btn)

        pass_btn = QPushButton("Pass")
        pass_btn.clicked.connect(bid.reject)
        bid.rejected.connect(
            lambda x=pass_btn.text(),
                a=box.isChecked: self.user_pass_pressed.emit((x, a())))
        btn_layout.addWidget(pass_btn)
        layout.addLayout(btn_layout)
        
        bid.setLayout(layout)
        bid.exec()
    
    @Slot()
    def user_playing_view(self, enable_list, card_list):
        """View for user to play cards."""
        print(f'Human Player choose a card...')
        # self.enable_player_hand(enable_list)

        win = QDialog()
        win.setWindowTitle('Choose a card to play...')
        layout = QHBoxLayout()

        for card in card_list:
            index = card_list.index(card)
            card_btn = QPushButton()
            card_btn.setText(card.name)
            card_btn.clicked.connect(win.accept)
            card_btn.clicked.connect(
                lambda _, i=index: self.user_play_pressed.emit(i)
            )
            if index not in enable_list:
                card_btn.setDisabled(True)
            layout.addWidget(card_btn)

        win.setLayout(layout)
        win.exec()

    @Slot()
    def user_calling_view(self, card_suit):
        """Get the player calling for this round."""
        SUITS = ["Spades", "Diamonds", "Clubs", "Hearts"]

        call_win = QDialog()
        call_win.setWindowTitle("Do you want to call Trump?")
        layout = QVBoxLayout()
        check_layout = QHBoxLayout()
        card_layout = QHBoxLayout()
        pass_layout = QHBoxLayout()

        box = QCheckBox("Going alone?")
        box.setCheckable(True)
        check_layout.addWidget(box)
        layout.addLayout(check_layout)

        for suit in SUITS:
            suit_btn = QPushButton(suit)
            card_layout.addWidget(suit_btn)
            suit_btn.clicked.connect(call_win.accept)
            suit_btn.clicked.connect(
                lambda _,
                    s=suit,
                    c=box.isChecked: self.user_call_pressed.emit((s, c()))) 
            if suit == card_suit:
                suit_btn.setDisabled(True)
        layout.addLayout(card_layout)

        pass_btn = QPushButton('Pass')
        pass_layout.addWidget(pass_btn)
        pass_btn.clicked.connect(call_win.reject)
        pass_btn.clicked.connect(
            lambda _, s=pass_btn.text(): self.user_call_pressed.emit(s)) 
        layout.addLayout(pass_layout)

        call_win.setLayout(layout)
        call_win.exec()

    @Slot()
    def game_over_view(self):
        """The View for the game over."""
        options = ["new game", "quit"]
        win = QDialog()
        win.setWindowTitle("Congratulations!")
        layout = QHBoxLayout()

        for option in options:
            btn = QPushButton(option.capitalize())
            btn.clicked.connect(win.accept)
            btn.clicked.connect(
                lambda _, x=option: self.user_game_over_pressed.emit(x)
            )
            layout.addWidget(btn)

        win.setLayout(layout)
        win.exec()

    def update_display_msg(self, msg):
        """Update the display message for the player."""
        self.display_msg.setText(msg)

    def state_main_menu(self):
        """Display the main menu."""
        self.welcome = QLabel("Welcome to Euchre!")
        self.welcome.setAlignment(ALIGN_CENTER)
        self.table_layout.addWidget(self.welcome)

    def state_new_game(self):
        """Display view for initializing a new game."""
        # for layout_obj in self.plyr_layout_dict.values():
        #     self.table_layout.addLayout(layout_obj.layout)
        for layout_obj in self.plyr_layout_dict.values():
            self.table_layout.addLayout(
                layout_obj.layout,
                layout_obj.position['row'],
                layout_obj.position['column']
            )
        
        # lyt = self.plyr_layout_dict["bottom"]
        # self.table_layout.addLayout(
        #     lyt.layout,
        #     lyt.position['row'],
        #     lyt.position['column']
        # )
        self.welcome.hide()
        self.new_btn.hide()
        self.quit_btn.hide()

    def state_dealing(self, msg):
        """Display view for Dealing round."""
        self.update_display_msg(msg)
    
    def state_bidding(self):
        """Display view for Bidding round."""
        pass

    def create_player_layout(self, player):
        """Create instance of each players layout."""
        plyr_lyt = PlayerLayoutView(player)
        
        self.plyr_layout_dict[plyr_lyt.position['position']] = plyr_lyt
        return plyr_lyt
    
    def create_bot_layout(self, bot_list):
        """Create the layout for bot players."""
        for bot in bot_list:
            bot_lyt = BotLayoutView(bot)
            self.plyr_layout_dict[bot_lyt.position['position']] = bot_lyt
        
    def update_player_hand(self, player_cards, position='bottom'):
        """Update the player hand view"""
        lyt = self.plyr_layout_dict[position]
        lyt.refresh_hand()
        for card in player_cards:
            card_btn = QPushButton(card.name)
            lyt.hand_lyt.addWidget(card_btn)

    def enable_player_hand(self, en_list: list[int], position=0):
        """Enable the player hand buttons for the cards.
        
        keyword arguments:
        - en_list:list of index for the player hand.
        - position: int position for the player view
        """
        lyt = self.plyr_layout_dict[get_lyt_config(position)]
        lyt.enable_hand(en_list)

    def disable_player_hand(self, position=0):
        """Disable the player hand."""
        lyt = self.plyr_layout_dict[get_lyt_config(position)]
        lyt.disable_hand()



class BotLayoutView():
    """Class to construct the layout of each bot player view."""
    def __init__(self, bot):
        self.layout = QVBoxLayout()
        self.hand_lyt = QHBoxLayout()

        self.label = QLabel(bot.name)
        self.label.setAlignment(ALIGN_H_CENTER)
        self.layout.addWidget(self.label)

        self.id = f"{bot.name}_lyt"
        self.position = get_lyt_config(bot.position)


        # bot hand = small icons for cards, width of name?
        # bot card played = single icon full image card
        

class PlayerLayoutView():
    """Class to construct the layout of each player object view."""
    def __init__(self, player):
        self.layout = QVBoxLayout()
        self.hand_lyt = QHBoxLayout()
        self.label = QLabel(player.name)
        self.label.setAlignment(ALIGN_H_CENTER)
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.hand_lyt)
        self.id = f"{player.name}_lyt"
        self.position = get_lyt_config(player.position)

    def refresh_hand(self):
        """Clean up the the hand layout."""
        count = self.hand_lyt.count()
        while count > 0:
            index = count - 1
            widget = self.hand_lyt.itemAt(index).widget()
            self.hand_lyt.removeWidget(widget)
            widget.hide()
            count -= 1

    def enable_hand_list(self, indexes):
        """Enable the hand of cards to play."""
        for index in indexes:
            widget = self.hand_lyt.itemAt(index).widget()
            widget.setDisabled(False)

    def disable_hand(self):
        """Disable the hand of cards."""
        count = self.hand_lyt.count()
        while count > 0:
            index = count - 1
            widget = self.hand_lyt.itemAt(index).widget()
            widget.setDisabled(True)
            count -= 1


def get_lyt_config(player_pos):
    """Return the position of the layout for this layout for the main window."""
    match player_pos:
        case 0:
            config = {
                'position': "bottom",
                'row': 2,
                'column': 1
            }
            return config
        case 1:
            config = {
                'position': 'top',
                'row': 0,
                'column': 1
            }
            return config
        case 2:
            config = {
                'position': 'left',
                'row': 1,
                'column': 0
            }
            return config
        case 3:
            config = {
                'position': 'right',
                'row': 1,
                'column': 2
            }
            return config
        case _:
            print("ERROR: NO VALID POSITION FOR PLAYER LAYOUT")
            return None

# class EuchreConsole():
#     """Class for the console version of Euchre."""
#     def __init__(self):
#         pass
    # def get_call(self, previous_revealed: Card) -> str:
    #     """Get call from the player. Only acceptable options are 'Hearts', 'Spades', 'Diamonds', or 'Clubs'.
    #     Player cannot chose the trump that was already bidded.

    #     Keyword arguments:
    #     previous_revealed: -- Revealed card from the top of deck.
    #     """
    #     if not previous_revealed:
    #         return
        
    #     suit = previous_revealed.get_suit().lower()
    #     call = None
    #     while call is None:
    #         call = input("Enter suit ({}) for trump or pass: -> ".format(', '.join(suit for suit in Card.SUITS)))
    #         if call.lower() == 'pass':
    #             return call.lower()
    #         elif call.lower() != suit:
    #             if call.capitalize() in Card.SUITS:
    #                 return call.capitalize()
    #             else:
    #                 call = None
    #         else:
    #             call = None

    # def get_order(self, revealed: Card) -> str:
    #     """Get order from the player. Only acceptable options are 'order' or 'pass'.

    #     Keyword arguments:
    #     revealed: -- Revealed card from the top of deck.
    #     """
    #     if not revealed:
    #         return
        
    #     order = None
    #     while order is None:
    #         # print(f'Order {revealed} or pass?: ->')
    #         order = input(f'Order {revealed} or pass?: ->')
            
    #         if (order.lower() == 'order' or order.lower() == 'yes') or order.lower() == 'pass':
    #             return order.lower()
    #         else:
    #             order = None

    # def get_player_card(self, legal_card_list: list[tuple [int, Card]]) -> int:
    #     """Get player input choosing a card from the list in hand. Returns 
    #     number assignment (integer) of card to play.

    #     Keyword arguments:
    #     legal_card_list: -- List of cards able to be played this round.
    #     """
    #     if not legal_card_list:
    #         return
        
    #     card = None
    #     while card is None:
    #         card = input("Enter the number of a card you'd like to choose: -> ")
    #         if card.isdigit():
    #             if int(card) <= len(legal_card_list) and int(card) > 0:
    #                 return int(card)
    #             else:
    #                 card = None    
    #         else:
    #             card = None

    # def get_player_status(self, cards:list[tuple [int, Card]]=None, trump: Trump=None):
    #     """Print the player's name and the current legal cards in their respective hand of cards."""
    #     print('\n')
    #     print('-' * 40)
    #     print(f'\tPLAYER: {self._name} \tTEAM: {self._team.get_name()}')
    #     print('-' * 40)
    #     if trump:
    #         print(f'CARDS IN HAND: \t\tTRUMP: {trump.get_suit()}')
    #     else:
    #         print(f'CARDS IN HAND: ')
    #     if cards:
    #         for card in cards:
    #             print(f'\t{card[0]}. {card[1]}')
    #     else:
    #         for card in self.list_cards():
    #             print(f'\t{card[0]}. {card[1]}')
    #     print('-' * 40)