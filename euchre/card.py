"""The card module takes care of the data surrounding anythin card related."""

# Base Card class
class Card():
    '''The base Card class. Modeled after a standard deck of playing cards.

    is_trump(): -- returns if the Card object is matching the suit of the current trump.
    get_value(): -- returns the value of the Card object.
    get_suit(): -- returns the suit of the Card object.
    get_rank(): -- returns the value of the Card object converted to the face card of the same value, i.e. 13 -> King.
    get_color(): -- returns the color of the Card object.
    '''
    def __init__(self, value=None, suit=None):
        """Initialize the card. Construct the value and suit from value and suit arguments respectively.
        _rank and _color are determined by argument assignments.
        """
        self._value = value
        self._suit = suit
        self._rank = self._convert(self._value)
        self._color = self._assign_color(self._suit)

    def __str__(self):
        """Return human friendly version of card."""
        return f'{self._rank} of {self._suit}'
    
    def __repr__(self):
        """Return card object."""
        return f'Card(\'{self._rank}\', \'{self._suit}\')'
    
    def _convert(self, value):
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
                
    def _assign_color(self, suit):
        """Get the color of the card suit.(i.e., "red", "black")"""
        if not suit:
            return
        if suit == "Diamonds" or "Hearts":
            return "red"
        elif suit == "Spades" or "Clubs":
            return "black"
        else:
            return "ERROR - NOT VALID SUIT."
        
    def is_trump(self, trump):
        """Returns if the Card object is matching the current Trump.

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
            
    def get_value(self):
        """Return the numerical value of the card."""
        return self._value
    
    def get_suit(self):
        """Return the symbolic suit of the card."""
        return self._suit
   
    def get_rank(self):
        """Return the rank of the card, converted from number to face-card value."""
        return self._rank
    
    def get_color(self):
        """Return the color of the card."""
        return self._color