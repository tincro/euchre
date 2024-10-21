"""The Player class keeps track of the data surrounding a player.

Player(): -- The base Player class.
build_players(): -- build each player object.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from euchre.cards import Card
    from euchre.teams import Team
    from euchre.trumps import Trump

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
    get_player_card(): -- get input from player to choose a card in hand.
    get_player_status(): -- print player name and each card in hand.
    get_tricks(): -- return the tricks won for the round.
    set_tricks(): -- set the trick count increasing by one.
    is_alone(): -- returns status if Player is going alone this round.
    set_alone(): -- set the alone status for the Player.
    going_alone(): -- check if the player is going alone without a partner this round.
    reset(): -- reset the counters for the round.    
    """

    def __init__(self, name: str):
        """"Initialize player object. Player name assigned via argument name.
        _cards and _team are assigned external of initialization.
        """
        self._name = name
        self._cards = []
        self._team = None
        self._tricks = 0
        self._is_alone = False
    
    def __str__(self):
        """Return human-friendly version of player."""
        return f'{self._name}'
    
    def __repr__(self):
        """Return the player object."""
        return f'Player(\'{self._name}\')'

    # Public methods
    def get_name(self) -> str:
        """Return the player's name."""
        return self._name
    
    def get_team(self) -> Team:
        """Return the team object the player is assigned."""
        return self._team
    
    def set_team(self, team: Team):
        """Assign the player to a team."""
        self._team = team
    
    def receive_card(self, card: Card):
        """Add the received card to the players hand of cards."""
        self._cards.append(card)
    
    def remove_card(self, card: Card):
        """Remove the Card object from the Player hand."""
        if card in self._cards:
            self._cards.remove(card)
    
    def get_cards(self) -> list[Card]:
        """Returns the list of cards in players hand. Cards are not listed."""
        return self._cards
    
    def list_cards(self, cards: list[Card]=None) -> list[Card]:
        """Returns enumerated list of cards currently in hand. If no cards list passed, all cards returned.
        
        Keyword arguments:
        cards: -- list of cards to enumerate.
        """
        # Start enumeration at 1 for player input simplicity
        if cards:
            return list(enumerate(cards, start=1))
        return list(enumerate(self._cards, start=1))
    
    def filter_cards(self, card_to_match: Card, trump: Trump):
        """Filters the list of cards in player's hand for legal cards and returns it.
            
        card_to_match: -- card to compare suits against to filter.
        trump: -- the curren trump for the round.
        """
        # If Left Bower played first we need to filter for trump suits instead
        if card_to_match.is_trump(trump):
            suit_to_match = trump.get_suit()
        else:
            suit_to_match = card_to_match.get_suit()

        legal_list = []

        for card in self._cards:
            suit = card.get_suit()
            # Special case for Left Bower played later in round, and shares suit with lead card.
            if suit == suit_to_match and not card_to_match.is_trump(trump) and card.is_trump(trump):
                continue
            # Otherwise follow normal filtering
            elif suit == suit_to_match:
                legal_list.append(card)
            # If trump was lead we need to get the left bower in the filter.
            if suit_to_match == trump.get_suit():
                if card.get_rank() == "Jack" and suit == trump.get_left():
                    legal_list.append(card)

        return legal_list

    def get_player_card(self, legal_card_list: list[Card]) -> int:
        """Get player input choosing a card from the list in hand. Returns integer.

        Keyword arguments:
        previous_revealed: -- Revealed card from the top of deck.
        """
        if not legal_card_list:
            return
        
        card = None
        while card is None:
            card = input("Enter the number of a card you'd like to choose: -> ")
            if card.isdigit():
                if int(card) <= len(legal_card_list) and int(card) > 0:
                    return int(card)
                else:
                    card = None    
            else:
                card = None

    def get_player_status(self, cards:list[Card]=None, trump: Trump=None):
        """Print the player's name and the current legal cards in their respective hand of cards."""
        print('\n')
        print('-' * 40)
        print(f'\tPLAYER: {self._name} \tTEAM: {self._team.get_name()}')
        print('-' * 40)
        if trump:
            print(f'CARDS IN HAND: \t\tTRUMP: {trump.get_suit()}')
        else:
            print(f'CARDS IN HAND: ')
        if cards:
            for card in cards:
                print(f'\t{card[0]}. {card[1]}')
        else:
            for card in self.list_cards():
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

    def set_alone(self, alone: bool):
        """Set alone status for the Player object."""
        if alone == True:
            self._is_alone = True
            return
        self._is_alone = False

    def going_alone(self) -> bool:
        """Check if player wants to go alone this round for more points.
        Keyword arguments:
        player: -- player in question, to set is_alone status.
        """
        while True:
            is_alone = input("Are you going alone?: -> ")
            match is_alone.lower():
                case 'yes':
                    self.set_alone(True)
                    return True
                case 'no':
                    self.set_alone(False)
                    return False

    def reset(self):
        """Reset tricks for new round of play."""
        self._tricks = 0
        self._is_alone = False

# Player builder
def build_players(names: list[str]) -> list[Player]:
    """Create Player objects based on names list."""
    if not names:
        return
       
    players = [Player(name) for name in names]
    return players
