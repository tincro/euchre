"""
Dealer module is used to deal cards to players, pick up card, and track player order positions.
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
    pickup_and_discard(card): Pick up the Card and choose a card to discard.
    set_leader(player): set the leader player for the round.
    """

    def __init__(self, player_list: list[Player]):
        self._dealer_list = deque(player_list)
        self._player_order = deque(self._dealer_list)
        self._dealer_player = self._player_order[0]
        self._next_dealer = self._get_next_dealer()

        # offset player order so dealer is last in the player order
        self._set_dealer()

    def __str__(self):
        """Print human-friendly version of Dealer."""
        return f'Dealer {self._dealer_player}'
    
    def __repr__(self):
        """Print Dealer Object."""
        return f'Dealer(\'{self._dealer_player}\')'
    
    def get_player_order(self) -> list[Player]:
        """Return player order."""
        return self._player_order

    def deal_cards(self) -> Card:
        """Shuffle the deck and deal cards to players in two rounds. Returns the top 
        card left in the remaining deck of cards.

        Keyword arguments:
        players: -- list of players for whom the cards are dealt.
        deck: -- list of cards to deal.
        """
        print('\n')
        print(f'{self._dealer_player} is dealing cards...')
        shuffled = sample(DECK, len(DECK))
        rounds = 0
        cards_to_deal = 3
        
        while rounds < 2:
            for player in self._player_order:
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
        # Get this dealer and find the next dealer then set the round of players.
        self._dealer_player = self._next_dealer
        this_dealer = self._dealer_list.popleft()
        self._dealer_list.append(this_dealer)
        self._next_dealer = self._get_next_dealer()
        self._set_dealer()

    def pickup_and_discard(self, card):
        """
        Add card to dealer hand and prompt them to discard.

        Keyword arguments:
        card: -- Card object the Dealer is to pick up.
        """
        self._pickup_card(card)
        self._discard_card()

    def set_leader(self, leader: Player):
        """Get the leader player and make sure they are first in the order of play.

        Keyword arguments:
        leader: -- The new Player to be first in the round of play.
        """
        while self._player_order[0] != leader:
            self._get_new_order()

    def _pickup_card(self, card: Card):
        """Dealer player picks up top card if player has ordered Trump."""
        self._dealer_player.receive_card(card)
        print(f'{self._dealer_player} picked up {card}.')

    def _discard_card(self):
        """Dealer discards Card they do not want."""
        dealer = self._dealer_player

        player_cards = dealer.list_cards()
        dealer.get_player_status(player_cards)            

        # Subtract 1 from player choice to index properly
        discard = (dealer.get_player_card(player_cards) - 1)
        # card_hand = player_cards
        # Get the card from the tuple of the enumerated list
        card_to_discard = player_cards[discard][1]

        print(f'{dealer.get_name()} discarded {card_to_discard}.')
        dealer.remove_card(card_to_discard)

    def _get_next_dealer(self) -> Player:
        """Get next dealer in player order"""
        return self._dealer_list[1]
    
    def _get_new_order(self):
        """Move the first player in the list to the end of the list."""
        first = self._player_order.popleft()
        self._player_order.append(first)

    def _set_dealer(self):
        """Get the leader player and make sure they are first in the order of play."""
        while self._player_order[-1] != self._dealer_player:
            self._get_new_order()
