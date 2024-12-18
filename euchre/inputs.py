"""
Inputs module: allows us to get various input from the player.
""" 
from euchre.constants import BOTS

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




