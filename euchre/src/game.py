#!/usr/bin/python3
"""
This is the main game loop for the Euchre game in the GUI version.
This is the main class to control the game logic.
"""
from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.cards import Card
    from src.dealers import Dealer
    from src.players import Player
    from src.trumps import Trump

from docs.constants import (
    MAX_CARD_HAND_LIMIT,
    TEAM_COUNT,
)

from src.cards import Deck
import src.bots as _bots
import src.dealers as _dealers
import src.players as _players
import src.scores as _scores
import src.teams as _teams
import src.titles as _titles
import src.trumps as _trumps

# BUG high ace of lead suit is not counting in ranking, 
#       KH -> diamonds trump, AH played 4 pos

class EuchreGame():

    def __init__(self):
        self.players = None
        self.dealer = None
        self.trump = None
        self.deck = Deck()

    def bidding_round(self, players: list[Player], dealer: Dealer, revealed: Card=None, first_round=True) -> Trump|None:
        """Start bidding round for trump card for this round. If revealed is None,
        Players can choose trump from their hand. Returns Trump object.

        Keyword arguments:
        players: -- list of players in this round of bidding.
        revealed: -- the revealed card to start the Trump bidding.
        previous: -- the same as revealed, except cannot be chosen as Trump this round.
        """
        if first_round:
            for player in players:
                if not player.is_bot():
                    player.get_player_status()
                order = player.get_order(revealed)
                if order == 'order' or order == 'yes':
                    trump = _trumps.Trump(revealed.get_suit(), player.get_team())
                    if player.is_bot():
                        player.going_alone(trump)
                    else:
                        player.going_alone()
                    dealer.pickup_and_discard(revealed)
                    return trump
                elif order == 'pass':
                    continue
                else:
                    print('ERROR - NOT VALID OPTION.')
        else:
            if not first_round:
                print(f'The dealer {dealer} turned the {revealed} face-down. Starting second round of bidding...')

                for player in players:
                    if not player.is_bot():
                        player.get_player_status()
                    call = player.get_call(revealed)
                    if call == 'pass':
                        continue
                    if call:
                        trump = _trumps.Trump(call, player.get_team())
                        if player.is_bot():
                            player.going_alone(trump)
                        else:
                            player.going_alone()
                        return trump
            else:
                print("ERROR - NO PREVIOUS CARD REFERENCED.")
        return None

    def play_cards(self, players: list[Player], trump: Trump) -> list[tuple[Player, Card]]:
        """Each player plays a card from their hand. Returns tuple list of (player, card played).
        
        Keyword arguments:
        players: -- list of players.
        trump: -- trump for current round.
        """
        cards_played = []
        for player in players:
            # check if player gets skipped because partner alone this round
            if player.get_skipped():
                continue
            # If a card has been played, we need to filter cards that are legal and
            # is matching the first card's suit in the list
            if len(cards_played) >= 1:
                card_to_match = cards_played[0][1]
                # Filter list of cards in player hand that is legal to play
                # If filtered list returns empty, any card in hand is legal to play
                legal_cards = player.list_cards(player.filter_cards(card_to_match, trump))
                if len(legal_cards) == 0:
                    legal_cards = player.list_cards()
            else:
                legal_cards = player.list_cards()
            player.get_player_status(legal_cards, trump)            

            # Subtract 1 from player choice to index properly
            card = (player.get_player_card(legal_cards) - 1)

            # Get the card from the tuple of the enumerated list
            card_to_play = legal_cards[card][1]

            print(f'{player.get_name()} played {card_to_play}.')
            player.remove_card(card_to_play)
            cards_played.append((player, card_to_play))
            print('All cards played:')
            for card in cards_played:
                print(f'{card[0]} played {card[1]}')
            
        return cards_played

    # TODO: Possibly need to refactor this into card.py
    def get_highest_rank_card(self, cards: list[tuple[Player, Card]], trump: Trump) -> tuple[Player, Card]:
        """Return the highest ranking Card object in the card list by value. Returns as tuple (player, card).
        
        cards: -- list of tuples of (player, card).
        trump: -- current round Trump object.
        """
        if not cards or not trump:
            print("ERROR - MISSING CARD OR TRUMP.")
            return
        # intitialize with first card in tuple list (player, card)
        first_card = cards[0][1]
        
        highest_card = first_card
        winning_card = cards[0]
        
        for this_card in cards:
            card = this_card[1]
            if card == highest_card:
                # Check for Trump on first card to assign correct value
                card.is_trump(trump)
                continue

            if card.is_trump(trump):
                if card.get_value() > highest_card.get_value():
                    highest_card = card
                    winning_card = this_card

            # Filter out cards that don't match the leading card suit
            elif card.get_suit == first_card.get_suit() and card.get_value() > highest_card.get_value():
                highest_card = card
                winning_card = this_card

        return winning_card

    def reset_round(self, players: list[Player], dealer: Dealer):
        """Reset Player counters for next round of play.
        
        Keyword arguments:
        players: -- list of players to reset.
        """
        for player in players:
            player.reset()

        dealer.next_dealer()    

    # Main game loop for GUI
    def new_game(self):
        """Start a new game of Euchre."""

        # Initialize Bots
        bot_list = _bots.sample_bots()
        bots = _bots.build_bots(bot_list)
        
        # Initialize Players
        # names = _inputs.get_players(PLAYER_COUNT)
        names = ['Player_1']
        names.extend(bots)

        self.players = _players.build_players(names)
        
        # Set up teams
        teams = _teams.randomize_teams(self.players, TEAM_COUNT)
        team_list = _teams.build_teams(teams)
        _teams.assign_player_teams(team_list)
        player_seating = _teams.seat_teams(team_list)

        # Inititialize dealer object for the game to keep track of player positions in turn order
        self.dealer = _dealers.Dealer(player_seating)
        player_order = self.dealer.get_player_order()

        # Run main game loop until a Team has 10 points
        game_over = False
        while game_over is False:
            
            while self.trump is None:
                # Deal 5 cards to each player and return the top card of the leftover 
                # stack of cards (the kitty in Euchre lingo)
                top_card = self.dealer.deal_cards(self.deck)
                    
                # Start bidding round to determine the trump suit for this hand.
                # If no player orders the revealed card to be trump, it is turned face down.
                #
                # A second round of bidding starts, and players may choose trump from their
                # hand. After trump is chosen, the player to dealer's left starts 
                # the first trick.
                #
                # If by the end of the second round of bidding no trump is declared,
                # pass the dealer and repeat.
                self.trump = self.bidding_round(player_order, self.dealer, top_card)
                
                if self.trump is None:
                    self.trump = self.bidding_round(player_order, self.dealer, top_card, False)
                
                if self.trump is None:
                    print(f'Second round of dealing passed.')                
                    self.reset_round(self.players, self.dealer)

            self.trump.print_trump()
            self.trump.get_makers()
            self.trump.print_makers()
            
            # The team with the most tricks wins points for the round
            round = 0
            while round < MAX_CARD_HAND_LIMIT:
                cards_played = self.play_cards(player_order, self.trump)

                # For each card played this round, it is only considered if the 
                # suit matches the first card played this round. Otherwise, the card
                # is ignored. The only exception further, is if the card is considered to be
                # matching the current Trump suit. If so, that card is considered highest 
                # ranking card played in the round. Each trump is considered in ranking this way.
                winner = self.get_highest_rank_card(cards_played, self.trump)
                _scores.score_trick(winner)
                _scores.print_trick_winner(winner)
                _scores.print_tricks(player_order, team_list)
                # set winning player as the new leader for player order
                self.dealer.set_leader(winner[0])
                
                round += 1

            # 3 tricks wins 1 point, all 5 tricks wins 2 points
            # If a player chooses to go alone this round and wins, 4 points awarded.
            _scores.score_round(team_list, self.trump)
            _scores.print_scores(team_list)
            
            game_over = _scores.check_for_winner(team_list)

            # Clean up for next round
            self.reset_round(player_order, self.dealer)

        # The first team to reach 10 points wins the game
        if game_over is not False:
            _titles.congrats(game_over)