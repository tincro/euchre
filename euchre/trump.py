"""The Trump class keeps track of information regarding a special version of a Card.

A Trump is the highest ranking cards in the game of Euchre, and depending on the value it is handled differently.
"""

class Trump():
    # Unique ranking for the game of Euchre, with Jack being the highest.
    # Second index in tuple is the new value for the card
    RANK = {
        "Jack": (1, 20),
        "Ace": (2, 19),
        "King": (3, 18),
        "Queen": (4, 17),
        "10": (5, 16),
        "9": (6, 15),
    }
    
    def __init__(self, suit=None):
        """Initialize the Trump object."""
        self._suit = suit

    def __str__(self):
        """Return human-friendly version of Trump object."""
        return f'The current trump is {self._suit}.'
    
    def __repr__(self):
        """Return Trump object."""
        return f'Trump(\'{self._suit}\')'

    def get_suit(self):
        """Return the current suit of the Trump object."""
        return self._suit        
    
    def set_suit(self, suit):
        """Set the suit of the Trump object."""
        self._suit = suit

    def reset(self):
        """Reset the suit of the Trump object."""
        self._suit = None