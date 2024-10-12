class Player():
    """Class to keep track of each players cards data
    """
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
        return self._cards
    
    def play(self, card):
        """Play the card and remove from hand."""
        if card in self._cards:
            self._cards.remove(card)