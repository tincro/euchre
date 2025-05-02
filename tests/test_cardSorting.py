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


    def test_cardSorting_sameSuit_MixedValues(self):
        p1 = Player("Player_1")
        c1 = Card(11, "Diamonds")
        c2 = Card(14, "Diamonds")
        c3 = Card(12, "Diamonds")
        c4 = Card(9, "Diamonds")

        p1.receive_card(c1)
        p1.receive_card(c2)
        p1.receive_card(c3)
        p1.receive_card(c4)

        sorted = p1.sort_cards_by_suit()
        expected = { k: [] for k in SUITS}

        expected['Diamonds'].append(c1)
        expected['Diamonds'].append(c2)
        expected['Diamonds'].append(c3)
        expected['Diamonds'].append(c4)

        self.assertEqual(sorted, expected)


    def test_cardSorting_sameSuit_SortedValues(self):
        p1 = Player("Player_1")
        c1 = Card(11, "Diamonds")
        c2 = Card(14, "Diamonds")
        c3 = Card(12, "Diamonds")
        c4 = Card(9, "Diamonds")

        p1.receive_card(c1)
        p1.receive_card(c2)
        p1.receive_card(c3)
        p1.receive_card(c4)

        sorted = p1.sort_cards_by_value()
        expected = { k: [] for k in SUITS}

        expected['Diamonds'].append(c2) # Ace
        expected['Diamonds'].append(c3) # Queen
        expected['Diamonds'].append(c1) # Jack
        expected['Diamonds'].append(c4) # 9

        self.assertEqual(sorted, expected)


    def test_cardSorting_inHand(self):
        p1 = Player("Player_1")

        c1 = Card(11, "Diamonds")
        c2 = Card(14, "Diamonds")
        c3 = Card(12, "Diamonds")
        p1.receive_card(c1)
        p1.receive_card(c2)
        p1.receive_card(c3)

        c5 = Card(9, "Spades")
        c6 = Card(14, "Spades")
        p1.receive_card(c5)
        p1.receive_card(c6)

        # Order = ("Spades", "Diamonds", "Clubs", "Hearts")
        sorted = p1.sorted_cards_in_hand()
        expected = [c6, c5, c2, c3, c1 ]

        self.assertEqual(sorted, expected)


if __name__ == '__main__':
    main()
