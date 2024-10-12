# This is the main game loop for the Euchre game
from random import sample
from collections import deque

from card import Card
from trump import Trump
from player import Player
from team import Team

# 9 thru A in ascending order values of rank, A => 14
VALUES = (9, 10, 11, 12, 13, 14)
SUITS = ("Spades", "Diamonds", "Clubs","Hearts")

DECK = [
    Card(value, suit) for value in VALUES for suit in SUITS
]

# PLAYER_COUNT = 4
TEAM_COUNT = 2

# TODO Refactor into method to get names from user
names = ["Austin", "Zach", "Alicia", "Sean"]
# players = [Player(name) for name in names]

def main():
    """Main game loop."""
    # Initialize Players
    players = build_players(names)
    
    # Set up teams
    teams = randomize_players(players)
    team_list = build_teams(teams)

    # Deal 5 cards to each player and return the top card of the leftover stack
    top_card = deal_cards(players)
        
    # Start bidding round to determine the trump suit for this hand
    # If no player wants the revealed trump to be trump, it is hidden
    # A second round of bidding starts, and players choose trump from their hand
    # After trump is chosen, the player to dealer's left starts the first trick
    trump = Trump()

    bidding_round(players, trump, top_card)
    print(trump)
    

    # Each player adds a card to the pool of cards on the table 
    # The team with the most tricks wins points for the round
    
    # Assuming the team that wins the points called the trump:
    # 3 tricks wins 1 point, all 5 tricks wins 2 points
    # If a player chooses to go alone this round and wins, 4 points awarded.

    # If the team that wins points did not call trump, 2 points awarded instead
    # The first team to reach 10 points wins the game
    pass

def build_players(names):
    """Create players based on names list"""
    players = [Player(name) for name in names]

    return players

def build_teams(teams_list):
    """Initilize teams with random generated player teams list"""
    teams = []
    team_names = ["Red", "Black"]
    for team in zip(team_names, teams_list):
        new_team = Team(team[1][0],team[1][1], team[0])
        teams.append(new_team)

    return teams
    
def randomize_players(players):
    """Randomize the players and put them into a team and return the list."""
    copy = players.copy()
    player_count = 2
    teams = []

    for _ in range(TEAM_COUNT):
        members = sample(copy, player_count)

        for member in members:
            copy.remove(member)

        teams.append(members)

    return teams

def deal_cards(players):
    """Shuffles the deck and deals cards to players in two rounds. 3 cards
    in the first round, and 2 in the second round.
    """
    print("Dealing Cards...")
    shuffled = sample(DECK, len(DECK))
    rounds = 0
    cards_to_deal = 3
    
    while rounds < 2:
        for player in players:
            cards_dealt = shuffled [0:cards_to_deal]
            
            for card in cards_dealt:
                shuffled.remove(card)
                player.receive_card(card)
                    
        rounds += 1
        cards_to_deal -= 1

    return shuffled[0]

def get_order(revealed):
    """Get order from the player. Only acceptable options are order or pass.
    """
    order = None
    while order is None:
        order = input(f'Order {revealed} or pass? ')
        if order.lower() == 'order' or order.lower() == 'pass':
            return order.lower()
        else:
            order = None

def bidding_round(players, trump, revealed=None):
    """Bidding round for trump card for this round. If revealed is None,
    Players can choose trump from their hand.
    """
    if revealed is not None:
        for player in players:
            print(f'{player.get_name()}')
            print(f'{player.get_cards()}')
            order = get_order(revealed)
            if order == 'order':
                trump.set_suit(revealed.get_suit())
                return trump
            elif order == 'pass':
                continue
            else:
                print('ERROR - NOT VALID OPTION.')
        #   if player wants trump, revealed = trump.suit
        #   else next player chooses
        # if none want trump, return

    #else:
        # for player in players
        # player chooses trump in hand or passes to next player
        pass


# Run main game loop
if __name__ == "__main__":
    main()