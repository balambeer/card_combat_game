Design doc
----------

PvP card battler.

- Combatants have the following attributes: HP, Stress (tolerance), Armor(?)
- Goal of the game is to reduce opponent to 0 HP (or take all the cards of the opponent).

Combat:
- Use standard playing cards.
- Trick taking & deckbuilder format.
- Players start with their unique deck (of a fixed size). At the start of a round, each player draws 4 cards into their hand.
- Players alternate leading tricks. The leading player plays a card. The other player must also play a card, matching the suit of the leading card if possible.
- Trick is resolved: Highest value in the suit that led takes the trick. The lowest value card deals damage. Any card with a unique suit in the trick does a special effect.
- Cards taken as part of the trick go to the players discard pile.
- Each player refills their hand to 4 cards. If the draw deck of the player is empty, they form a new draw deck by reshuffling their discard pile.

Implementation steps
--------------------
- try using more desciptive lingo other then "self" when referencing class instances

- Create draw deck, discard pile, play area
- Logic for resolving tricks
- Cards that are buttons as well
- Lay it out on screen