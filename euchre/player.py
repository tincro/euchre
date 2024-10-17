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
        self._is_alone = False
    
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
    
    def filter_cards(self, card_to_match, trump):
        """Filters the list of cards in player's hand for legal cards and returns it.
            
        card_to_match: card to compare suits against to filter
        """
        suit_to_match = card_to_match.get_suit()
        legal_list = []

        for card in self._cards:
            if card.get_suit() == suit_to_match:
                legal_list.append(card)
            if suit_to_match == trump.get_suit():
                # TODO This needs to show up when the trump is lead
                if card.get_rank() == "Jack" and card.get_color() == trump.get_color():
                    legal_list.append(card)

        return legal_list
    
    def play(self, card):
        """Play the card and remove from hand."""
        if card in self._cards:
            self._cards.remove(card)

    def get_player_status(self, cards=None, trump=None):
        """Print the player's name and the current legal cards in their respective hand of cards."""
        print('\n')
        print('-' * 40)
        print(f'\tPLAYER: {self._name}')
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

    def get_tricks(self):
        """Return current tricks (hands) won this round."""
        return self._tricks
    
    def set_tricks(self):
        """Set tricks increasing value of tricks by one."""
        self._tricks += 1

    def is_alone(self):
        """Return status if player is playing alone this round."""
        return self._is_alone

    def set_alone(self, alone):
        if alone == True:
            self._is_alone = True

    def reset(self):
        """Reset tricks for new round of play."""
        self._tricks = 0
        self._is_alone = False