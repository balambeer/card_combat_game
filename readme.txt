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
- readability: animate trick resolution & damage
- juice: sound effects, camerea shake, particle effects etc...
- rename settings to constants
- add settings/options menu
- handle whos players turn it is (done but maybe can be done better?)
- enable playing against computer

Current stuff
-------------
- Animate sliding cards: better handle animation control...