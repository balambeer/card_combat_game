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

Systems:
- rewards after combat
- multiple character classes, skills/items
- settings/options menu + rules description
- animate point-crawl
- build vertical slice demo
- redefine game structure (random encounters while traveling, mix of story + combat encounters at locations)
- rename/redefine stress to defense (s.t. it's decreasing)

Current stuff
-------------
- Redefine game structure
  - Build a 3 node mini-setup
  - Point crawl: must move to a different & neighboring location
