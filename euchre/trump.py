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
    
    def __init__(self, suit=None, makers=None):
        """Initialize the Trump object."""
        super().__init__()
        self._suit = suit
        self._makers = makers
        self._left = None

    def __str__(self):
        """Return human-friendly version of Trump object."""
        return f'The current trump is {self._suit}.'
    
    def __repr__(self):
        """Return Trump object."""
        return f'Trump(\'{self._suit}\')'
    
    def set_suit(self, suit):
        """Set the suit of the Trump object."""
        self._suit = suit

    def get_makers(self):
        """Return Team that made Trump this round."""
        return self._makers
    
    def get_left(self):
        """Return Left Bower card for Trump this round."""
        return self._left
    
    def _find_left(self):
        """Find the left bower and assign it."""
        pass

    def reset(self):
        """Reset the suit of the Trump object."""
        self._color = None
        self._suit = None
        self._makers = None
        self._left = None