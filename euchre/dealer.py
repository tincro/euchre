"""
Dealer module is used to deal cards to players, pick up card, and track player positions.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from card import Card
    from player import Player

from collections import deque
from random import sample

from constants import DECK

class Dealer():
    """
    Keeps track of player positions for dealing cards and playing cards each round.

    get_player_order(): Returns player order.
    deal_cards(): Deal 5 Cards to each player in player order.
    next_dealer(): Get the next Player object in player order and assign as dealer.
    """

    def __init__(self, player_list: list[Player]):
        self._player_list = player_list
        self._player_round = deque(self._player_list)
        self._dealer_player = self._player_round[0]
        self._next_player = self._get_next_player()

    def get_player_order(self) -> list[Player]:
        """Return player order."""
        return self._player_round

    def deal_cards(self) -> Card:
        """Shuffle the deck and deal cards to players in two rounds. Returns the top 
        card left in the remaining deck of cards.

        Keyword arguments:
        players: -- list of players for whom the cards are dealt.
        deck: -- list of cards to deal.
        """
        print('\n')
        print("Dealing Cards...")
        shuffled = sample(DECK, len(DECK))
        rounds = 0
        cards_to_deal = 3
        
        while rounds < 2:
            for player in self._player_round:
                cards_dealt = shuffled[0:cards_to_deal]
                
                for card in cards_dealt:
                    shuffled.remove(card)
                    player.receive_card(card)
                        
            rounds += 1
            cards_to_deal -= 1

        revealed = shuffled[0]
        print(f'Revealed card to bid for trump: {revealed}')
        return revealed
         
    def next_dealer(self):
        """Pass to the next dealer in player order."""
        print(f'Passing dealer...')
        self._dealer_player = self._next_player
        self._get_new_order()
        self._next_player = self._get_next_player()

    def _get_next_player(self) -> Player:
        """Get next player in player list and return it."""     
        return self._player_round[1]
    
    def _get_new_order(self):
        """Move the first player in the list to the end of the list."""
        first = self._player_round.popleft()
        self._player_round.append(first)
