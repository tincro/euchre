"""
The card module takes care of the data surrounding anythin card related.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from euchre.trumps import Trump
    from euchre.players import Player

from colorama import just_fix_windows_console, Fore, Style
just_fix_windows_console()

# The base Card class
class Card():
    '''The base Card class. Modeled after a standard deck of playing cards.

    is_trump(): -- returns if the Card object is matching the suit of the current trump.
    get_value(): -- returns the value of the Card object.
    get_suit(): -- returns the suit of the Card object.
    get_rank(): -- returns the value of the Card object converted to the face card of the same value, i.e. 13 -> King.
    get_color(): -- returns the color of the Card object.
    '''
    SYMBOLS = {
            "Diamonds": "♦",
            "Spades": "♠",
            "Clubs": "♣",
            "Hearts": "♥"
        }
    
    def __init__(self, value: int=None, suit: str=None):
        """Initialize the card. Construct the value and suit from value and suit arguments respectively.
        _rank and _color are determined by argument assignments.
        """
        self._value = value
        self._suit = suit
        self._rank = self._convert(self._value)
        self._color = self._assign_color(self._suit)
        self._id = f'{self._rank}{self._suit}_{self._value}{self._color}'
        self._symbol = self._assign_symbol(self._suit)

    def __gt__(self, other):
        return self.get_value() > other.get_value()
    
    def __ge__(self, other):
        return self.get_value() >= other.get_value()
    
    def __lt__(self, other):
        """Necessary for sorting purposes."""
        return self.get_value() < other.get_value()
    
    def __le__(self, other):
        return self.get_value() <= other.get_value()

    def __str__(self):
        """Return human friendly version of card."""
        if type(self._rank) == str:
            # assign color with colorama, print text of card, reset colors
            return f'{self._color}{self._rank[0]}{self._symbol}{Style.RESET_ALL}'
        else:
            return f'{self._color}{self._rank}{self._symbol}{Style.RESET_ALL}'
    
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
            return True
        elif self._suit == trump.get_left() and self._rank == "Jack":
            return True
        return False

    def update_to_trump(self, trump):
        """Update this card's value with the new trump ranking value."""
        if self._suit == trump.get_suit():
            # Get the new value of the trump
            self._value = trump.RANK[self._rank]
            # Check for the other Jack of same color
        elif self._suit == trump.get_left() and self._rank == "Jack":
            # Subtract 1 to lower the strength for the left bower, adds suffix to rank for this effect
            self._value = trump.RANK[f'{self._rank}_L']
            
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
        
        try:
            if suit == "Diamonds" or suit == "Hearts":
                return Fore.RED
            elif suit == "Spades" or suit == "Clubs":
                return Fore.BLUE
            else:
                raise ValueError("Not Valid Suit Value")
        except ValueError as e:
            print(e)
    
    def _assign_symbol(self, suit: str):
        """Get the symbol associated with the suit."""
        return Card.SYMBOLS[suit]
    

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

        # Check if the card is trump suit, update if true
        if card.is_trump(trump):
            card.update_to_trump(trump)

        if card == first_card:
            continue

        # Only compare cards that have the matching value or have a trump suit
        if card.get_suit() == first_card.get_suit() or card.is_trump(trump):

            if card.get_value() > highest_card.get_value():
                highest_card = card
                winning_card = this_card

    return winning_card
        