from card import Card
from trump import Trump

# 9 thru A in ascending order values of rank, A => 14
VALUES = (9, 10, 11, 12, 13, 14)
SUITS = ("Spades", "Diamonds", "Clubs","Hearts")

DECK = [
    Card(value, suit) for value in VALUES for suit in SUITS
]

def main():
    # Deal random card to each player, until they have 5 cards
    # Each player gets 3 cards, then 2 cards.
    # After each player has 5 cards, there will be 4 cards left over
    # The top card gets revealed

    # Start bidding round to determine the trump suit for this hand
    # If no player wants the revealed trump to be trump, it is hidden
    # A second round of bidding starts, and players choose trump from their hand
    # After trump is chosen, the player to dealer's left starts the first trick
    
    # Each player adds a card to the trick pool until all players have played
    # The highest ranking card wins the trick for this round
    # Play continues until all cards have been played
    # The team with the most tricks wins points for the round
    
    # Assuming the team that wins the points called the trump:
    # 3 tricks wins 1 point, all 5 tricks wins 2 points
    # If a player chooses to go alone this round and wins, 4 points awarded.

    # If the team that wins points did not call trump, 2 points awarded instead
    # The first team to reach 10 points wins the game


if __name__ == "__main__":
    main()