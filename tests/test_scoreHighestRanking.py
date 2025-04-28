import unittest
from euchre.__main__ import get_highest_rank_card
from euchre.cards import Card
from euchre.players import Player
from euchre.trumps import Trump

class TestScoreTrick(unittest.TestCase):
    
    def setUp(self):
        
        # Create Players
        self.p1 = Player("Player1")
        self.p2 = Player("Player2")
        self.p3 = Player("Player3")
        self.p4 = Player("Player4")
        
        # Create Cards (9, 10, J, Q, K, A) and assign Trump suit, 
        self.c9d = Card(9, "Diamonds")
        self.c10d = Card(10, "Diamonds")
        self.cJd = Card(11, "Diamonds")
        self.cQd = Card(12, "Diamonds")
        self.cKd = Card(13, "Diamonds")
        self.cAd = Card(14, "Diamonds")

        self.c9h = Card(9, "Hearts")
        self.c10h = Card(10, "Hearts")
        self.cJh = Card(11, "Hearts")
        self.cQh = Card(12, "Hearts")
        self.cKh = Card(13, "Hearts")
        self.cAh = Card(14, "Hearts")

        self.tH = Trump("Hearts")
        self.tD = Trump("Diamonds")
        self.tC = Trump("Clubs")
        self.tS = Trump("Spades")

        # Assign cards played in order
        self.cards_played_lead_9 = [
            (self.p1, self.c9d),
            (self.p2, self.cAd),
            (self.p3, self.c10d),
            (self.p4, self.cQd)
        ]

        self.cards_played_lead_10 = [
            (self.p1, self.c10d),
            (self.p2, self.cAd),
            (self.p3, self.cKd),
            (self.p4, self.cQd)
        ]

        self.cards_played_lead_Jack = [
            (self.p1, self.cJd),
            (self.p2, self.c10d),
            (self.p3, self.cAd),
            (self.p4, self.cKd)
        ]

        self.cards_played_lead_Queen = [
            (self.p1, self.cQd),
            (self.p2, self.c10d),
            (self.p3, self.cAd),
            (self.p4, self.cKd)
        ]

        self.cards_played_lead_King = [
            (self.p1, self.cKd),
            (self.p2, self.c10d),
            (self.p3, self.cAd),
            (self.p4, self.cQd)
        ]

        self.cards_played_lead_Ace = [
            (self.p1, self.cAd),
            (self.p2, self.c10d),
            (self.p3, self.cKd),
            (self.p4, self.cQd)
        ]

        self.cards_played_lead_9_wJack = [
            (self.p1, self.c9d),
            (self.p2, self.cAd),
            (self.p3, self.c10d),
            (self.p4, self.cJd)
        ]

        self.cards_played_lead_Queen_D_with_9_Trumps_H = [
            (self.p1, self.cQd),
            (self.p2, self.c10d),
            (self.p3, self.cAd),
            (self.p4, self.c9h)
        ]
    
    def test_getHighestRankingCard_lead_9(self):

        winner_test = get_highest_rank_card(self.cards_played_lead_9, self.tH)
        winner_expected = (self.p2, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)
    
    def test_getHighestRankingCard_lead_10(self):

        winner_test = get_highest_rank_card(self.cards_played_lead_10, self.tH)
        winner_expected = (self.p2, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)

    def test_getHighestRankingCard_lead_Jack(self):

        winner_test = get_highest_rank_card(self.cards_played_lead_Jack, self.tS)
        winner_expected = (self.p3, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)

    def test_getHighestRankingCard_lead_Jack_asLeftBower(self):

        winner_test = get_highest_rank_card(self.cards_played_lead_Jack, self.tH)
        winner_expected = (self.p1, self.cJd)
        
        self.assertEqual(winner_test, winner_expected)

    def test_getHighestRankingCard_lead_Queen(self):

        winner_test = get_highest_rank_card(self.cards_played_lead_Queen, self.tH)
        winner_expected = (self.p3, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)

    def test_getHighestRankingCard_lead_King(self):

        winner_test = get_highest_rank_card(self.cards_played_lead_King, self.tH)
        winner_expected = (self.p3, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)

    def test_getHighestRankingCard_lead_Ace(self):

        winner_test = get_highest_rank_card(self.cards_played_lead_Ace, self.tH)
        winner_expected = (self.p1, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)

    def test_getHighestRankingCard_lead_Jack_with_Trumps(self):

        winner_test = get_highest_rank_card(self.cards_played_lead_Jack, self.tD)
        winner_expected = (self.p1, self.cJd)
        
        self.assertEqual(winner_test, winner_expected)

    def test_getHighestRankingCard_lead_9_with_Trumps_no_Jack(self):

        winner_test = get_highest_rank_card(self.cards_played_lead_9, self.tD)
        winner_expected = (self.p2, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)

    def test_getHighestRankingCard_lead_9_with_Trumps_with_Jack(self):

        winner_test = get_highest_rank_card(self.cards_played_lead_9_wJack, self.tD)
        winner_expected = (self.p4, self.cJd)
        
        self.assertEqual(winner_test, winner_expected)

    def test_getHighestRankingCard_lead_Q_with_9_Trumps(self):

        winner_test = get_highest_rank_card(self.cards_played_lead_Queen_D_with_9_Trumps_H, self.tH)
        winner_expected = (self.p4, self.c9h)
        
        self.assertEqual(winner_test, winner_expected)



if __name__ == '__main__':
    unittest.main()
