from unittest.mock import patch
from unittest import TestCase, main
from euchre.cards import Card
from euchre.players import Player
from euchre.teams import Team, assign_player_teams
from euchre.trumps import Trump
from euchre.__main__ import play_cards

class TestPlayerLoopMechanics(TestCase):
    def setUp(self):
        self.p1 = Player("Player_1")
        
        self.pcAS = Card(14, "Spades")
        self.pc9H = Card(9, "Hearts")
        self.pcAD = Card(14, "Diamonds")
        self.pcAC = Card(14, "Clubs")
        self.pcQC = Card(12, "Clubs")

        self.p1.receive_card(self.pcAS)
        self.p1.receive_card(self.pc9H)
        self.p1.receive_card(self.pcAD)
        self.p1.receive_card(self.pcAC)
        self.p1.receive_card(self.pcQC)

        # Computer players setup
        self.p2 = Player("Pig")
        self.jS = Card(11, "Spades")
        self.p2.receive_card(self.jS)

        self.p3 = Player("Dog")
        self.kH = Card(13, "Hearts")
        self.p3.receive_card(self.kH)

        self.p4 = Player("Cow")
        self.aH = Card(14, "Hearts")
        self.p4.receive_card(self.aH)

        # Teams setup
        t1 = Team(self.p1, self.p3, "Player_team")
        t2 = Team(self.p2, self.p4, "Opponent_team")
        t = [t1, t2]
        assign_player_teams(t)

        # Turn order
        self.players = [self.p2, self.p3, self.p4, self.p1]
        self.trump = Trump("Spades")

    @patch('builtins.input', return_value='1')
    def test_playerHasCardAfterPlayingCard(self, input):
        cards_played = play_cards(self.players, self.trump)

        self.assertEqual(cards_played, [
            (self.p2, self.jS), 
            (self.p3, self.kH), 
            (self.p4, self.aH), 
            (self.p1,self.pcAS)
        ])
        

if __name__ == '__main__':
    main()
