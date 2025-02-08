"""
The card module takes care of the data surrounding anythin card related.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.trumps import Trump

from random import sample

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

    def __str__(self):
        """Return human friendly version of card."""
        return f'{self._rank} of {self._suit}'
    
    def __repr__(self):
        """Return card object."""
        return f'Card(\'{self._rank}\', \'{self._suit}\')'
     
     # Public methods      
    def is_trump(self, trump: Trump) -> bool:
        """Returns if the Card object is matching the current Trump.

        If True, a new value will be assigned to self._value. If Card object is considered
        to be the Left Bower, self._rank will be appended with '_L' suffix to increase
        the stength of the ranking when comparing cards.

        Keyword arguments:
        trump: -- the current trump object.
        """
        if self._suit == trump.get_suit():
            # Get the new value of the trump
            self._value = trump.RANK[self._rank]
            return True
            # Check for the other Jack of same color
        elif self._suit == trump.get_left() and self._rank == "Jack":
            # Subtract 1 to lower the strength for the left bower, adds suffix to rank for this effect
            self._value = trump.RANK[f'{self._rank}_L']
            return True
        return False            
            
    def get_value(self) -> int:
        """Return the numerical value of the card."""
        return self._value
    
    def get_suit(self) -> str:
        """Return the symbolic suit of the card."""
        return self._suit
   
    def get_rank(self) -> str|int:
        """Return the rank of the card, converted from number to face-card value."""
        return self._rank
    
    def get_color(self) -> str:
        """Return the color of the card."""
        return self._color
    
    def get_id(self) -> str:
        """Return the ID of the card."""
        return self._id
    
    def reset(self, value:int):
        """Reset the value if it is the initial value of the card."""
        if str(value) in self._id:
            self._value = value
    
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

    def shuffle(self) -> list[Card]:
        """Returns a shuffled list of cards."""
        return sample(self._cards, len(self._cards))
        