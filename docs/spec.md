# Euchre
Euchre is a fast-paced, trick taking card game usually played with 2 teams of 2 players on each team. It is played with half a deck of 24 cards (9, 10, J, Q, K, A) from a standard deck of playing cards, and all four suits (Spades, Diamonds, Clubs, Hearts). The team with the most tricks at the end of each round gets points, and the first team to 10 points wins.

## Project Overview
### Purpose
Euchre is a project to play a digital version of the the classic card game, Euchre, in a standalone application. This standalone version of the game is a way for me to learn about building software from the ground up.

### Scope
 - The game will support 4 players.
 - 2 teams of 2 players on each team.
 - Highest ranking card in a round of play will score a trick.
 - Team with majority of tricks won in a round will score points.
 - First team to 10 points wins the game.
 - Support for 1 human player and 3 bot players
 - Support for bot players to make their own decisions.

## Functional Requirements
- Teams are randomly assigned.
- Trump card bidding is simulated such as in a real card game.
- Players will bid on cards based on hand structure.
- Players can pass, bid, or call on cards in a round of bidding.
- Cards are dealt.
- Players can play cards.
- AI driven bots will play any non-human player and make decisions based on their hand of cards.
- Players will win tricks (hands) in order to score points for their respective teams.
- Scores are calculated for teams based on which players have the most tricks.
- At least one version of the GUI for the player to interact with the game.

## Feature Wishlist
- Multiple forms of the GUI for player to interact with the game. Console, desktop, or web based GUI.
- Multiplayer game ability to play with local players.
- Network capability to play multiplayer game with non-local players.
- Rewards such as skins for deck of cards, as something fun to add to the game to personalize the game.
- Sound effects, music, and settings controls.

## User Stories
- As a player, I want to ability to add a name of my choosing to represent me.
- As a player, I want to be able to know what the current score is of both teams.
- As a player, I want to be able to know who the current dealer is.
- As a player, I want to be able to know who's turn it currently is.
- As a player, I want 5 cards to be dealt to me in two rounds.
- As a player, I want the ability to choose to order a trump presented or to pass on it to the next player.
- As a player, I want to be able to choose a trump card if the option to call a trump is presented during a round of bidding.
- As a player, I want to be able to see my cards and choose which one to play.
- As a dealer, I want to be able to choose which card I want to discard in a round of bidding when necessary.

## Technical Requirements
- Python v3.10+
- PySide6 for desktop GUI
