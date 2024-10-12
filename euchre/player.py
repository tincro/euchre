class Player():
    """Class to keep track of each players cards data
    """
    def __init__(self, name):
        self._name = name
        self.cards = []

    def get_name(self):
        return self._name
    
    def receive_card(self, card):
        self.cards.append(card)
    
    def play(self, card):
        """Play the card and remove from hand."""
        if card in self.cards:
            self.cards.remove(card)