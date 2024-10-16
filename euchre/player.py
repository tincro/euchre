"""The Player class keeps track of the data surrounding a player."""

class Player():
    def __init__(self, name):
        self._name = name
        self._cards = []
    
    def __str__(self):
        return f'{self._name}'
    
    def __repr__(self):
        return f'Player(\'{self._name}\')'

    def get_name(self):
        return self._name
    
    def receive_card(self, card):
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
        """Print the player's name and their current hand of cards."""
        print('----------------')
        print(f'PLAYER: {self._name}')
        print(f'CARDS IN HAND: ')
        if cards:
            for card in cards:
                print(card)
        else:
            for card in self.list_cards():
                print(card)