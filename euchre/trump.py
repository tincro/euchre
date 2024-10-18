"""The trump module keeps track of data relating to a trump.

Trump(): -- Base Trump class
"""

from card import Card

# Base Trump class, which is a special version of a card.
class Trump(Card):
    """Base Trump Class used to keep track of the Trump for the round.
    
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
        """Set the suit of the Trump object.
        Keyword arguments: 
        suit: -- the suit to set the current trump.
        """
        self._suit = suit

    def get_makers(self):
        """Return Team object that made Trump this round."""
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

    def print_trump(self):
        """Print the current Trump suit."""
        print('\n')
        print('-' * 40)
        print(f'\tCURRENT TRUMP IS: {self._suit}')
        print('-' * 40)
