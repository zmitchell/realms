========
Gameplay
========

Rules
=====

The goal of the game is to defeat the other players by reducing their health to zero. Every player starts out with 50 health. You reduce a player's health by attacking him with your ships and/or bases. Every player begins with the same deck consisting of some cards which provide money and basic attacks. As you progress you will use your cards to buy better and better cards. You can read more about how to play at the `Star Realms site <https://www.starrealms.com/learn-to-play/>`_, although our rules will differ slightly and this game is in no way affiliated with Star Realms.

Walkthrough
===========

When implementing the game logic, it's helpful to have an idea of the details that take place during the course of the game. To that end, the minute details of what happens during a game have been fleshed out and provided for your convenience.

Start a game
------------
* N players join the game
* A list of players is created

    * N players are created
    * Health is initialized to 50
    * The player is given a UUID
    * Each player constructs their deck

        * 8 scouts, 2 vipers

* Each player shuffles their deck
* Shuffle the list of players
* The main deck is constructed

    * The deck is populated from the repository

* The trade row is drawn

    * 5 cards

* Explorers are made available

One turn
--------

* The current player is set to the player at the head of the list
* Any pending effects targeting the current player are triggered

    * Each player will have a queue of pending effects

* The current player draws his hand

    * The number of cards to draw is determined (N cards)
    * The player’s deck produces a Hand object

        * The deck object draws up to N cards from the undrawn stack
        * If the undrawn stack contains fewer than N cards, the discard pile is shuffled and added to the undrawn pile
        * The remaining cards are drawn from the undrawn pile

* A list of the player’s active cards is created

    * The existing bases and the cards from the hand go into one list of active cards

* Card effects are aggregated from the active cards

    * The first pass over the active cards pulls out the effects that are not ally abilities
    * A second pass over the active cards pulls out the active ally abilities

        * A pass over the list of active cards determines which factions occur more than once

            * This determines which ally abilities to trigger

        * The factions that occur more than once are placed in a list of active factions
        * A pass over the list of active cards pulls out ally abilities belonging to cards whose factions are in the active factions list

* All of the money effects are totaled
* The player’s budget is set to the money total
* The list of active cards and effects are presented to the user

    * Card 1

        * Effect A
        * Effect B
        * etc

    * Card 2

        * Effect A
        * etc

    * etc

* The player makes choices

    * The player chooses cards to buy

        * The player is presented with a numbered list of cards in the trade row (including Explorers)
        * A dictionary is constructed mapping the numbers to the cards’ UUIDs
        * The player chooses a number
        * The UUID of the card is obtained from the dictionary
        * The cost of the card is compared to the player’s budget

            * If the card costs more than the player has, the transaction is rejected

        * The cost of the card is subtracted from the player’s budget
        * If the player bought an Explorer

            * An Explorer is added to the player’s discard pile

        * If the player did not buy an explorer

            * The card is removed from the trade row
            * The card is added to the player’s discard pile
            * A new card is drawn from the main deck
            * The new card is added to the trade row

    * The player chooses effects to apply ( Card 1A, 2C, etc)

        * combat

            * The player is presented with a numbered list of opponents
            * A dictionary is constructed mapping the numbers to the opponents’ UUIDs
            * The player chooses a number
            * The UUID of the target is obtained from the dictionary
            * The damage is applied to the player whose UUID matches that of the target chosen by the player

        * acquire

            * The player is presented with a numbered list of cards in the trade row
            * A dictionary is constructed mapping the numbers to the cards’ UUIDs
            * The player chooses a number
            * The chosen card is removed from the trade row and placed on top of the player’s discard pile
            * A new card is drawn from the main deck and placed in the trade row

        * discard

            * The player is presented with a numbered list of opponents
            * A dictionary is constructed mapping the numbers to the opponents’ UUIDs
            * The player chooses a number
            * The UUID of the target is obtained from the dictionary
            * A discard effect is added to the target’s pending effects queue

        * money

            * The value is added to the player’s budget

        * scrap

            * The player is presented with a numbered list of unplayed cards in their hand and the cards in their discard pile
            * A dictionary is constructed mapping the numbers to the UUIDs of the cards
            * The player chooses a number
            * The UUID of the card is obtained from the dictionary
            * The card with the UUID is permanently removed from the player’s deck

        * heal

            * The player’s health is increased by the value of the effect

        * draw

            * The player draws the specified number of cards from the undrawn pile
            * The cards are added to the player’s hand
            * Effects are extracted from the new cards
            * Ally abilities are analyzed again

    * The player chooses to end his turn

* The player is moved to the end of the list of players

Combat
------

* The player chooses a target

    * The player is presented with a numbered list of opponents
    * A dictionary is constructed mapping the numbers to the opponents’ UUIDs
    * The player chooses a number
    * The UUID of the target is obtained from the dictionary

* The player chooses how to deal damage

    * If the opponent has an outpost, damage is applied there first
    * If the opponent doesn’t have an outpost, the player chooses where to deal damage

        * Opponent’s health
        * Opponent’s other bases

    * If the player destroys a base, it is moved to the opponent’s discard pile
    * If the player reduces the opponent’s health to zero, the opponent is removed from the list of active players
