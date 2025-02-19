#!/bin/python3
"""The user interface for the app."""
import sys

from PySide6.QtCore import ( 
    Qt,
    Signal,
    Slot,   
)

from PySide6.QtWidgets import (
    QPushButton,
    QLabel,
    QMainWindow,
    QMessageBox,
    QHBoxLayout,
    QVBoxLayout,
    QWidget
)
# import src.euchre as _euchre
import euchre.model.titles as _titles

class EuchreGUI(QMainWindow):
    new_game_start_pressed = Signal()
    user_discard_pressed = Signal()
    user_order_pressed = Signal()
    user_call_pressed = Signal()
    user_pass_pressed = Signal()
    align_center = Qt.AlignmentFlag.AlignCenter
    align_h_center = Qt.AlignmentFlag.AlignHCenter

    def __init__(self,):
        super().__init__()
        self.setWindowTitle("Python Euchre")
        self.setMinimumHeight(480)
        self.setMinimumWidth(960)
        self.plyr_layout_dict = {}

        # Menu
        menu = self.menuBar()
        aboutMenu = menu.addMenu("About")
        howto_action = aboutMenu.addAction("How to play")
        howto_action.triggered.connect(self.howto_trigger)
        credits_action = aboutMenu.addAction("View Credits")
        credits_action.triggered.connect(self.credits_trigger)

        # Buttons
        self.new_btn = QPushButton("New Game")
        self.new_btn.clicked.connect(self.new_game)
        
        self.quit_btn = QPushButton("Quit Game")
        self.quit_btn.clicked.connect(self.quit_game)

        # Window Layout Declaration
        layout = QVBoxLayout()
        self.table_layout = QVBoxLayout()
        
        # self.top_layout = QHBoxLayout()
        # self.mid_layout = QHBoxLayout()
        # self.bttm_layout = QHBoxLayout()

        self.btn_layout = QHBoxLayout()

        # Build Layout
  
        layout.addLayout(self.table_layout)
        layout.addLayout(self.btn_layout)
        self.btn_layout.addWidget(self.new_btn)
        self.btn_layout.addWidget(self.quit_btn)
               
        centralWidget = QWidget()
        centralWidget.setLayout(layout)

        self.setCentralWidget(centralWidget)

    def main_menu(self):
        """Main menu screen."""
        self.new_btn.show()
        self.quit_btn.show()

    @Slot()
    def new_game(self):
        """Slot to start a new game."""
        print("New game on GUI pressed...")
        self.new_btn.setDisabled(True)
        for btn in self.btn_layout.children():
            self.btn_layout.removeWidget(btn)
        self.new_game_start_pressed.emit()

    @Slot()
    def quit_game(self):
        """Exit the application."""
        sys.exit()

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
    def user_discard(self):
        """Method to discard a card."""
        print("Discarding card...")
        self.user_discard_pressed.emit()

    @Slot()
    def user_pass(self):
        """Method to pass"""
        print("Passing...")
        self.user_pass_pressed.emit()

    @Slot()
    def user_call(self):
        """Method to call a suit by the user."""
        print("User Call...")
        self.user_call_pressed.emit()

    @Slot()
    def user_order(self):
        """Method to order a card by the user."""
        print("Ordering....")
        self.user_order_pressed.emit()

    def create_player_layout(self, player):
        """Create instance of each players layout."""
        plyr_lyt = PlayerLayoutView(player)
        self.plyr_layout_dict[plyr_lyt.position] = plyr_lyt
        return plyr_lyt

    def update_player_hand(self,position, player_cards):
        """Update the player hand view"""
        lyt = self.plyr_layout_dict[get_lyt_pos(position)]
        for card in player_cards:
            card_btn = QPushButton(card.name)
            lyt.hand_lyt.addWidget(card_btn)

    def state_main_menu(self):
        """Display the main menu."""
        label = QLabel("Welcome to Euchre!")
        label.setAlignment(EuchreGUI.align_center)
        self.table_layout.addWidget(label)

    def state_new_game(self):
        """Display view for initializing a new game."""
        # for layout_obj in self.plyr_layout_dict.values():
        #     self.table_layout.addLayout(layout_obj.layout)
        self.table_layout.addLayout(self.plyr_layout_dict["bottom"].layout)


    def state_dealing(self):
        """Display view for Dealing round."""
        pass

    
class NewGameView():
    """Class to construct the view to initialize a new game."""
    def __init__(self):
        pass


class PlayerLayoutView():
    """Class to construct the layout of each player object view."""
    def __init__(self, player):
        self.layout = QVBoxLayout()
        self.hand_lyt = QHBoxLayout()
        self.label = QLabel(player.name)
        self.label.setAlignment(EuchreGUI.align_h_center)
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.hand_lyt)
        self.id = f"{player.name}_lyt"
        self.position = get_lyt_pos(player.position)

def get_lyt_pos(player_pos):
    """Return the position of the layout for this layout for the main window."""
    match player_pos:
        case 0:
            return "bottom"
        case 1:
            return "top"
        case 2:
            return "left"
        case 3:
            return "right"
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