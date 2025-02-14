#!/bin/python3
"""The user interface for the app."""
import sys

from PySide6.QtCore import ( 
    Qt,
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
from src.game import EuchreGame
import src.titles as _titles

from docs.constants import APP

class EuchreGUI(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.setWindowTitle("Python Euchre")
        self.setMinimumHeight(480)
        self.setMinimumWidth(960)

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
        self.player_layout = QVBoxLayout()
        self.btn_layout = QHBoxLayout()

        # Build Layout
   
        layout.addLayout(self.player_layout)
       
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
        print("New game starting...")
    
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
        pass

    @Slot()
    def user_pass(self):
        """Method to pass"""
        pass

    @Slot()
    def user_call(self):
        """Method to call a suit by the user."""
        pass

    @Slot()
    def user_order(self):
        """Method to order a card by the user."""
        pass

    def update_display(self):
        """Update the display to show cards."""
        for card in self.game.player.get_cards():
            card_name = f'{card.get_value()} of {card.get_suit()}'
            card_btn = QPushButton(card_name)
            self.player_layout.addWidget(card_btn)


class EuchreConsole():
    """Class for the console version of Euchre."""
    def __init__(self):
        pass
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

# Main loop for the game
def main():
    APP(sys.argv)
    game = EuchreGame()
    win = EuchreGUI(game)
    win.show()
    sys.exit(APP.exec())

if __name__ == '__main__':
    main()