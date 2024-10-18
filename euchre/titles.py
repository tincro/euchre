"""The titles module contains display functions."""

# Print the title screen for the game
def title():
    print('-' * 40)
    print(f'\t\tEUCHRE')
    print('-' * 40)
    print(f'Welcome to the classic card game of Euchre!')
    print('\n')

# Congratulate the winners of the game
def congrats(team):
    """Congratulate the winners for a great game!"""
    players = team.get_players()
    print(f'Team {team.get_name()} HAS WON THE GAME! CONGRATULATIONS {players[0]} and {players[1]}!')
    