"""The Trump class keeps track of information regarding a special version of a Card.

A Trump is the highest ranking cards in the game of Euchre, and depending on the value it is handled differently.
"""

class Trump():
    # Unique ranking for the game of Euchre, with Jack being the highest.
    RANK = {
        "Jack": 1,
        "Ace": 2,
        "King": 3,
        "Queen": 4,
        "10": 5,
        "9": 6
    }
    
    def __init__(self, suit=None):
        self._suit = suit

    def __str__(self):
        return f'The current trump is {self._suit}.'
    
    def __repr__(self):
        return f'Trump(\'{self._suit}\')'

    def get_suit(self):
        return self._suit        
    
    def set_suit(self, suit):
        self._suit = suit

    def reset(self):
        self._suit = None