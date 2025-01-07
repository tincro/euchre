"""
Inputs module: allows us to get various input from the player that affect the
game directly.
""" 
from euchre.constants import BOTS
from random import sample

# Get Player names from the user, otherwise use bots.
def get_players(count: int) -> list[str]:
    """Get player names from the user. Bots are used instead if chosen by the player.
    
    Keyword arguments:
    count: -- Number of players to create.
    """
    if not count:
        return
    
    names = []

    player_name = input(f'Enter your player name: -> ')
    names.append(player_name)
    
    while True:
        use_bots = input(f'Would you like to use bots? -> ')
        match use_bots.lower():
            case 'yes':
                bot_num = input(f'How many bots? -> ')
                while not bot_num.isnumeric():
                    print(f'Please enter a valid number...')
                    bot_num = input(f'How many bots? -> ')
                bot_num = int(bot_num)

                player_num = bot_num + len(names)

                # Get remaining human players before adding bots
                if player_num < count:
                    num = count - player_num
                    names.extend(_enter_players(num))
                
                names.extend(sample(BOTS, bot_num))
                break
            case 'no':
                while len(names) < count:
                    i = len(names)
                    name = input(f'Enter a player for Player {i+1}: ')
                    while not name.isalnum():
                        print(f'Invalid characters used. Please enter alpha numeric characters for name.')
                        name = input(f'Enter a player for Player {i+1}: ')
                    names.append(name)
                break
            case _:
                print('Not a valid answer. Please use \'yes\' or \'no\'.')
    return names

def _enter_players(count: int) -> list[str]:
    players = []
    for i in range(count):
        name = input(f'Enter a name for Player {i+1}: ')
        while not name.isalnum():
            print(f'Invalid characters used. Please enter alpha numeric characters for name.')
            name = input(f'Enter a name for Player {i+1}: ')
        players.append(name)
    return players



