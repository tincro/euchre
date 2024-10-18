"""The inputs module allows us to get various input from the player."""

from constants import SUITS, BOTS

# Get Player names from the user, otherwise use bots.
def get_players(count):
    """Get player names from the user. Bots are used instead if chosen by the player."""
    names = []
    while True:
        use_bots = input(f'Would you like to use bots? -> ')
        match use_bots:
            case 'yes':
                names = BOTS
                break
            case 'no':
                for i in range(count):
                    name = input(f'Enter a player for Player {i+1}: ')
                    names.append(name)
                break
            case _:
                print('Not Valid Answer')
    return names

def get_order(revealed):
    """Get order from the player. Only acceptable options are 'order' or 'pass'.
    """
    order = None
    while order is None:
        order = input(f'Order {revealed} or pass? ')
        if order.lower() == 'order' or order.lower() == 'pass':
            return order.lower()
        else:
            order = None

def get_call(previous_revealed):
    """Get call from the player. Only acceptable options are 'Hearts', 'Spades', 'Diamonds', or 'Clubs'.
    Player cannot chose the trump that was already bidded.
    """
    print(f'The {previous_revealed} was turned face-down. Second round of bidding...')
    suit = previous_revealed.get_suit().lower()
    call = None
    while call is None:
        call = input("Enter suit ({}) for trump or pass: ".format(', '.join(suit for suit in SUITS)))
        if call.lower() == 'pass':
            return call.lower()
        elif call.lower() != suit:
            if call.capitalize() in SUITS:
                return call.capitalize()
            else:
                call = None
        else:
            call = None

def get_player_card(legal_card_list):
    """Get player input choosing a card from the list in hand. Returns integer. 
    """
    card = None
    while card is None:
        card = input("Choose the number of a card you'd like to play: ")
        if card.isdigit():
            if int(card) <= len(legal_card_list) and int(card) > 0:
                return int(card)
            else:
                card = None    
        else:
            card = None