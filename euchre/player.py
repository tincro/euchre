"""The Player class keeps track of the data surrounding a player.

Player(): -- The base Player class.
build_players(): -- build each player object.
"""
from card import Card
from team import Team
from trump import Trump

class Player():
    """The base class for Player objects.

    get_name(): -- returns the name of the Player.
    get_team(): -- returns the team object this Player is assigned.
    set_team(): -- assign the Player to the Team object.
    receive_card(): -- add the card object to the Player's hand of cards.
    get_cards(): -- returns the list of  cards in the Player's hand.
    list_cards(): -- returns enumerated list of cards.
    filter_cards(): -- filters cards that are legal to play for the hand.
    play(): -- play the card and remove it from hand.
    get_player_status(): -- print player name and each card in hand.
    get_tricks(): -- return the tricks won for the round.
    set_tricks(): -- set the trick count increasing by one.
    is_alone(): -- returns status if Player is going alone this round.
    set_alone(): -- set the alone status for the Player.
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
        suit_to_match = card_to_match.get_suit()
        legal_list = []

        for card in self._cards:
            suit = card.get_suit()
            if suit == suit_to_match:
                legal_list.append(card)
            if suit_to_match == trump.get_suit():
                # TODO This needs to show up when the trump is lead
                if card.get_rank() == "Jack" and suit == trump.get_left():
                    legal_list.append(card)

        return legal_list
    
    def play(self, card: Card):
        """Play the card and remove it from hand."""
        if card in self._cards:
            self._cards.remove(card)

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
        # print('\n')
        if cards:
            for card in cards:
                print(f'\t{card[0]}. {card[1]}')
        else:
            for card in self.list_cards():
                print(f'\t{card[0]}. {card[1]}')
        # print('\n')
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
        self._is_alone = False

    def reset(self):
        """Reset tricks for new round of play."""
        self._tricks = 0
        self._is_alone = False

# Player builder
def build_players(names: list[str]) -> list[Player]:
    """Create Player objects based on names list."""
    players = [Player(name) for name in names]

    return players

