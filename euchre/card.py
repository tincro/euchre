class Card():
    def __init__(self, value, suit):
        self._value = value
        self._suit = suit

    def get_value(self):
        return self._value
    
    def get_suit(self):
        return self._suit