from unittest import TestCase
from euchre.cards import Card

class TestCardComparisons(TestCase):

    def test_cardEqualByInstance(self):
        c1 = Card(9, "Clubs")
        c2 = Card(9, "Spades")

        self.assertNotEqual(c1, c2)

    
    def test_cardEqualByValue(self):
        c1 = Card(9, "Clubs")
        c2 = Card(9, "Spades")

        self.assertEqual(c1.get_value(), c2.get_value())

    
    def test_cardLessThanByInstance(self):
        c1 = Card(9, "Clubs")
        c2 = Card(9, "Spades")

        # Cards are compared by sorting suit values
        # therefore 'c' is less than 's'
        is_equal = c1 < c2

        self.assertEqual(is_equal, True)
