# This is the main game loop for the Euchre game
from random import sample, choices, shuffle

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

    # Deal random card to each player, until they have 5 cards
    # Each player gets 3 cards, then 2 cards.
    deal_cards(players)
    
    # After each player has 5 cards, there will be 4 cards left over
    # The top card gets revealed

    
    # Start bidding round to determine the trump suit for this hand
    # If no player wants the revealed trump to be trump, it is hidden
    # A second round of bidding starts, and players choose trump from their hand
    # After trump is chosen, the player to dealer's left starts the first trick
    trump = Trump()

    # Each player adds a card to the trick pool until all players have played
    # The highest ranking card wins the trick for this round
    # Play continues until all cards have been played
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
    print("Dealing Cards...")

# Run main game loop
if __name__ == "__main__":
    main()