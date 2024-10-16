"""The Player class keeps track of the data surrounding a player."""

class Player():
    def __init__(self, name):
        """"Initialize player object. Player name assigned via argument name.
        _cards and _team are assigned external of initialization.
        """
        MAX_TRICKS = 5

        self._name = name
        self._cards = []
        self._team = None
        self._tricks = 0
    
    def __str__(self):
        """Return human-friendly version of player."""
        return f'{self._name}'
    
    def __repr__(self):
        """Return the player object."""
        return f'Player(\'{self._name}\')'

    def get_name(self):
        """Return the player's name."""
        return self._name
    
    def get_team(self):
        """Return the team object the player is assigned."""
        return self._team
    
    def set_team(self, team):
        """Assign the player to a team."""
        self._team = team
    
    def receive_card(self, card):
        """Add the received card to the players hand of cards."""
        self._cards.append(card)
    
    def get_cards(self):
        """Returns the list of cards in players hand. Cards are not listed."""
        return self._cards
    
    def list_cards(self, cards=None):
        """Returns enumerated list of cards currently in hand."""
        # Start enumeration at 1 for player input simplicity
        if cards:
            return list(enumerate(cards, start=1))
        return list(enumerate(self._cards, start=1))
    
    def filter_cards(self, card_to_match):
        """Filters the list of cards in player's hand for legal cards and returns it.
            
        card_to_match: card to compare suits against to filter
        """
        suit_to_match = card_to_match.get_suit()
        # color_to_match = card_to_match.get_color()
        legal_list = []

        for card in self._cards:
            if card.get_suit() == suit_to_match:
                legal_list.append(card)

            # Implementation for filtering for trump matching
            # elif card.get_color() == color_to_match and card.get_rank() == "Jack":
            #     legal_list.append(card)

        return legal_list
    
    def play(self, card):
        """Play the card and remove from hand."""
        if card in self._cards:
            self._cards.remove(card)

    def get_player_status(self, cards=None):
        """Print the player's name and the current legal cards in their respective hand of cards."""
        print('-' * 40)
        print(f'PLAYER: {self._name}')
        print(f'CARDS IN HAND: ')
        if cards:
            for card in cards:
                print(f'{card[0]}. {card[1]}')
        else:
            for card in self.list_cards():
                print(f'{card[0]}. {card[1]}')
        print('-' * 40)

    def get_tricks(self):
        """Return current tricks (hands) won this round."""
        return self._tricks
    
    def set_tricks(self):
        """Set tricks increasing value of tricks by one."""
        self._tricks += 1

    def reset(self):
        """Reset tricks for new round of play."""
        self._tricks = 0