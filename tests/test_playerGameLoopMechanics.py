from unittest.mock import patch
from unittest import TestCase, main, skipIf
from euchre.cards import Card
from euchre.players import Player
from euchre.teams import Team, assign_player_teams
from euchre.trumps import Trump
from euchre.__main__ import play_cards

# Set to False if you want to run all tests with skipIf decorator
skip_passing = True
skip_failing = False

# TODO Actually implement tests for bots, right now they are actual human players

# These tests take a long time to process on the commandline
# since they rely on input from the terminal
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
        self.jC = Card(11, "Clubs")
        self.p2.receive_card(self.jS)
        self.p2.receive_card(self.jC)

        self.p3 = Player("Dog")
        self.kH = Card(13, "Hearts")
        self.qS = Card(12, "Spades")
        self.p3.receive_card(self.kH)
        self.p3.receive_card(self.qS)

        self.p4 = Player("Cow")
        self.aH = Card(14, "Hearts")
        self.kS = Card(13, "Spades")
        self.p4.receive_card(self.aH)
        self.p4.receive_card(self.kS)

        # Teams setup
        t1 = Team(self.p1, self.p3, "Player_team")
        t2 = Team(self.p2, self.p4, "Opponent_team")
        t = [t1, t2]
        assign_player_teams(t)

        # Turn order
        self.players = [self.p2, self.p3, self.p4, self.p1]
        self.trump = Trump("Spades")


    @skipIf(skip_passing, "Test is working, skipping for now.")
    @patch('builtins.input', side_effect=['2','1','1','1'])
    def test_loop_playersPlayCardFromHand(self, input):
        cards_played = play_cards(self.players, self.trump)

        self.assertEqual(cards_played, [
            (self.p2, self.jC), 
            (self.p3, self.qS), 
            (self.p4, self.kS), 
            (self.p1,self.pcAS)
        ])


    @skipIf(skip_passing, "Test is working, skipping for now.")
    @patch('builtins.input', side_effect=['2','1','1','1'])
    def test_cardsInHandAfterPlaying(self, input):
        cards_played = play_cards(self.players, self.trump)
        
        # Cards in players hand
        #   self.pcAS = Card(14, "Spades") <- played 
        #   self.pc9H = Card(9, "Hearts")
        #   self.pcAD = Card(14, "Diamonds")
        #   self.pcAC = Card(14, "Clubs")
        #   self.pcQC = Card(12, "Clubs")
        p1_cards = self.p1.get_cards()

        self.assertEqual(p1_cards, [self.pc9H, self.pcAD, self.pcAC, self.pcQC])

    
    @skipIf(skip_passing, "Test is working, skipping for now.")
    @patch('builtins.input', side_effect=['2','1','1','1'])
    def test_listCardsAfterPlaying(self, input):
        cards_played = play_cards(self.players, self.trump)
        
        # Cards in players hand
        #   self.pcAS = Card(14, "Spades") <- played 
        #   self.pc9H = Card(9, "Hearts")
        #   self.pcAD = Card(14, "Diamonds")
        #   self.pcAC = Card(14, "Clubs")
        #   self.pcQC = Card(12, "Clubs")
        p1_cards = self.p1.list_cards()

        self.assertEqual(p1_cards, [
            (1, self.pc9H),
            (2, self.pcAD), 
            (3, self.pcAC), 
            (4, self.pcQC)
        ])


    @skipIf(skip_passing, "Test is working, skipping for now.")
    @patch('builtins.input', side_effect=['2','1','1','1','1','1','1','1'])
    def test_playerCardsPlayed_TwoHands(self, input):
        cards_played_r1 = play_cards(self.players, self.trump)
        cards_played_r2 = play_cards(self.players, self.trump)
        
        # Cards in players hand
        #   self.pcAS = Card(14, "Spades")  <- played r1
        #   self.pc9H = Card(9, "Hearts")   <- played r2
        #   self.pcAD = Card(14, "Diamonds")
        #   self.pcAC = Card(14, "Clubs")
        #   self.pcQC = Card(12, "Clubs")
        p1_card_r1 = cards_played_r1[3][1]
        p1_card_r2 = cards_played_r2[3][1]

        self.assertNotEqual(p1_card_r1, p1_card_r2)


    @skipIf(skip_failing, "Test is failing, skipping for now.")
    @patch('builtins.input', side_effect=['2','1','1','1','1','1','1','1'])
    def test_LeaderCardsPlayed_TwoHands(self, input):
        cards_played_r1 = play_cards(self.players, self.trump)
        cards_played_r2 = play_cards(self.players, self.trump)
        
        # Cards in players hand
        #   self.pcAS = Card(14, "Spades")  <- played r1
        #   self.pc9H = Card(9, "Hearts")   <- played r2
        #   self.pcAD = Card(14, "Diamonds")
        #   self.pcAC = Card(14, "Clubs")
        #   self.pcQC = Card(12, "Clubs")
        p2_card_r1 = cards_played_r1[0][1]
        p2_card_r2 = cards_played_r2[0][1]

        self.assertNotEqual(p2_card_r1, p2_card_r2)


    @skipIf(skip_failing, "Test is failing, skipping for now.")
    @patch('builtins.input', side_effect=['2','1','1','1','1','1','1','1'])
    def test_LeaderCardsPlayed_TwoHands_listCards(self, input):
        cards_played_r1 = play_cards(self.players, self.trump)
        cards_played_r2 = play_cards(self.players, self.trump)
        
        # Cards in players hand
        #   self.pcAS = Card(14, "Spades")  <- played r1
        #   self.pc9H = Card(9, "Hearts")   <- played r2
        #   self.pcAD = Card(14, "Diamonds")
        #   self.pcAC = Card(14, "Clubs")
        #   self.pcQC = Card(12, "Clubs")
        cards = self.p2.list_cards()

        self.assertEqual(cards, [])



    @skipIf(skip_passing, "Test is passing, skipping for now.")
    def test_BotPlayer_CardsInHand(self):
        # self.p2 = Player("Pig")
        # self.jS = Card(11, "Spades")
        # self.jC = Card(11, "Clubs")
        cards = self.p2.get_cards()
        expected = [self.jS, self.jC]

        self.assertEqual(cards, expected)


    @skipIf(skip_passing, "Test is passing, skipping for now.")
    def test_BotPlayer_CardsInHand_afterRemovingCard(self):
        # self.p2 = Player("Pig")
        # self.jS = Card(11, "Spades")
        # self.jC = Card(11, "Clubs")
        self.p2.remove_card(self.jC)

        cards = self.p2.get_cards()
        expected = [self.jS]

        self.assertEqual(cards, expected)


    @skipIf(skip_passing, "Test is passing, skipping for now.")
    @patch('builtins.input', side_effect=['2','1','1','1'])
    def test_BotPlayer_CardsInHand_afterPlayingCard(self, input):
        cards_played = play_cards(self.players, self.trump)
        
        # self.p2 = Player("Pig")
        # self.jS = Card(11, "Spades")
        # self.jC = Card(11, "Clubs")

        cards = self.p2.get_cards()
        expected = [self.jS]

        self.assertEqual(cards, expected)


    @patch('builtins.input', side_effect=['2','1','1','1'])
    def test_BotPlayer_listCards_afterPlayingCard(self, input):
        cards_played = play_cards(self.players, self.trump)
        
        # self.p2 = Player("Pig")
        # self.jS = Card(11, "Spades")
        # self.jC = Card(11, "Clubs")

        cards = self.p2.list_cards()
        expected = [(1, self.jS)]

        self.assertEqual(cards, expected)


    @patch('builtins.input', side_effect=['2','1','1','1'])
    def test_BotPlayer_filterCards_afterPlayingCard(self, input):
        cards_played = play_cards(self.players, self.trump)
        
        # self.p2 = Player("Pig")
        # self.jS = Card(11, "Spades")
        # self.jC = Card(11, "Clubs")
        filtered_cards = self.p2.filter_cards(None, self.trump)

        cards = self.p2.list_cards(filtered_cards)
        expected = [(1, self.jS)]

        self.assertEqual(cards, expected)


    @skipIf(skip_passing, "Test is passing, skipping for now.")
    def test_BotPlayer_listCards_noFilter(self):

        # self.p2 = Player("Pig")
        # self.jS = Card(11, "Spades")
        # self.jC = Card(11, "Clubs")

        cards = self.p2.list_cards()
        expected = [(1, self.jS), (2, self.jC)]

        self.assertEqual(cards, expected)


    @skipIf(skip_passing, "Test is passing, skipping for now.")
    def test_BotPlayer_listCards_allTrumpInHand_withFilter_noTrumpSuit(self):

        # self.p2 = Player("Pig")
        # self.jS = Card(11, "Spades")
        # self.jC = Card(11, "Clubs")

        match = Card(9, "Hearts")

        filtered_list = self.p2.filter_cards(match, self.trump)
        cards = self.p2.list_cards(filtered_list)

        expected = [(1, self.jS), (2, self.jC)]
        
        self.assertEqual(cards, expected)
        

if __name__ == '__main__':
    main()
