import unittest
from euchre.cards import Card
from euchre.trumps import Trump

class TestCardMethods(unittest.TestCase):

    def setUp(self):
        self.c9S = Card(9, "Spades")
        self.c9H = Card(9,"Hearts")
        self.c9C = Card(9, "Clubs")
        self.c9D = Card(9, "Diamonds")

        self.cJS = Card(11, "Spades")
        self.cJC = Card(11, "Clubs")

        self.tS = Trump("Spades")

    def test_cardIsTrump_Spades_9S(self):
        card = self.c9S
        spades = self.tS
        
        self.assertTrue(card.is_trump(spades))

    def test_cardIsTrump_Spades_9H(self):
        card = self.c9H
        spades = self.tS

        self.assertFalse(card.is_trump(spades))

    def test_cardIsTrump_Spades_9C(self):
        card = self.c9C
        spades = self.tS

        self.assertFalse(card.is_trump(spades))

    def test_cardIsTrump_Spades_9D(self):
        card = self.c9D
        spades = self.tS

        self.assertFalse(card.is_trump(spades))

    def test_cardIsTrump_Spades_JS(self):
        card = self.cJS
        spades = self.tS

        self.assertTrue(card.is_trump(spades))

    def test_cardIsTrump_Spades_JC(self):
        card = self.cJC
        spades = self.tS

        self.assertTrue(card.is_trump(spades))

    def test_updateCardValueToTrump(self):
        pass

if __name__ == '__main__':
    unittest.main()
