"""This is the main game loop for the Euchre game."""

from random import sample

from card import Card
from player import Player
from team import Team
from trump import Trump

# 9 thru A in ascending order values of rank, A => 14
VALUES = (9, 10, 11, 12, 13, 14)
SUITS = ("Spades", "Diamonds", "Clubs", "Hearts")

DECK = [
    Card(value, suit) for value in VALUES for suit in SUITS
]

# PLAYER_COUNT = 4
TEAM_COUNT = 2
CARD_HAND_LIMIT = 5

# TODO Refactor into method to get names from user
names = ["Austin", "Zach", "Alicia", "Sean"]

def main():
    """Main game loop."""
    # Initialize Players
    players = build_players(names)
    
    # Set up teams
    # TODO implement alternate seating for players
    teams = randomize_players(players)
    team_list = build_teams(teams)
    assign_players(team_list)

    # Deal 5 cards to each player and return the top card of the leftover 
    # stack of cards (the kitty in Euchre lingo)
    top_card = deal_cards(players)
        
    # Start bidding round to determine the trump suit for this hand
    # If no player wants the revealed trump to be trump, it is hidden
    # A second round of bidding starts, and players choose trump from their
    # hand. After trump is chosen, the player to dealer's left starts 
    # the first trick
    # TODO need to add trump evaluation functionality of cards
    trump = Trump()

    # TODO handle case for no trump in second round
    bidding_round(players, trump, top_card)
    if trump.get_suit() is None:
        bidding_round(players, trump, None, top_card)
    print(trump)    

    # Each player adds a card to the pool of cards on the table 
    # The team with the most tricks wins points for the round
    # List of cards chosen by each player to play this round.
    cards_played = play_cards(players)
    print(cards_played)

    # For each card played this round, it is only considered if the 
    # suit matches the first card played this round. Otherwise, the card
    # is ignored. The only exception further, is if the card is considered to be
    # matching the current Trump suit. If so, that card is considered highest 
    # ranking card played in the round. Each trump is considered in ranking this way.
    winner = get_highest_rank_card(cards_played)
    print(winner)
    score_trick(winner)

    # Assuming the team that wins the points called the trump:
    # 3 tricks wins 1 point, all 5 tricks wins 2 points
    # If a player chooses to go alone this round and wins, 4 points awarded.

    # If the team that wins points did not call trump, 2 points awarded instead
    # The first team to reach 10 points wins the game

def build_players(names):
    """Create players based on names list."""
    players = [Player(name) for name in names]

    return players

def build_teams(teams_list):
    """Initilize teams with random generated player teams list."""
    print(f'Assigning teams...')
    teams = []
    team_names = ["Red", "Black"]

    for team in zip(team_names, teams_list):
        new_team = Team(team[1][0],team[1][1], team[0])
        print(new_team)
        teams.append(new_team)

    return teams

def assign_players(teams):
    """Assign players to their respective assigned teams."""
    for team in teams:
        for player in team.get_players():
            player.set_team(team)

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
    in the first round, and 2 in the second round then reveals the top 
    card left in the remaining deck.
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

    revealed = shuffled[0]
    print(f'Revealed card to bid for trump: {revealed}')
    return revealed

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
        call = input(f'Enter suit (Spades, Diamonds, Clubs, Hearts) for trump or pass: ')
        if call.lower() == 'pass':
            return call.lower()
        elif call.lower() != suit:
            if call.capitalize() in SUITS:
                return call.capitalize()
            else:
                call = None
        else:
            call = None

def bidding_round(players, trump, revealed=None, previous=None):
    """Bidding round for trump card for this round. If revealed is None,
    Players can choose trump from their hand.
    """
    if revealed is not None:
        for player in players:
            player.get_player_status()
            order = get_order(revealed)
            if order == 'order':
                trump.set_suit(revealed.get_suit())
                return trump
            elif order == 'pass':
                continue
            else:
                print('ERROR - NOT VALID OPTION.')
    else:
        if previous is not None:
            for player in players:
                player.get_player_status()
                call = get_call(previous)
                if call == 'pass':
                    continue
                if call:
                    trump.set_suit(call)
                    return trump
        else:
            print("ERROR - NO PREVIOUS CARD REFERENCED.")

def get_player_card(legal_card_list):
    """Get player input choosing a card from the list in hand.
    Sanitize to confirm card is a valid choice. Returns INT 
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

def play_cards(players):
    """Each player will play a card from their hand. The card will be 
    removed from the respective players hand. Returns tuple list of (player, card played).
    """
    cards_played = []
    for player in players:
        # If a card has been played, we need to filter cards that are legal and
        # is matching the first card's suit in the list
        if len(cards_played) >= 1:
            card_to_match = cards_played[0][1]
            # Filter list of cards in player hand that is legal to play
            # If filtered list returns empty, any card in hand is legal to play
            legal_cards = player.list_cards(player.filter_cards(card_to_match))
            if len(legal_cards) == 0:
                legal_cards = player.list_cards()
        else:
            legal_cards = player.list_cards()
        player.get_player_status(legal_cards)            

        # Subtract 1 from player choice to index properly
        card = (get_player_card(legal_cards) - 1)
        card_hand = legal_cards
        # Get the card from the tuple of the enumerated list
        card_to_play = card_hand[card][1]

        print(f'{player.get_name()} played {card_to_play}.')
        player.play(card_to_play)
        cards_played.append((player, card_to_play))
        
    return cards_played

def get_highest_rank_card(cards):
    """Return the highest ranking card in the list by value. Returns as tuple (player, card)"""
    if not cards:
        print("ERROR - NO CARD TO EVALUATE.")
        return
    # intitialize with first card in tuple list (player, card)
    highest_card = cards[0][1]
    winning_card = cards[0]
    
    for this_card in cards:
        card = this_card[1]
        if card == highest_card:
            continue
        if card.get_value() > highest_card.get_value():
            highest_card = card    
            winning_card = this_card 

    return winning_card

def score_trick(winner):
    """Score the trick for this round increasing winning team trick count."""
    if not winner:
        print("ERROR - NO TRICK TO SCORE.")
        return    
    # increase the trick count by one for this hand for the player
    player = winner[0]
    player.set_tricks()

# Run main game loop
if __name__ == "__main__":
    main()