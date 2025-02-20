"""Module for Euchre game controller."""

# TODO update the display for each player
# TODO polish to slow down timing
# TODO Need to correct the order of player turns, refactor here.

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
        self.init_new_game()
        self.deal_cards()
        self.bidding_round()
        if self._game.trump:
            self.pickup()
            self.discard()

    def init_new_game(self):
        self._game.new_game()
        # for player in self._game.player_seating:
        #     self._view.create_playerLayout(player)
        self._view.create_player_layout(self._game.player)
        self._view.state_new_game()

    def deal_cards(self):
        """Deal some cards."""
        self._game.dealing()
        self._view.state_dealing()
        self.update_display()
        self.update_player_hand()

    def update_player_hand(self):
        """Updates the player hand of cards."""
        self._view.update_player_hand(self._game.player.position, self._game.player.cards)

    def discard(self):
        """Ask the dealer to discard their extra card."""
        # ask the dealer to discard a card from their hand
        # if the player is a bot, bot handles discard
        # if player is human, signal discard response
        self._game.discard()

    def pickup(self):
        """Ask the dealer to pick up the trump card."""
        # Ask the player that is assigned dealer to pick up the card
        # move to the discard phase
        self._game.pickup()
        self.update_player_hand()

   # TODO refactor loop on player bidding to an each-player turn
   # TODO work on 2 round of bidding
    def bidding_round(self):
        """Starts a new bidding round for the trump card."""
        self._game.initialize_bidding()
        self._view.state_bidding()
        self.update_display()

        bid_round = self._game.bid_round
        
        for player in self._game.players:
            if player.is_bot():
                player.get_order(self._game.deck.revealed)
                bid_round.first_round(player, player.bid_order)
                self._game.bid_display()
                self.update_display()
                self.get_trump()
                if self._game.trump:
                    break
            else:
                self.bidding_requested.emit()
                self.get_trump()
        # if self._game.trump:
        #     self.pickup()

    def get_trump(self):
        self._game.get_trump()
        if self._game.trump:
            print("Trump has been set.")

    def bid_order(self, order):
        """Give the player order of trump to the game."""
        bid_round = self._game.bid_round
        self._game.player.get_order(order)
        bid_round.first_round(self._game.player, 
                              self._game.player.bid_order)
        self._game.bid_display()
        self.update_display()
        


    def update_display(self):
        """Update the display."""
        self._view.update_display_msg(self._game.display_msg)
        # self._view_update_player_turn(self._game.current_player_turn)
        # self._view_update_score(self._game.score)
