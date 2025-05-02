from unittest import TestCase, main
from euchre.cards import Card
from euchre.players import Player
from euchre.constants import SUITS

class TestCardSorting(TestCase):

    def test_cardSorting(self):
        p1 = Player("Player_1")
        c1 = Card(9, "Diamonds")

        p1.receive_card(c1)
        sorted = p1.sort_cards_by_suit()
        expected = { k: [] for k in SUITS}
        expected['Diamonds'].append(c1)

        self.assertEqual(sorted, expected)


    def test_cardSorting_everySuit(self):
        p1 = Player("Player_1")
        c1 = Card(9, "Diamonds")
        c2 = Card(9, "Hearts")
        c3 = Card(9, "Clubs")
        c4 = Card(9, "Spades")

        p1.receive_card(c1)
        p1.receive_card(c2)
        p1.receive_card(c3)
        p1.receive_card(c4)

        sorted = p1.sort_cards_by_suit()
        expected = { k: [] for k in SUITS}

        expected['Diamonds'].append(c1)
        expected['Hearts'].append(c2)
        expected['Clubs'].append(c3)
        expected['Spades'].append(c4)

        self.assertEqual(sorted, expected)



if __name__ == '__main__':
    main()
