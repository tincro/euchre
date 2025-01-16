"""Module for holding the logic for the computer bot players.


"""
from docs.constants import BOTS
from src.gui.trumps import Trump
from src.gui.cards import Card
from src.gui.players import Player

# The base Bot class
class Bot(Player):
    """The base class for the computer bot Players.
    
    The bot players are activated when there are less than 4 human players.
    They have the same functionality for the player, with the exception that 
    the bot can play the hands for the non-human players in the game. There
    can be as many bot players as necessary.

    TODO: May need to rewrite some functions for the bot to play the game
    - bot needs to know if it should order the trump or pass
    - if second round of bidding, bot should decide to order any of the trump or pass
    - if bot orders trump, is he going alone?
    - if bot is ordered up trump and is the dealer, bot needs to choose a card to discard that is not trump
    - bot needs to play a card from hand
    - when playing a card, the bot must play the best card, if he can catch the trick he will play the best card to do so
    - if bot is leading the hand, he will play the highest card in hand

    is_bot(): -- returns status if player is a bot.
    get_player_card(): -- bot evaluates and plays a card from hand.
    going_alone(): -- bot decideds if it will go alone in a hand.
    """
    def __init__(self, name: str):
        """Initialize bot player object. Anything player related should be 
        inherited by the player object that this object is taking place of as they
        should be created first.
        """
        super().__init__(name)
        self._is_bot = True

    def __repr__(self):
        """Return the bot object."""
        return f'Bot player(\'{self._name}\')'

    # public methods
    def is_bot(self):
        """Returns if is a bot."""
        return self._is_bot
    
    def get_player_status(self, *args, **kwargs):
        print('\n')
        print('-' * 40)
        print(f'\tPLAYER: {self._name} \tTEAM: {self._team.get_name()}')
        print('-' * 40)
        print(f'{self._name} is thinking...')
        
    def get_player_card(self, legal_card_list: list[Card]) -> int:
        """Bot evaluates and plays a card from hand. Returns card number to play.
        
        Keyword arguments:
        legal_card_list: -- List of cards able to be played this round.
        """
        if not legal_card_list:
            return
        
        card = self._choose_high_card(legal_card_list)
        return card
    
    def get_call(self, previous_revealed: Card) -> str:
        """Bot decides if it wants to call a trump on second round of bidding.
        Keyword arguments:
        previous_revealed: -- card turned down for trump bidding in last round.
        """
        if not previous_revealed:
            return
        
        trumps = ['Spades', 'Diamonds', 'Clubs', 'Hearts']
        trump_count = {}
        highest = 0

        for card in self._cards:
            if card.get_suit() in trump_count.keys():
                trump_count[card.get_suit()] += 1
            else:
                trump_count[card.get_suit()] = 1

        suit = previous_revealed.get_suit()
        suit_to_call = None
        
        for trump in trumps:
            if trump == suit or trump not in trump_count.keys():
                continue
            if trump_count[trump] > highest:
                highest = trump_count[trump]
                suit_to_call = trump
        
        # If we have 3 or more trumps, we will call that suit, else pass
        # TODO adding more refined decisions if this is working, such as
        #   strength of the trumps in hand, etc.
        if highest >= 3:
            print(f'{self._name} has called {suit_to_call} for trump.')
            return suit_to_call
        print(f'{self._name} has passed in second round.')
        return 'pass'
    
    def get_order(self, revealed: Card) -> str:
        """Evaluates and decides if to order revealed card as trump or not.
        """
        hand_strength = self._calculate_hand_strength(revealed)
        order_value = 75

        if hand_strength >= order_value:
            print(f'{self._name} has ordered {revealed}.')
            return  'order'
        print(f'{self._name} has passed.')
        return 'pass'

    def going_alone(self, trump: Trump) -> bool:
        """Check if bot wants to go alone this round.
        """
        # Calculate hand strength based on card values.
        # alone value is based on 3A + both Bowers
        hand_strength = self._calculate_hand_strength(trump)
        alone_value = 83

        if hand_strength >= alone_value:
            self.set_alone(True)
            partner = self._get_partner()
            self._set_partner_skipped(partner)
            print(f'{self._name} is going alone.')
            return True
        self.set_alone(False)
        print(f'{self._name} is not going alone.')
        return False

    # private methods
    def _choose_high_card(self, card_list: list[tuple [int, Card]]) -> int:
        """Evaluates all the cards, and chooses the highest value card in the list. 
        Returns integer of that card.

        Keyword arguments:
        card_list: -- List of cards able to be played this round.
        """
        highest_card = card_list[0][1]
        highest_card_index = card_list[0][0]
        for card in card_list:
            if card[1].get_value() > highest_card.get_value():
                highest_card_index = card[0]

        return highest_card_index
    
    def _choose_low_card(self, card_list: list[tuple [int, Card]]) -> int:
        """Evaluates and chooses the first low card in the list of cards.
        
        Keyword arguments:
        card_list: -- List of cards able to be chosen to discard.
        """
        print(f'BOT PLAYER {self._name} CHOOSING CARD TO DISCARD...')
        lowest_card = card_list[0][1]
        lowest_card_index = card_list[0][0]
        for card in card_list:
            if card[1].get_value() < lowest_card.get_value():
                lowest_card_index = card[0]

        return lowest_card_index
    
    def _calculate_hand_strength(self, trump):
        """Calculates the strength on hand by adding up the values of each card in hand.

        The values for the cards are temporarily set to be inflated for the purposes of calculation.
        """
        tmp_trump = Trump(trump.get_suit())
        # record the hand values
        tmp_cards = {}
        hand_strength = 0

        for card in self._cards:
            tmp_cards[card.get_id()] = card.get_value() 
            card.is_trump(tmp_trump)
            hand_strength += card.get_value()

        self._reset_card_values(tmp_cards)

        return hand_strength
    
    def _reset_card_values(self, card_values):
        """Reset the cards values."""
        for card in self._cards:
            id = card.get_id()
            value = card_values[id]
            card.reset(value)

    
# Bot player builder
def build_bots(players: list[Player]) -> list[Bot]:
    """Create Bot player objects based on list of Player objects."""
    if not players:
        print("WARNING: NO NAMES OF PLAYER OBJECTS TO CREATE BOTS. EXITING BUILDER.")
        return
    
    bots = [Bot(player.get_name()) for player in players]
    return bots

def find_bots(players: list[Player]):
    bots = []
    for player in players:
        if player.get_name() in BOTS:
            bots.append(player)

    return bots

def replace_players_with_bots(player_list: list[Player], bot_list: list[Bot]):
    '''Replaces Players with Bot Players.'''
    players = player_list.copy()
    bots = bot_list.copy()
    new_list = []

    for player in player_list:
        for bot in bots:
            if player.get_name() == bot.get_name():
                new_list.append(bot)
                bots.remove(bot)
                players.remove(player)
        if player in players:
            new_list.append(player)
        
    return new_list