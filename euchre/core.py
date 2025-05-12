"""Core.py holds the core functions that run the main game loop."""
from __future__ import annotations
import time
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from euchre.cards import Card
    from euchre.dealers import Dealer
    from euchre.players import Player
    from euchre.trumps import Trump

import euchre.trumps as _trumps
from euchre.constants import DELAY


def bidding_round(players: list[Player], dealer: Dealer, revealed: Card=None, first_round=True) -> Trump|None:
    """Start bidding round for trump card for this round. If revealed is None,
    Players can choose trump from their hand. Returns Trump object.

    Keyword arguments:
    players: -- list of players in this round of bidding.
    revealed: -- the revealed card to start the Trump bidding.
    previous: -- the same as revealed, except cannot be chosen as Trump this round.
    """
    if first_round:
        for player in players:
            delay()
            if not player.is_bot():
                player.get_player_status()
            order = player.get_order(revealed)
            if order == 'order' or order == 'yes':
                trump = _trumps.Trump(revealed.get_suit(), player.get_team())
                if player.is_bot():
                    player.going_alone(trump)
                else:
                    player.going_alone()
                delay()
                dealer.pickup_and_discard(revealed)
                return trump
            elif order == 'pass':
                continue
            else:
                print('ERROR - NOT VALID OPTION.')
    else:
        if not first_round:
            print('\n')
            print(f'The dealer {dealer} turned the {revealed} face-down. Starting second round of bidding...')
            print('\n')

            for player in players:
                delay()
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


def play_cards(players: list[Player], trump: Trump) -> list[tuple[Player, Card]]:
    """Each player plays a card from their hand. Returns tuple list of (player, card played).
    
    Keyword arguments:
    players: -- list of players.
    trump: -- trump for current round.
    """
    cards_played = []
    card_to_match = None
    for player in players:
        # check if player gets skipped because partner alone this round
        if player.get_skipped():
            continue
        delay()
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
        player.remove_card(card_to_play)
        cards_played.append((player, card_to_play))

        print(f'{player.get_name()} played {card_to_play}.')
        space_break()
        space_break()
        print('All cards played:')
        for card in cards_played:
            print(f'\t{card[0]} played {card[1]}')
        
    return cards_played


def reset_round(players: list[Player], dealer: Dealer):
    """Reset Player counters for next round of play.
    
    Keyword arguments:
    players: -- list of players to reset.
    """
    for player in players:
        player.reset()

    dealer.next_dealer() 


def delay():
    """Delay the time between display updates."""
    # Check if we should use time delay on display updates
    if DELAY:
        time.sleep(2)
    else:
        pass

def space_break():
    print('\n')

