"""Module for Euchre game controller."""

# TODO update the display for each player
# TODO polish to slow down timing

from PySide6.QtCore import Signal, QObject

class EuchreController(QObject):
    bidding_requested = Signal()
    
    def __init__(self, game, view):
        super().__init__()
        self._game = game
        self._view = view

        self._view.new_game_start_pressed.connect(self.new_game)
        self.bidding_requested.connect(self._view.user_bidding)
        self._view.user_order_pressed.connect(self.bid_order)
        self._view.user_pass_pressed.connect(self.bid_order)
        self.main_menu()

    def main_menu(self):
        """Start on this menu."""
        self._view.state_main_menu()

    def new_game(self):
        """Start new game of play."""
        self._game.new_game()
        # for player in self._game.player_seating:
        #     self._view.create_playerLayout(player)
        self._view.create_player_layout(self._game.player)
        self._view.state_new_game()
        self.deal_cards()

    def deal_cards(self):
        """Deal some cards."""
        self._game.dealing()
        self._view.state_dealing()
        self.update_display()
        self._view.update_player_hand(self._game.player.position, self._game.player.cards)
        # self._view.update_display_msg(self._game.display_msg)
        self.bidding_round()

    def bidding_round(self):
        """Starts a new bidding round for the trump card."""
        self._game.initialize_bidding()
        self._view.state_bidding()
        self.update_display()
        
        for player in self._game.players:
            if player.is_bot():
                player.get_order(self._game.deck.revealed)
            else:
                self.bidding_requested.emit()

    def bid_order(self, order):
        """Return order."""
        print(order)

    def update_display(self):
        """Update the display."""
        self._view.update_display_msg(self._game.display_msg)
        # self._view_update_player_turn(self._game.current_player_turn)
        # self._view_update_score(self._game.score)
