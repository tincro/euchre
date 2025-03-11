"""Module for Euchre game controller."""

# TODO update the display for each player
# TODO polish to slow down timing
# TODO Need to correct the order of player turns, refactor here.
import sys

from PySide6.QtCore import Signal, Slot, QObject

from euchre.model.cards import Card

DELAY = True

class EuchreController(QObject):
    bidding_requested = Signal()
    calling_requested = Signal(str)
    discard_requested = Signal(Card)
    playing_requested = Signal(list, list)
    game_over_requested = Signal()
    
    def __init__(self, game, view):
        super().__init__()
        self._game = game
        self._view = view

        self.connect_signals()
        self.connect_views()
        
        self.main_menu()

    def connect_views(self):
        """Connect the view Signals to slots in this instance."""
        self._view.new_game_start_pressed.connect(self.new_game)
        self._view.user_quit_pressed.connect(self.quit_game)
        self._view.user_pass_pressed.connect(self.bid_order)
        self._view.user_order_pressed.connect(self.bid_order)
        self._view.user_call_pressed.connect(self.call_trump)
        self._view.user_play_pressed.connect(self.player_card)
        self._view.user_discard_pressed.connect(self.player_discard)
        self._view.user_game_over_pressed.connect(self.game_over_handle)

    def connect_signals(self):
        """Connect Signals from this instance to the view."""
        self.game_over_requested.connect(self._view.game_over_view)
        self.playing_requested.connect(self._view.user_playing_view)
        self.bidding_requested.connect(self._view.user_bidding_view)
        self.calling_requested.connect(self._view.user_calling_view)
        self.discard_requested.connect(self._view.user_discard_view)

    def main_menu(self):
        """Start on this menu."""
        self._view.state_main_menu()

    @Slot()
    def new_game(self):
        """Start new game of play."""
        self.init_new_game()
        while not self.game_over():
            # self.delay()
            self.deal_cards()

            self.init_bid_round()
            
            # self.delay()
            self.init_play_round()
            
            self.delay()
            self.score_round()
            self.check_for_winner()
            self.clean_up()

    @Slot()
    def player_discard(self, card):
        """Player discards this card."""
        # TODO refactor this when Dealer refactor.done == True
        self._game.dealer.player.remove_card(card)
        self.update_player_hand()

    @Slot()  
    def bid_order(self, order):
        """Check if the player wants to order the trump this round."""
        print(order)
        bid_round = self._game.bid_round
        self._game.player.get_order(order)
        bid_round.first_round(self._game.player, 
                              self._game.player.bid_order)
        self._game.bid_display()
        self.update_display()

    @Slot()
    def player_card(self, index):
        """Get the player card from the player."""
        round = self._game.play_round
        player = self._game.player
        card = self._game.player.get_player_card(index)
        round.play_card(player, card)
        self.update_player_hand()

    @Slot()
    def game_over_handle(self, answer):
        """Handler for the Game over screen."""
        if answer == "new game":
            self.new_game()
        elif answer == "quit":
            self.quit_game()
        else:
            print(f'UNKNOWN ANSWER FOR END GAME.')

    @Slot()
    def quit_game(self):
        """Exit the application."""
        sys.exit()

    @Slot()             
    def call_trump(self, trump):
        """Player calls trump."""
        bid_round = self._game.bid_round
        self._game.player.get_call(self._game.deck.revealed, trump)
        bid_round.second_round(self._game.player)

    def init_play_round(self):
        """Play round of cards."""
        round = 0
        while round < 5:
            self.play_cards()
            self.award_trick()
            self.update_turn_order()

            round += 1

    def init_bid_round(self):
        """Bid round loop."""

        self.bidding_round()
        if self.get_trump():
            self.pickup()
            self.discard()
        else:
            self.calling_round()
            if not self.get_trump():
                self.reset_round()

    def init_new_game(self):
        self._game.new_game()
        self._view.create_player_layout(self._game.player)
        self._view.create_bot_layout(self._game.bots)
        self._view.state_new_game()
        self.update_display()

    def deal_cards(self):
        """Deal some cards."""
        self._game.dealing()
        self._view.state_dealing(self._game.display_msg)
        self.update_player_hand()
        self.update_display()

    def update_player_hand(self):
        """Updates the player hand of cards in the player view."""
        self._view.update_player_hand(self._game.player.cards)

    def disable_player_hand(self):
        """Disable player hand in the view."""
        self._view.disable_player_hand(self._game.player.position)

    def discard(self):
        """Ask the dealer to discard their extra card."""
        self._game.discard()
        # if player is human, signal discard response
        if not self._game.dealer.is_bot():
            self.discard_requested.emit(self._game.dealer.player.cards)

        self.update_display()  

    def pickup(self):
        """Ask the dealer to pick up the trump card."""
        # Ask the player that is assigned dealer to pick up the card
        # move to the discard phase
        self._game.pickup()
        self.update_player_hand()
        self.update_display()

   # TODO refactor loop on player bidding to an each-player turn
    def bidding_round(self):
        """Starts a new bidding round for the trump card."""
        self._game.initialize_bidding()
        self._view.state_bidding()
        self.update_display()

        bid_round = self._game.bid_round
        
        for player in self._game.players:
            self.delay()
            if player.is_bot():
                player.get_order(self._game.deck.revealed)
                bid_round.first_round(player, player.bid_order)
                self._game.bid_display()
                self.update_display()
                if self.get_trump():
                    self.going_alone(player)
                    break
            else:
                self.bidding_requested.emit()
  
    def calling_round(self):
        """Second round of bidding."""
        bid_round = self._game.bid_round
        bid_round.msg_second_start()
        revealed = self._game.deck.revealed

        for player in self._game.players:
            if player.is_bot():
                player.get_call(revealed)
                bid_round.second_round(player)
                self._game.bid_display()
                self.update_display()
                if self.get_trump():
                    self.going_alone(player)
                    break
            else:
                self.calling_requested.emit(revealed.suit)
                # self.get_trump()
                # self._game.bid_display()
                # self.update_display()
            if self.get_trump():
                self.going_alone(player)
                break

        if not self.get_trump():
            bid_round.msg_second_end()
            self._game.bid_display()
            self.update_display()

    def get_trump(self):
        """Update current Trump status."""
        return self._game.get_trump()
 
    def going_alone(self, player):
        """Check the going alone status of player."""
        self._game.going_alone(player)

    def play_cards(self):
        """Play round of cards from each player."""
        # TODO make sure round resets after all cards played
        self._game.init_playing()

        for player in self._game.players:
            if player.get_skipped():
                print(f'{player} is skipped this round.')
                continue

            self.filter_player_cards(player)
            
            if player.is_bot():
                self.bot_play_card(player)
            else:
                index = self.index_from_player(player)
                self.playing_requested.emit(index, player.cards)
                       
    def filter_player_cards(self, player) -> None:
        """Filter the player cards if there is a leading cards already played this round."""
        if not self.get_lead_card():
            # print('NO LEAD CARD')
            player.list_cards()
        else:
            # print("LEAD")
            # print(self.get_lead_card())
            # print("TRUMP")
            # print(self.get_trump())
            player.list_cards(self.get_lead_card(), self.get_trump())
            
    def get_lead_card(self):
        """Get the leading card this round."""
        return self._game.play_round.leading_card
  
    def bot_play_card(self, player):
        """Play the card from the bot."""
        round = self._game.play_round

        card = round.get_player_card(player)
        round.play_card(player, card)

    def award_trick(self):
        """Score the trick this round of cards played and award the highest value card to the player."""
        self._game.award_trick()

    def index_from_player(self, player):
        """Get the list from the player"""
        return player.filtered_index_list()

    def update_turn_order(self):
        """Update the turn order."""
        self._game.update_turn_order()

    def update_display(self):
        """Update the display."""
        self._view.update_display_msg(self._game.display_msg)
        # self._view_update_player_turn(self._game.current_player_turn)
        # self._view_update_score(self._game.score)

    def score_round(self):
        """Score the current round."""
        self._game.scoring()

    def check_for_winner(self):
        """Check if there is a winner."""
        self._game.check_for_winner()

    def clean_up(self):
        """Clean up anything before starting a new round."""
        self._game.clean_up()
    
    def game_over(self):
        """Check if game over."""
        game_over = self._game.game_over

        if game_over:
            self.game_over_requested.emit()

        return game_over
       
    def reset_round(self):
        """Reset the round."""
        self._game.reset_round()

    def delay(self):
        """Time delay for better pacing."""
        if DELAY:
            self._game.delay()