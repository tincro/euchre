class Trump():
    """Trump class is information regarding highest ranking Card in Euchre.
    There will always only be one suit of Trump at a time.
    """
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
        if self._suit is not None:
            return self._suit
        else:
            return "No suit has been currently chosen for the trump."
    
    def set_suit(self, suit):
        self._suit = suit

    def reset(self):
        self._suit = None