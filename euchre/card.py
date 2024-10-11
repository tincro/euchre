class Card():
    '''Class is modeled after a standard deck of cards, but fits for the 
    purposes of the card game Euchre. For this game, Ace is high, so for now 
    we have Ace value as 14 instead of 1 to be more powerful than the King.
    '''
    def __init__(self, value, suit):
        self._value = value
        self._suit = suit
        self._rank = self._convert(self._value)

    def __str__(self):
        return f'{self._rank} of {self._suit}'
    
    def __repr__(self):
        return f'Card(\'{self._rank}\', \'{self._suit}\')'
    
    def _convert(self, value):
        '''Convert numeral cards to string based familiar names 
        (e.g., 11 -> "Jack").
        '''
        match value:
            case 11:
                return "Jack"
            case 12:
                return "Queen"
            case 13:
                return "King"
            case 14:
                return "Ace"
            case _:
                if value == 9 or value == 10:
                    return value
                else:
                    return "Not valid card value. Remove card from deck."
    
    def get_value(self):
        return self._value
    
    def get_suit(self):
        return self._suit
   
    def get_rank(self):
        return self._rank