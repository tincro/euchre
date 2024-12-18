"""Module for holding the logic for the computer bot players.


"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from euchre.cards import Card
    from euchre.teams import Team
    from euchre.trumps import Trump

from euchre.players import Player

# The base Bot class
class Bot(Player):
    """The base class for the computer bot Players.
    
    The bot players are activated when there are less than 4 human players.
    They have the same functionality for the player, with the exception that 
    the bot can play the hands for the non-human players in the game. There
    can be as many bot players as necessary.

    TODO: May need to rewrite some functions for the bot to play the game
    - bot needs to know if it should order the trump or pass
    - if second round of bidding, bot should decide to order any of the trump or pass
    - if bot orders trump, is he going alone?
    - if bot is ordered up trump and is the dealer, bot needs to choose a card to discard that is not trump
    - bot needs to play a card from hand
    - when playing a card, the bot must play the best card, if he can catch the trick he will play the best card to do so
    - if bot is leading the hand, he will play the highest card in hand

    is_bot(): -- returns status if player is a bot.
    get_player_card(): -- bot evaluates and plays a card from hand.
    going_alone(): -- bot decideds if it will go alone in a hand.
    """
    def __init__(self, name: str):
        """Initialize bot player object. Anything player related should be 
        inherited by the player object that this object is taking place of as they
        should be created first.
        """
        super().__init__(self, name)
        self._is_bot = True

    def __repr__(self):
        """Return the bot object."""
        return f'Bot player(\'{self._name}\')'

    # public methods
    def is_bot(self):
        """Returns if is a bot."""
        return self._is_bot
    
    def get_player_card(self, legal_card_list: list[Card]) -> int:
        """Bot evaluates and plays a card from hand. Returns card number to play.
        
        Keyword arguments:
        legal_card_list: -- List of cards able to be played this round.
        """
        if not legal_card_list:
            return
        
        card = self._choose_card(legal_card_list)
        return card
    
    def going_alone(self, trump: Trump) -> bool:
        """Check if bot wants to go alone this round.
        """
        hand_strength = 0
        alone_value = 60

        for card in self._cards:
            if card.get_suit() == trump.get_suit():
                hand_strength += card.get_value()

        if hand_strength >= alone_value:
            self.set_alone(True)
            partner = self._get_partner()
            self._set_partner_skipped(partner)
            return True
        self.set_alone(False)
        return False

    # private methods
    def _choose_card(self, card_list: list[tuple [int, Card]]) -> int:
        """Evaluates all the cards, and chooses the highest value card in the list. 
        Returns integer of that card.

        Keyword arguments:
        card_list: -- List of cards able to be played this round.
        """
        print('BOT PLAYER CHOOSING CARD...')
        highest_card = card_list[0][1]
        highest_card_index = card_list[0][0]
        for card in card_list:
            if card[1].get_value() > highest_card.get_value():
                highest_card_index = card[0]

        return highest_card_index


# Bot player builder
def build_bots(names: list[Player]) -> list[Bot]:
    """Create Bot player objects based on list of Player objects."""
    if not names:
        print("WARNING: NO NAMES OF PLAYER OBJECTS TO CREATE BOTS. EXITING BUILDER.")
        return
    
    bots = [Bot() for name in names]
    return bots