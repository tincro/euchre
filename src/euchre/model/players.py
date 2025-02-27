"""The Player class keeps track of the data surrounding a player.

Player(): -- The base Player class.
build_players(): -- build each player object.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from euchre.view.interface import MainInterface
    from euchre.model.teams import Team
    from euchre.model.cards import Trump

from euchre.model.cards import Card

# The base Player class
class Player():
    """The base class for Player objects.

    get_name(): -- returns the name of the Player.
    get_team(): -- returns the team object this Player is assigned.
    set_team(): -- assign the Player to the Team object.
    receive_card(): -- add the card object to the Player's hand of cards.
    remove_card(): -- remove the card from hand.
    get_cards(): -- returns the list of  cards in the Player's hand.
    list_cards(): -- returns enumerated list of cards.
    filter_cards(): -- filters cards that are legal to play for the hand.
    get_call(): -- get trump call from player after second round of bidding.
    get_order(): -- get order to pick up revealed card to be trump in first round of bidding.
    get_player_card(): -- get input from player to choose a card in hand.
    get_player_status(): -- print player name and each card in hand.
    get_tricks(): -- return the tricks won for the round.
    set_tricks(): -- set the trick count increasing by one.
    is_alone(): -- returns status if Player is going alone this round.
    is_bot(): -- returns status if Player is a bot.
    set_alone(): -- set the alone status for the Player.
    going_alone(): -- check if the player is going alone without a partner this round.
    reset(): -- reset the counters for the round.
    """
    # count of Player instances
    count = 0
    h_count = 0

    def __init__(self, name: str):
        """Initialize player object. Player name assigned via argument name.
        _cards and _team are assigned external of initialization.
        """
        Player.count += 1
        
        self._name = name
        self._cards = []
        self._filtered_cards = None
        self._team = None
        self._tricks = 0
        self._is_alone = False
        self._is_skipped = False
        self._is_bot = False
        self._selected = None
        self._order = None
        self._position = Player.count - 1
        self._bid_order = None
        self._bid_call = None
        
    
    def __str__(self):
        """Return human-friendly version of player."""
        return f'{self._name}'
    
    def __repr__(self):
        """Return the player object."""
        return f'Player(\'{self._name}\')'

    # Public methods
    @property
    def name(self) -> str:
        """Return the player's name."""
        return self._name
    
    @property
    def cards(self) -> list[Card]:
        """Returns the list of cards in players hand. Cards are not listed."""
        return self._cards
    
    @property
    def filtered_cards(self):
        """Return enumerated filtered list of cards."""
        return self._filtered_cards
    
    @filtered_cards.setter
    def filtered_cards(self, enum_cards_list):
        """Set the cards as an enumerated filtered list."""
        self._filtered_cards = enum_cards_list

    @property
    def team(self) -> Team:
        """Return the team object the player is assigned."""
        return self._team
    
    @team.setter
    def team(self, team: Team):
        """Assign the player to a team."""
        if self._team == None:
            self._team = team

    @property
    def position(self):
        """Return the seating position of this player for display purposes."""
        return self._position
    
    @property
    def bid_order(self):
        """Return player bid order."""
        return self._bid_order
    
    @bid_order.setter
    def bid_order(self, order):
        self._bid_order = order
    
    @property
    def bid_call(self):
        """Return call bid of the player."""
        return self._bid_call
    
    @bid_call.setter
    def bid_call(self, call):
        """Set the call bid for this player."""
        if call in Card.SUITS or call == 'pass':
            self._bid_call = call

    def receive_card(self, card: Card):
        """Add the received card to the players hand of cards."""
        self._cards.append(card)
    
    def remove_card(self, card: Card):
        """Remove the Card object from the Player hand."""
        if card in self._cards:
            self._cards.remove(card)
    
    # def list_cards(self, cards: list[Card]=None) -> list[tuple [int, Card]]:
    #     """Returns enumerated list of cards currently in hand. If no cards list passed, all cards returned.
        
    #     Keyword arguments:
    #     cards: -- list of cards to enumerate.
    #     """
    #     # Start enumeration at 1 for player input simplicity.
    #     # If no list is provided, just return all the cards in hand instead.
    #     if cards:
    #         return list(enumerate(cards, start=1))
    #     return list(enumerate(self._cards, start=1))
    
    def list_cards(self, filter=None, trump=None) -> None:
        """Returns enumerated list of cards currently in hand. If no cards list passed, all cards returned.
        
        Keyword arguments:
        cards: -- list of cards to enumerate.
        """
        # Start enumeration at 1 for player input simplicity.
        # If no filter and trump is provided, just return all the cards in hand instead.
        if filter and trump:
            cards = self.filter_cards(filter, trump)
            self._filtered_cards = list(enumerate(cards, start=1))
            # TODO Remove the start since we won't be using the console anymore.
            # return list(enumerate(cards, start=1))
        self.filtered_cards = list(enumerate(self.cards, start=1))
        # return list(enumerate(self.cards, start=1))
    
    def filter_cards(self, card_to_match: Card, trump: Trump):
        """Filters the list of cards in player's hand for legal cards and returns it.
            
        card_to_match: -- card to compare suits against to filter.
        trump: -- the curren trump for the round.
        """
        # If Left Bower played first we need to filter for trump suits instead
        if card_to_match.is_trump(trump):
            suit_to_match = trump.suit
        else:
            suit_to_match = card_to_match.suit

        legal_list = []

        for card in self.cards:
            suit = card.suit
            # TODO Refactor this to simplify
            # Special case for Left Bower played later in round, and shares suit with lead card.
            if suit == suit_to_match and not card_to_match.is_trump(trump) and card.is_trump(trump):
                continue
            # Otherwise follow normal filtering
            elif suit == suit_to_match:
                legal_list.append(card)
            # If trump was lead we need to get the left bower in the filter.
            if suit_to_match == trump.suit:
                if card.rank == "Jack" and suit == trump.left:
                    legal_list.append(card)

        return legal_list
    
    def get_call(self, previous_revealed: Card, call) -> str:
        """Get call from the player. Only acceptable options are 'Hearts', 'Spades', 'Diamonds', or 'Clubs'.
        Player cannot chose the trump that was already bidded.

        Keyword arguments:
        previous_revealed: -- Revealed card from the top of deck.
        """
        suit = previous_revealed.suit.lower()
        call_or_pass = call[0]
        is_alone = call[1]

        if call_or_pass.lower() == 'pass':
            self.bid_call = call_or_pass.lower()
            self.set_alone(False)
        elif call_or_pass.lower() != suit:
            if call_or_pass.capitalize() in Card.SUITS:
                self.bid_call = call_or_pass.capitalize()
                self.set_alone(is_alone)
            else:
                self.bid_call = None
        else:
            print(f"CANNOT CHOOSE THAT SUIT: {previous_revealed.suit}")

    def get_order(self, order_tup:tuple[str,bool]=None ) -> str:
        """Get order from the player. Only acceptable options are 'order' or 'pass'.

        Keyword arguments:
        revealed: -- Revealed card from the top of deck.
        """
        order = order_tup[0]
        is_alone = order_tup[1]
        if order.lower() == 'pass':
            self.bid_order = order.lower()
            self.set_alone(False)
        elif order.lower() == 'order':
            self.bid_order = order.lower()
            self.set_alone(is_alone)
            self.print_alone()
        else:
            print(f'ERROR: NO VIABLE ORDER COMMAND.')
            order = None

    # def card_to_play(self, index):
    #     """Set the selected card from user input."""
    #     self.set_selected(self.filtered_cards[index][1])
    
    def get_player_card(self, index) -> int:
        """Get player input choosing a card from the list in hand. Returns 
        number assignment (integer) of card to play.

        Keyword arguments:
        legal_card_list: -- List of cards able to be played this round.
        """ 
        self.get_player_status()       
        return self.filtered_cards[index][1]
        
        # card = None
        # while card is None:
        #     card = input("Enter the number of a card you'd like to choose: -> ")
        #     if card.isdigit():
        #         if int(card) <= len(self.filtered_cards) and int(card) > 0:
        #             return int(card)
        #         else:
        #             card = None    
        #     else:
        #         card = None

    def get_selected(self):
        """Return selected card."""
        return self._selected
    
    def set_selected(self, selected):
        """Set the selected card."""
        if self._selected == None:
            self._selected = selected

    def get_player_status(self, cards:list[tuple [int, Card]]=None, trump: Trump=None):
        """Print the player's name and the current legal cards in their respective hand of cards."""
        print('\n')
        print('-' * 40)
        print(f'\tPLAYER: {self._name} \tTEAM: {self._team.name}')
        print('-' * 40)
        if trump:
            print(f'CARDS IN HAND: \t\tTRUMP: {trump.suit}')
        else:
            print(f'CARDS IN HAND: ')
        if cards:
            for card in cards:
                print(f'\t{card[0]}. {card[1]}')
        else:
            for card in self.filtered_cards:
                print(f'\t{card[0]}. {card[1]}')
        print('-' * 40)

    def get_tricks(self) -> int:
        """Return current tricks (hands) won this round."""
        return self._tricks
    
    def set_tricks(self):
        """Set tricks increasing value of tricks by one."""
        self._tricks += 1

    def is_alone(self) -> bool:
        """Return status if player is playing alone this round."""
        return self._is_alone
    
    def is_bot(self) -> bool:
        """Return status if player is a bot."""
        return self._is_bot

    def print_alone(self):
        """Print alone status."""
        print(f"Player {self.name} is going alone: {self.is_alone()}")

    def set_alone(self, alone: bool):
        """Set alone status for the Player object."""
        self._is_alone = alone

    def going_alone(self, bool) -> bool:
        """Check if player wants to go alone this round for more points.
        
        Keyword arguments:
        player: -- player in question, to set is_alone status.
        """
        if bool:
            self.set_alone(True)
            partner = self._get_partner()
            self._set_partner_skipped(partner)
            print(f'{self._name} is going alone.')
            # return True
        else:
            self.set_alone(False)
            print(f'{self._name} is not going alone.')
            # return False
                
    def get_skipped(self):
        """Returns True if player is skipped this round."""
        return self._is_skipped
    
    def set_skipped(self, skipped: bool):
        """Set if the player is to be skipped this round. Clears their hand of any cards.
        
        Keyword arguments:
        skipped: Set to True if the Player is to be skipped this round. False if not.
        """
        self._is_skipped = skipped
        self._cards.clear()

    def find_trumps(self, trump):
        """Update all the cards in hand with trump cards."""
        for card in self.cards:
            card.is_trump(trump)

    # Reset the status of the player
    # TODO Refactor this to a dict outside of the object.
    def reset(self):
        """Reset the status of the player for new round of play."""
        self._cards.clear()
        self._tricks = 0
        self._is_alone = False
        self._is_skipped = False
        self._selected = None
    
    # Private methods
    def _get_partner(self):
        """Return the Player that is on the same team as this Player."""
        team = self._team
        players = team.players
        for player in players:
            if player.name != self._name:
                return player

    def _set_partner_skipped(self, partner: Player) -> Player:
        """Set the partner to be skipped for the round."""
        partner.set_skipped(True)
        return partner

# Player builder
def build_players(names: list[str]) -> list[Player]: 
    """Create Player objects based on names list."""
    if not names:
        print("WARNING: NO NAMES TO CREATE PLAYER OBJECTS. EXITING BUILDER.")
        return
       
    players = [Player(name) for name in names]
    return players
