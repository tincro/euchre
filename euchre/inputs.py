"""
The inputs module allows us to get various input from the player.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from euchre.cards import Card
    
from euchre.constants import SUITS, BOTS

# Get Player names from the user, otherwise use bots.
def get_players(count: int) -> list[str]:
    """Get player names from the user. Bots are used instead if chosen by the player.
    
    Keyword arguments:
    count: -- Number of players to create.
    """
    if not count:
        return
    
    names = []
    while True:
        use_bots = input(f'Would you like to use generic names? -> ')
        match use_bots.lower():
            case 'yes':
                names = BOTS
                break
            case 'no':
                for i in range(count):
                    name = input(f'Enter a player for Player {i+1}: ')
                    while not name.isalnum():
                        name = input(f'Enter a player for Player {i+1}: ')
                    names.append(name)
                break
            case _:
                print('Not Valid Answer')
    return names

def get_order(revealed: Card) -> str:
    """Get order from the player. Only acceptable options are 'order' or 'pass'.

    Keyword arguments:
    revealed: -- Revealed card from the top of deck.
    """
    if not revealed:
        return
    
    order = None
    while order is None:
        order = input(f'Order {revealed} or pass?: -> ')
        if order.lower() == 'order' or order.lower() == 'pass':
            return order.lower()
        else:
            order = None

def get_call(previous_revealed: Card) -> str:
    """Get call from the player. Only acceptable options are 'Hearts', 'Spades', 'Diamonds', or 'Clubs'.
    Player cannot chose the trump that was already bidded.

    Keyword arguments:
    previous_revealed: -- Revealed card from the top of deck.
    """
    if not previous_revealed:
        return
    
    suit = previous_revealed.get_suit().lower()
    call = None
    while call is None:
        call = input("Enter suit ({}) for trump or pass: -> ".format(', '.join(suit for suit in SUITS)))
        if call.lower() == 'pass':
            return call.lower()
        elif call.lower() != suit:
            if call.capitalize() in SUITS:
                return call.capitalize()
            else:
                call = None
        else:
            call = None
