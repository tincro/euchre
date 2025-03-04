"""Module for holding the logic for the computer bot players.


"""
from random import sample

from euchre.constants import BOTS
from euchre.model.cards import Card, Trump
from euchre.model.players import Player

# The base Bot class
class Bot(Player):
    """The base class for the computer bot Players.
    
    The bot players are activated when there are less than 4 human players.
    They have the same functionality for the player, with the exception that 
    the bot can play the hands for the non-human players in the game. There
    can be as many bot players as necessary.

    is_bot(): -- returns status if player is a bot.
    get_player_card(): -- bot evaluates and plays a card from hand.
    going_alone(): -- bot decideds if it will go alone in a hand.
    """
    # The number of bots in the game.
    bot_count = 0

    def __init__(self, name: str):
        """Initialize bot player object. Anything player related should be 
        inherited by the player object that this object is taking place of as they
        should be created first.
        """
        super().__init__(name)
        Bot.bot_count += 1
        self._is_bot = True
        self._position = None
        self.display_msg = None

    def __repr__(self):
        """Return the bot object."""
        return f'Bot player(\'{self._name}\')'

    # public methods
    def is_bot(self):
        """Returns if is a bot."""
        return self._is_bot
    
    def get_player_status(self):
        print('\n')
        print('-' * 40)
        print(f'\tPLAYER: {self._name} \tTEAM: {self._team.name}')
        print('-' * 40)
        print(f'{self._name} is thinking...')

    def receive_card(self, card: Card):
        """Add the received card to the bot player's hand of cards."""
        self._cards.append(card)
        
    def get_player_card(self) -> int:
        """Bot evaluates and plays a card from hand. Returns card index to play.
        
        Keyword arguments:
        legal_card_list: -- List of cards able to be played this round.
        """        
        card_index = self._choose_high_card(self.filtered_cards)
        return card_index
    
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
            if card.suit in trump_count.keys():
                trump_count[card.suit] += 1
            else:
                trump_count[card.suit] = 1

        suit = previous_revealed.suit
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
            msg = f'{self._name} has called {suit_to_call} for trump.\n'
            print(msg)
            self.display_msg = msg
            self.bid_call = suit_to_call
        else:
            msg = f'{self._name} has passed in second round.\n'
            print(msg)
            self.display_msg = msg
            self.bid_call = 'pass'
    
    def get_order(self, revealed: Card) -> str:
        """Evaluates and decides if to order revealed card as trump or not.
        """
        hand_strength = self._calculate_hand_strength(revealed)
        order_value = 75

        if hand_strength >= order_value:
            msg = f'{self._name} has ordered {revealed}.'
            print(msg)
            self.display_msg = msg
            self.bid_order = 'order'
        else:
            msg = f'{self._name} has passed.'
            print(msg)
            self.display_msg = msg
            self.bid_order = 'pass'

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
            msg = f'{self._name} is going alone.'
            print(msg)
            self.display_msg = msg
            return True
        self.set_alone(False)
        msg = f'{self._name} is not going alone.'
        print(msg)
        self.display_msg = msg
        return False

    def discard(self):
        """Bot player to discard a card of their choosing."""
        # Update filtered cards list
        self.list_cards()

        # Subtract 1 from player choice to index properly
        discard = (self._choose_low_card(self.filtered_cards) - 1)
        # Get the card from the tuple of the enumerated list
        card_to_discard = self.filtered_cards[discard][1]
        self.remove_card(card_to_discard)

    # private methods
    def _choose_high_card(self, legal_card_list: list[tuple [int, Card]]=None) -> int:
        """Evaluates all the cards, and chooses the highest value card in the list. 
        Returns integer of that card.

        Keyword arguments:
        card_list: -- List of cards able to be played this round.
        """
        if not legal_card_list:
            card_list = self.list_cards()
        else:
            card_list = legal_card_list

        highest_card = card_list[0][1]
        highest_card_index = card_list[0][0]
        for card in card_list:
            if card[1].value > highest_card.value:
                highest_card_index = card[0]

        return highest_card_index
    
    def _choose_low_card(self, card_list: list[tuple [int, Card]]) -> int:
        """Evaluates and chooses the first low card in the list of cards.
        
        Keyword arguments:
        card_list: -- List of cards able to be chosen to discard.
        """
        msg = f'{self._name} CHOOSING CARD TO DISCARD...'
        print(msg)
        self.display_msg = msg.lower()

        lowest_card = card_list[0][1]
        lowest_card_index = card_list[0][0]
        for card in card_list:
            if card[1].value < lowest_card.value:
                lowest_card_index = card[0]

        return lowest_card_index
    
    def _calculate_hand_strength(self, trump):
        """Calculates the strength on hand by adding up the values of each card in hand.

        The values for the cards are temporarily set to be inflated for the purposes of calculation.
        """
        tmp_trump = Trump(trump.suit)
        # record the hand values
        tmp_cards = {}
        hand_strength = 0

        for card in self._cards:
            tmp_cards[card.id] = card.value 
            card.is_trump(tmp_trump)
            hand_strength += card.value

        self._reset_card_values(tmp_cards)

        return hand_strength
    
    def _reset_card_values(self, card_values):
        """Reset the cards values."""
        for card in self._cards:
            id = card.id
            value = card_values[id]
            card.reset(value)

    
# Bot player builder
def build_bots(bot_names: list[str]) -> list[Bot]:
    """Create Bot player objects based on list of Player objects."""
    if not bot_names:
        print("WARNING: NO STRINGS OF NAMES TO CREATE BOTS. EXITING BUILDER.")
        return
    
    bots = [Bot(name) for name in bot_names]
    return bots

def sample_bots(bot_num: int=3) -> list[str]:
    """Sample 3 random bot names and return them."""
    # bot_num = 3
    bots = sample(BOTS, bot_num)

    return bots

def find_bots(players: list[Player]):
    bots = []
    for player in players:
        if player.name in BOTS:
            bots.append(player)

    return bots

def replace_players_with_bots(player_list: list[Player], bot_list: list[Bot]):
    '''Replaces Players with Bot Players.'''
    players = player_list.copy()
    bots = bot_list.copy()
    new_list = []

    for player in player_list:
        for bot in bots:
            if player.name == bot.name:
                new_list.append(bot)
                bots.remove(bot)
                players.remove(player)
        if player in players:
            new_list.append(player)
        
    return new_list