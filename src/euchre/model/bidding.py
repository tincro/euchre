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

    def bidding_round(self):
        """Start bidding round for trump card for this round. If revealed is None,
        Players can choose trump from their hand. Returns Trump object.

        Keyword arguments:
        players: -- list of players in this round of bidding.
        revealed: -- the revealed card to start the Trump bidding.
        first_round: -- if this is the first round of bidding. Defaults to true.
        """
        if self.face_up:
            self.first_round()
            if self.trump:
                self._dealer.pickup_and_discard(self.revealed)
        else:
            msg = f'The dealer {self._dealer} turned the {self.revealed} face-down. Starting second round of bidding...'
            print(msg)
            self.display_msg = msg
            self.second_round()
            
        return None
    
    def first_round(self, player, order):
        """Bid the first round for trump."""
        if order == 'order':
            self.maker = player
            self.trump = Trump(self.revealed.suit, self.maker.team)
            msg = f'Trump has been ordered: {self.revealed.suit} is now trump.'
            self.display_msg = msg
        elif order == 'pass':
            if self.trump:
                print(f'{player.name} has passed.')
                self.trump = None

        # for player in self._players:
        #         order = player.get_order(order)
        #         if order == 'order' or order == 'yes':
        #             self.trump = Trump(self.revealed.get_suit(), player.get_team())
        #             if player.is_bot():
        #                 player.going_alone(self.trump)
        #             else:
        #                 player.going_alone()
        #         elif order == 'pass':
        #             continue
        #         else:
        #             print('ERROR - NOT VALID OPTION.')

    def second_round(self):
        if not self.first_round:
            
            for player in self._players:
                call = player.get_call(self.revealed)
                if call == 'pass':
                    continue
                if call:
                    self.trump = Trump(call, player.get_team())
                    if player.is_bot():
                        player.going_alone(self.trump)
                    else:
                        player.going_alone()
        else:
            print("ERROR - NO PREVIOUS CARD REFERENCED.")