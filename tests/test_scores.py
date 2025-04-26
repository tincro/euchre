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
        
        # Create Cards and assign Trump suit
        self.c1 = Card(10, "Diamonds")
        self.c2 = Card(14, "Diamonds")
        self.c3 = Card(13, "Diamonds")
        self.c4 = Card(12, "Diamonds")
        self.t1 = Trump("Hearts")

        # Assign cards played in order
        self.cards_played = [
            (self.p1, self.c1),
            (self.p2, self.c2),
            (self.p3, self.c3),
            (self.p4, self.c4)
        ]
    
    def test_getHighestRankingCard(self):

        winner_test = get_highest_rank_card(self.cards_played, self.t1)
        winner_expected = (self.p2, self.c2)
        
        self.assertEqual(winner_test, winner_expected)

if __name__ == '__main__':
    unittest.main()
