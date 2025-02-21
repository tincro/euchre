"""Class to keep track of bidding round."""

from euchre.model.cards import Trump
from euchre.model.players import Player

class BiddingRound():
    def __init__(self, players, dealer, revealed=None):
        self._players = players
        self._dealer = dealer
        self._revealed = revealed
        self._face_up = True
        self._trump = None
        self._maker = None
        self._display_msg = f"Revealed card to bid for trump {self._revealed}"

    @property
    def revealed(self):
        """Returns the revealed card at the top of the deck."""
        return self._revealed
    
    @property
    def face_up(self):
        """Returns whether the revealed card is face up or not."""
        return self._face_up
    
    @property
    def trump(self):
        """Trump for this round."""
        return self._trump
    
    @trump.setter
    def trump(self, trump):
        """Set the trump for this bidding round."""
        self._trump = trump
    
    @property
    def maker(self):
        """Returns the Player that is the Maker of the trump for this round."""
        return self._maker
    @maker.setter
    def maker(self, maker):
        """Set the maker of trump this round."""
        self._maker = maker
    
    @property
    def display_msg(self):
        """Return the display message for this round."""
        return self._display_msg
    
    @display_msg.setter
    def display_msg(self, msg):
        """Set the display message."""
        self._display_msg = msg
    
    def first_round(self, player, order):
        """Bid the first round for trump.
        
        Keyword arguments:
        players: -- list of players in this round of bidding.
        revealed: -- the revealed card to start the Trump bidding.
        """
        if order == 'order':
            self.maker = player
            self.trump = Trump(self.revealed.suit, self.maker.team)
            msg = f'Trump has been ordered: {self.revealed.suit} is now trump.'
            self.display_msg = msg
        elif order == 'pass':
            if self.trump:
                print(f'{player.name} has passed.')
                self.trump = None

    def second_round(self, player):
        """Bid for the second round for trump."""
        msg = f'The dealer {self._dealer} turned the {self.revealed} face-down. Starting second round of bidding...'
        print(msg)
        self.display_msg = msg

        call = player.bid_call
        if not call == 'pass':
            self.trump = Trump(call, player.team)
        else:
            self.trump = None
            