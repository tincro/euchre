"""Module to keep track of a round of playing cards."""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from euchre.model.cards import Card
    from euchre.model.players import Player

# TODO Need to make a play turn method for the players to take a turn to break loops.
class PlayRound():
    """Class to keep track of cards, players, and turns for this round of play."""
    def __init__(self, players, trump):
         self._players = players
         self._curr_player_turn = self._players[0]
         self._trump = trump
         self._cards_played = []
         self._leading_card = None
         self._winning_card = None
         self._display_msg = None

    @property
    def players(self):
        """Return list of players."""
        return self._players
    
    @property
    def trump(self):
        """Return current trump this round."""
        return self._trump
    
    @property
    def cards_played(self):
        """Return list of cards played this round."""
        return self._cards_played
    
    @cards_played.setter
    def cards_played(self, player_card: tuple[Player, Card]):
        """Add a card played this round to a list of cards played, along with the player."""
        self._cards_played.append(player_card)

    @property
    def current_player_turn(self):
        """Return current player's turn."""
        return self._curr_player_turn
    
    @property
    def leading_card(self):
        """Returns the leading (first) card played this round."""
        return self._leading_card
    
    @leading_card.setter
    def leading_card(self, card):
        """Set the leading card for the round."""
        self._leading_card = card
    
    @property
    def winning_card(self):
        """Returns the highest ranking card played this round."""
        return self._winning_card
    
    def get_player_card(self, player) -> Card:
        """Get a card from the player."""
        # TODO remove this (-1) when indexing fixed on player.list_cards method
        card_index = (player.get_player_card() - 1)
        return player.filtered_cards[card_index][1]
    
    def play_card(self, player, card):
        """Player will play a card for this round."""
        if not self.leading_card:
            self.leading_card = card
        self.cards_played = (player, card)
        player.remove_card(card)
        
        self.print_cards_played()


    # TODO Refactor this to break down the elements of the round.
    # TODO Enable one card played at a time, and evaluated.
    # def play_cards(self) -> list[tuple[Player, Card]]:
    #         """Each player plays a card from their hand. Returns tuple list of (player, card played).
            
    #         Keyword arguments:
    #         players: -- list of players.
    #         trump: -- trump for current round.
    #         """

    #         for player in self.players:
    #             # check if player gets skipped because partner alone this round
    #             if player.get_skipped():
    #                 continue
    #             # If a card has been played, we need to filter cards that are legal and
    #             # is matching the first card's suit in the list
    #             if len(self.cards_played) >= 1:
    #                 card_to_match = self.cards_played[0][1]
    #                 # Filter list of cards in player hand that is legal to play
    #                 # If filtered list returns empty, any card in hand is legal to play
    #                 legal_cards = player.list_cards(player.filter_cards(card_to_match, self.trump))
    #                 if len(legal_cards) == 0:
    #                     legal_cards = player.list_cards()
    #             else:
    #                 legal_cards = player.list_cards()
    #             player.get_player_status(legal_cards, self.trump)            

    #             # Subtract 1 from player choice to index properly
    #             # TODO Remove the ( - 1 ) since we won't be using console version anymore.
    #             card = (player.get_player_card(legal_cards) - 1)

    #             # Get the card from the tuple of the enumerated list
    #             card_to_play = legal_cards[card][1]

    #             print(f'{player.name} played {card_to_play}.')
    #             player.remove_card(card_to_play)
    #             self._cards_played.append((player, card_to_play))
    #             self.print_cards_played()

    def print_cards_played(self):
        print('All cards played:')
        for card in self.cards_played:
            print(f'\t{card[0]} played {card[1]}')
