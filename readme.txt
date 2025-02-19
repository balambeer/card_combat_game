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
- battle over screen (once final animation is done, print sg like "left click to exit" on the screen?).
- juice: sound effects, camerea shake, particle effects etc...
- rename settings to constants
- add settings/options menu
- add point-crawl and wrap the combat/exploration into that structure...

Current stuff
-------------
- Rename files & modules