from unittest.mock import patch
from unittest import TestCase, main
from euchre.cards import Card
from euchre.players import Player
from euchre.trumps import Trump

class TestPlayerMethods(TestCase):
    
    def test_getName(self):
        p1 = Player("Player_1")
        self.assertEqual(p1.get_name(), "Player_1")


    def test_receiveCard(self):
        card = Card(9, "Spades")
        p1 = Player("Player_1")
        
        p1.receive_card(card)
        
        self.assertEqual(p1.get_cards(), [card])


    def test_removeCard(self):
        card = Card(14, "Spades")
        p1 = Player("Player_1")

        p1.receive_card(card)
        p1.remove_card(card)

        self.assertEqual(p1.get_cards(), [])


    def test_listCards(self):
        card = Card(13, "Diamonds")
        p1 = Player("Player_1")

        p1.receive_card(card)

        self.assertEqual(p1.list_cards(), [(1, card)])


    def test_listCards_noCards(self):
        p1 = Player("Player_1")

        self.assertEqual(p1.list_cards(), [])


    def test_filterCards(self):
        p1 = Player("Player_1")
        pc1 = Card(10, "Hearts")
        p1.receive_card(pc1)

        c1 = Card(9, "Hearts")
        trump = Trump("Spades")

        self.assertEqual(p1.filter_cards(c1, trump), [pc1])


    def test_filterCards_notMatchingFilter(self):
        p1 = Player("Player_1")
        pc1 = Card(10, "Spades")
        p1.receive_card(pc1)

        c1 = Card(9, "Hearts")
        trump = Trump("Spades")

        self.assertEqual(p1.filter_cards(c1, trump), [])

    
    def test_filterCards_fullHand_OneValid(self):
        p1 = Player("Player_1")
        pc1 = Card(10, "Hearts")
        pc2 = Card(11, "Hearts")
        pc3 = Card(12, "Hearts")
        pc4 = Card(13, "Hearts")
        pc5 = Card(14, "Clubs")

        p1.receive_card(pc1)
        p1.receive_card(pc2)
        p1.receive_card(pc3)
        p1.receive_card(pc4)
        p1.receive_card(pc5)

        c1 = Card(9, "Clubs")
        trump = Trump("Spades")

        self.assertEqual(p1.filter_cards(c1, trump), [pc5])


    def test_filterCards_fullHand_ManyValid(self):
        p1 = Player("Player_1")
        pc1 = Card(10, "Hearts")
        pc2 = Card(11, "Hearts")
        pc3 = Card(12, "Hearts")
        pc4 = Card(13, "Hearts")
        pc5 = Card(14, "Clubs")

        p1.receive_card(pc1)
        p1.receive_card(pc2)
        p1.receive_card(pc3)
        p1.receive_card(pc4)
        p1.receive_card(pc5)

        c1 = Card(9, "Hearts")
        trump = Trump("Spades")

        self.assertEqual(p1.filter_cards(c1, trump), [pc1, pc2, pc3, pc4])


    def test_filterCards_TrumpLead(self):
        p1 = Player("Player_1")
        pc1 = Card(10, "Spades")
        pc2 = Card(10, "Hearts")
        p1.receive_card(pc1)
        p1.receive_card(pc2)

        c1 = Card(9, "Spades")
        trump = Trump("Spades")

        self.assertEqual(p1.filter_cards(c1, trump), [pc1])


    def test_filterCards_TrumpLead_LeftBowerInHand(self):
        p1 = Player("Player_1")
        pc1 = Card(11, "Clubs")
        pc2 = Card(10, "Hearts")
        p1.receive_card(pc1)
        p1.receive_card(pc2)

        c1 = Card(9, "Spades")
        trump = Trump("Spades")

        self.assertEqual(p1.filter_cards(c1, trump), [pc1])


    def test_filterCards_TrumpLead_BothBowersInHand(self):
        p1 = Player("Player_1")
        pc1 = Card(11, "Clubs")
        pc2 = Card(10, "Hearts")
        pc3 = Card(11, "Spades")
        p1.receive_card(pc1)
        p1.receive_card(pc2)
        p1.receive_card(pc3)
        
        c1 = Card(9, "Spades")
        trump = Trump("Spades")

        self.assertEqual(p1.filter_cards(c1, trump), [pc1, pc3])

    @patch('builtins.input', return_value='1')
    def test_getPlayerCard(self, input):
        p1 = Player("Player_1")
        pc1 = Card(10, "Diamonds")
        pc2 = Card(11, "Diamonds")
        pc3 = Card(12, "Hearts")
        pc4 = Card(13, "Spades")
        pc5 = Card(9, "Clubs")

        p1.receive_card(pc1)
        p1.receive_card(pc2)
        p1.receive_card(pc3)
        p1.receive_card(pc4)
        p1.receive_card(pc5)

        card_list = p1.list_cards()

        self.assertEqual(p1.get_player_card(card_list), 1)



if __name__ == '__main__':
    main()
