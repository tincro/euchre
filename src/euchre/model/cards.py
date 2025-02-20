"""
The card module takes care of the data surrounding anythin card related.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from euchre.model.cards import Trump
    from euchre.model.players import Player

from random import sample

# TODO refactor trump values to Trump class, replacing the cards for more simplicity
# TODO check if suit is same as trump, refactor to take trump as arg instead 

# The base Card class
class Card():
    '''The base Card class. Modeled after a standard deck of playing cards.

    is_trump(): -- returns if the Card object is matching the suit of the current trump.
    get_value(): -- returns the value of the Card object.
    get_suit(): -- returns the suit of the Card object.
    get_rank(): -- returns the value of the Card object converted to the face card of the same value, i.e. 13 -> King.
    get_color(): -- returns the color of the Card object.
    '''
    VALUES = (9, 10, 11, 12, 13, 14)
    SUITS = ("Spades", "Diamonds", "Clubs", "Hearts")

    def __init__(self, value=None, suit=None):
        """Initialize the card. Construct the value and suit from value and suit arguments respectively.
        _rank and _color are determined by argument assignments.
        """
        self._value = value
        self._suit = suit
        self._rank = self._convert(self._value)
        self._color = self._assign_color(self._suit)
        self._id = f'{self._rank}{self._suit}_{self._value}{self._color}'
        self._is_trump = False
        self._name = f"{self._rank} of {self._suit}"

    def __str__(self):
        """Return human friendly version of card."""
        return f'{self._rank} of {self._suit}'
    
    def __repr__(self):
        """Return card object."""
        return f'Card(\'{self._rank}\', \'{self._suit}\')'
    
    # Properties
    @property
    def name(self) -> str:
        """Return the name of the card."""
        return self._name
    
    @property    
    def value(self) -> int:
        """Return the numerical value of the card."""
        return self._value
    
    @value.setter
    def value(self, value):
        """Set the value. Usually if this is a trump card."""
        self._value = value

    @property
    def suit(self) -> str:
        """Return the symbolic suit of the card."""
        return self._suit
    
    @suit.setter
    def suit(self, suit):
        """Set the suit. Usually if this card is a trump card."""
        self._suit = suit
   
    @property
    def rank(self) -> str|int:
        """Return the rank of the card, converted from number to face-card value."""
        return self._rank
    
    @property
    def color(self) -> str:
        """Return the color of the card."""
        return self._color
    
    @property
    def id(self) -> str:
        """Return the ID of the card."""
        return self._id
    
    @property
    def trump(self):
        """Return if this card is a trump card."""
        return self._is_trump
    
    # Public methods      
    def reset(self, value:int):
        """Reset the value if it is the initial value of the card."""
        if str(value) in self._id:
            self._value = value
    
    def is_trump(self, trump: Trump) -> bool:
        """Returns if the Card object is matching suit to the current Trump or if this card is the Left Bower.

        If True, a new value will be assigned to self._value, else returns False.

        Keyword arguments:
        trump: -- the current trump object.
        """
        if self._suit == trump.suit:
            # Get the new value of the trump
            self._value = trump.RANK[self._rank]
            self._is_trump = True
            # Check for the other Jack of same color
        elif self._suit == trump.left and self._rank == "Jack":
            # Subtract 1 to lower the strength for the left bower, adds suffix to rank for this effect
            self.value = trump.RANK[f'{self._rank}_L']
            self._is_trump = True
        return self.trump
    
    # Private methods
    def _convert(self, value: int) -> str|int:
        """Convert numeral cards to string based familiar names 
        (i.e., 11 -> "Jack", 12 -> "Queen", etc.).
        """
        match value:
            case 11:
                return "Jack"
            case 12:
                return "Queen"
            case 13:
                return "King"
            case 14:
                return "Ace"
            case _:
                if value == 9 or value == 10:
                    return value
                else:
                    return "ERROR - NOT VALID CARD VALUE. REMOVE FROM DECK."                
    
    def _assign_color(self, suit: str):
        """Get the color of the card suit.(i.e., "red", "black")"""
        if not suit:
            return
        if suit == "Diamonds" or "Hearts":
            return "red"
        elif suit == "Spades" or "Clubs":
            return "black"
        else:
            return "ERROR - NOT VALID SUIT."


class Deck():
    """Class of a deck of Euchre cards."""
    def __init__(self):
        self._cards = [Card(value, suit) for value in Card.VALUES for suit in Card.SUITS]
        self._revealed = None

    @property
    def revealed(self):
        """Return the revealed top card of the deck, if there is one."""
        return self._revealed
    
    @revealed.setter
    def revealed(self, card):
        """Set the revealed top card."""
        if isinstance(card, Card) or card is None:
            self._revealed = card

    def shuffle(self) -> list[Card]:
        """Returns a shuffled list of cards. Original list of cards remains unchanged."""
        return sample(self._cards, len(self._cards))
    
    def collect(self):
        """Cleanup at the end of a round."""
        self.revealed = None
    

class Trump(Card):
    """Base Trump Class used to keep track of the Trump for the round. Basically it is super card.
    
    set_suit(): -- set the suit of the Trump object.
    get_makers(): -- return the Team object that chose Trump for the round.
    get_left(): -- return the left bower Card Object for Trump this round.
    reset(): -- reset the Trump for this round. Not normally used.
    print_trump(): -- Print the Trump for the round.
    """ 
    # Unique ranking for the game of Euchre, with Jack being the highest.
    # Since both Jacks of the same color are Trump, we leave room for it (20).
    RANK = {
        "Jack": 21,
        "Jack_L": 20,
        "Ace": 19,
        "King": 18,
        "Queen": 17,
        10: 16,
        9: 15,
    }
    
    def __init__(self, suit, makers=None):
        """Initialize the Trump object."""
        super().__init__(suit=suit)
        self._suit = suit
        self._makers = makers
        self._left = self._find_left(self._suit)

    def __str__(self):
        """Return human-friendly version of Trump object."""
        return f'The current trump is {self._suit}.'
    
    def __repr__(self):
        """Return Trump object."""
        return f'Trump(\'{self._suit}\')'
    
    # Properties
    @property
    def makers(self):
        """Return Team object that made Trump this round."""
        return self._makers
    
    @property
    def left(self):
        """Return Left Bower card for Trump this round."""
        return self._left

    @property
    def suit(self):
        """Return the current suit."""
        return self._suit
    
    @suit.setter
    def suit(self, suit):
        """Set the suit of the Trump object.
        Keyword arguments: 
        suit: -- the suit to set the current trump.
        """
        if suit in Trump.SUITS:
            self._suit = suit   

    # Public methods
    def reset(self):
        """Reset the suit of the Trump object."""
        self._color = None
        self._suit = None
        self._makers = None
        self._left = None

    def print_trump(self):
        """Print the current Trump suit."""
        print('\n')
        print('-' * 40)
        print(f'\tCURRENT TRUMP IS: {self._suit}')
        print('-' * 40)

    def print_makers(self):
        """Print the makers for the current Trump."""
        print(f'Ordered by {self._makers}.')

    # Private methods
    def _find_left(self, suit):
        """Find the left bower suit and return it.
        
        Keyword arguments:
        suit: -- The suit for which to find the opposite suit.
        """
        left = {
            "Spades": "Clubs",
            "Diamonds": "Hearts",
            "Clubs": "Spades",
            "Hearts": "Diamonds"
        }
        return left[suit]
        
def get_highest_rank_card(cards: list[tuple[Player, Card]], trump: Trump) -> tuple[Player, Card]:
    """Return the highest ranking Card object in the card list by value. Returns as tuple (player, card).
    
    cards: -- list of tuples of (player, card).
    trump: -- current round Trump object.
    """
    if not cards or not trump:
        print("ERROR - MISSING CARD OR TRUMP.")
        return
    # intitialize with first card in tuple list (player, card)
    first_card = cards[0][1]
    
    highest_card = first_card
    winning_card = cards[0]
    
    for this_card in cards:
        card = this_card[1]
        if card == highest_card:
            # Check for Trump on first card to assign correct value
            card.is_trump(trump)
            continue

        if card.is_trump(trump):
            if card.get_value() > highest_card.get_value():
                highest_card = card
                winning_card = this_card

        # Filter out cards that don't match the leading card suit
        elif card.get_suit == first_card.get_suit() and card.get_value() > highest_card.get_value():
            highest_card = card
            winning_card = this_card

    return winning_card
        