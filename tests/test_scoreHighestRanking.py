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

        self.c9c = Card(9, "Clubs")
        self.c10c = Card(10, "Clubs")
        self.cJc = Card(11, "Clubs")
        self.cQc = Card(12, "Clubs")
        self.cKc = Card(13, "Clubs")
        self.cAc = Card(14, "Clubs")

        self.c9s = Card(9, "Spades")
        self.c10s = Card(10, "Spades")
        self.cJs = Card(11, "Spades")
        self.cQs = Card(12, "Spades")
        self.cKs = Card(13, "Spades")
        self.cAs = Card(14, "Spades")

        self.tH = Trump("Hearts")
        self.tD = Trump("Diamonds")
        self.tC = Trump("Clubs")
        self.tS = Trump("Spades")


    def test_getHighestRankingCard_lead_9(self):

        cards_played = [
            (self.p1, self.c9d),
            (self.p2, self.cAd),
            (self.p3, self.c10d),
            (self.p4, self.cQd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tH)
        winner_expected = (self.p2, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)

    
    def test_getHighestRankingCard_lead_10(self):

        cards_played = [
            (self.p1, self.c10d),
            (self.p2, self.cAd),
            (self.p3, self.cKd),
            (self.p4, self.cQd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tH)
        winner_expected = (self.p2, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)


    def test_getHighestRankingCard_lead_Jack(self):

        cards_played = [
            (self.p1, self.cJd),
            (self.p2, self.c10d),
            (self.p3, self.cAd),
            (self.p4, self.cKd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tS)
        winner_expected = (self.p3, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)


    def test_getHighestRankingCard_lead_Queen(self):

        cards_played = [
            (self.p1, self.cQd),
            (self.p2, self.c10d),
            (self.p3, self.cAd),
            (self.p4, self.cKd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tH)
        winner_expected = (self.p3, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)


    def test_getHighestRankingCard_lead_King(self):

        cards_played = [
            (self.p1, self.cKd),
            (self.p2, self.c10d),
            (self.p3, self.cAd),
            (self.p4, self.cQd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tH)
        winner_expected = (self.p3, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)


    def test_getHighestRankingCard_lead_Ace(self):

        cards_played = [
            (self.p1, self.cAd),
            (self.p2, self.c10d),
            (self.p3, self.cKd),
            (self.p4, self.cQd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tH)
        winner_expected = (self.p1, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)


    def test_getHighestRankingCard_AllSameSuit_lead_Jack_asRightBower(self):

        cards_played = [
            (self.p1, self.cJd),
            (self.p2, self.c10d),
            (self.p3, self.cAd),
            (self.p4, self.cKd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tD)
        winner_expected = (self.p1, self.cJd)
        
        self.assertEqual(winner_test, winner_expected)


    def test_getHighestRankingCard_AllSameSuit_lead_Jack_asLeftBower(self):

        cards_played = [
            (self.p1, self.cJd),
            (self.p2, self.c10d),
            (self.p3, self.cAd),
            (self.p4, self.cKd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tH)
        winner_expected = (self.p1, self.cJd)
        
        self.assertEqual(winner_test, winner_expected)


    def test_getHighestRankingCard_lead_9_with_Trumps_no_Jack(self):

        cards_played = [
            (self.p1, self.c9d),
            (self.p2, self.cAd),
            (self.p3, self.c10d),
            (self.p4, self.cQd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tD)
        winner_expected = (self.p2, self.cAd)
        
        self.assertEqual(winner_test, winner_expected)


    def test_getHighestRankingCard_lead_9_with_Trumps_with_Jack(self):

        cards_played = [
            (self.p1, self.c9d),
            (self.p2, self.cAd),
            (self.p3, self.c10d),
            (self.p4, self.cJd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tD)
        winner_expected = (self.p4, self.cJd)
        
        self.assertEqual(winner_test, winner_expected)


    def test_getHighestRankingCard_lead_Q_with_9_Trumps(self):

        cards_played = [
            (self.p1, self.cQd),
            (self.p2, self.c10d),
            (self.p3, self.cAd),
            (self.p4, self.c9h)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tH)
        winner_expected = (self.p4, self.c9h)
        
        self.assertEqual(winner_test, winner_expected)


    def test_getHighestRankingCard_lead_Q_with_mixed_NoTrumps(self):

        cards_played = [
            (self.p1, self.cQd),
            (self.p2, self.c10c),
            (self.p3, self.cAs),
            (self.p4, self.cKd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tH)
        winner_expected = (self.p4, self.cKd)
        
        self.assertEqual(winner_test, winner_expected)


    def test_getHighestRankingCard_lead_Q_with_mixed_withHighTrumps(self):

        cards_played = [
            (self.p1, self.cQd),
            (self.p2, self.c10c),
            (self.p3, self.cAs),
            (self.p4, self.cKd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tS)
        winner_expected = (self.p3, self.cAs)
        
        self.assertEqual(winner_test, winner_expected)


    def test_getHighestRankingCard_lead_Q_with_mixed_withLowTrumps(self):

        cards_played = [
            (self.p1, self.cQd),
            (self.p2, self.c10c),
            (self.p3, self.c9s),
            (self.p4, self.cKd)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tS)
        winner_expected = (self.p3, self.c9s)
        
        self.assertEqual(winner_test, winner_expected)

    
    def test_getHighestRankingCard_JackMiddle_noTrumps(self):

        cards_played = [
            (self.p1, self.cKs),
            (self.p2, self.c10s),
            (self.p3, self.cJs),
            (self.p4, self.c9s)
        ]

        winner_test = get_highest_rank_card(cards_played, self.tH)
        winner_expected = (self.p1, self.cKs)
        
        self.assertEqual(winner_test, winner_expected)


if __name__ == '__main__':
    unittest.main()
