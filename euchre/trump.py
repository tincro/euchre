"""The Trump class keeps track of information regarding a special version of a Card.

A Trump is the highest ranking cards in the game of Euchre, and depending on the value it is handled differently.
"""

from card import Card

class Trump(Card): 
    # Unique ranking for the game of Euchre, with Jack being the highest.
    # Since both Jacks of the same color are Trump, we leave room for it (20).
    RANK = {
        "Jack": 21,
        "Ace": 19,
        "King": 18,
        "Queen": 17,
        10: 16,
        9: 15,
    }
    
    def __init__(self, suit=None):
        """Initialize the Trump object."""
        super().__init__()
        self._suit = suit

    def __str__(self):
        """Return human-friendly version of Trump object."""
        return f'The current trump is {self._suit}.'
    
    def __repr__(self):
        """Return Trump object."""
        return f'Trump(\'{self._suit}\')'
    
    def set_suit(self, suit):
        """Set the suit of the Trump object."""
        self._suit = suit

    def reset(self):
        """Reset the suit of the Trump object."""
        self._color = None
        self._suit = None