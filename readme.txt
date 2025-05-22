Design doc
----------

PvP card battler.

- Slay the spire or darkest dungeon -like gameplay
- Individual battles are small trick taking games
- Upgrade between levels by gaining new cards and/or unlocking new skills

Gameplay ideas
--------------
- 3 classes (fighter, thief, wizard):
  - play differently in that the gameplay is different: fighter deals damage to hp; thief steals cards when winning tricks; mage casts spells by taking tricks with specific cards

Implementation steps
--------------------
- appearance: change colors, background, add sprites & animations for combatants, change card suits
- readability: animate trick resolution (mark leading card?, mark winning card?)
- juice: sound effects, music, camerea shake, particle effects etc...
- rethink animations (maybe have dodge instead of riposte in some cases)

Systems:
- items (probably a must, potions, antidotes, etc...)
- rewards after combat (i.e. deckbuilding, also a must)
- settings/options menu + rules description (toggler between AI controlled and human controlled opponents)
- build vertical slice demo
- attacks (spells) that bypass defense (poison, chill touch)?

Current stuff
-------------
- demo
  - build map, write stories


Demo story outline
------------------
- Set in a city like that of Thief. Walled off district due to some cataclysm.
- Some patron wants to retrieve an old family heirloom from a mansion. Maybe a dagger/sword or a statue.
- Mansion's rough location available (look at map from Thief 1). Family crest is a chimera. Multiple mansion locations (maybe 3) on the map.
- A pet chimera used to guard the family mansion/vault, still alive (boss).

- Key to the vault?
 - Rogue can break in without a key.
 - Wizard can find a spell scroll to open it.
 - Fighter can find a key on the corpse of a family member (clue to this at the mansion, a note left on the door).

- Location ideas:
 - shrine: healing potion?
 - wizard shop: knock spell scroll
 - blacksmith: armor (+1 to starting defense in encounters)
 - market
 - pub
 - gardens

Testing observations
--------------------

Witch doesn't do any damage