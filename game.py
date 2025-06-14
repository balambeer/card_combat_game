import pygame as pg
import constants
import menu
from player import *
from point_crawl import *
from fight_scene import *
from story_scene import *
from dungeon_master import *

class Game:
    # constructor
    def __init__(self, program):
        self.program = program
        
        self.clock = pg.time.Clock()
        self.delta_time = 0
        
        self.dungeon_master = DungeonMaster(self)
        
        self.player = None
        
        self.select_character = menu.SelectCharacter(program)
        self.point_crawl = self.dungeon_master.create_point_crawl(player_start_node = 0)
        self.encounter = None
        self.state = "select_character"
        
    def assign_character(self):
        if self.select_character.heretic_button.is_left_clicked():
            self.player = Player(program = self.program,
                                 name = "heretic",
                                 hp = 3,
                                 max_defense = 7,
                                 armor = 0,
#                                  card_list = [(1, "spear", None), (2, "spear", None), (3, "spear", None),
#                                               (1, "shield", None), (2, "shield", None), (3, "shield", None),
#                                               (1, "trump", None), (2, "trump", None), (3, "trump", None)],
                                 card_list = [(1, "spear", None), (2, "spear", None), (3, "spear", None),
                                              (1, "shield", None), (2, "shield", None),
                                              (1, "trump", None), (2, "trump", None),
                                              (3, "mana", "rage")],
                                 skill_list = [],
                                 story_keywords = ["heretic"])
        elif self.select_character.thief_button.is_left_clicked():
            self.player = Player(program = self.program,
                                 name = "thief",
                                 hp = 3,
                                 max_defense = 5,
                                 armor = 0,
                                 card_list = [(1, "shield", None), (2, "spear", None),
                                              (1, "shield", None), (2, "shield", None), (3, "shield", None),
                                              (2, "mana", "hide"),
                                              (1, "trump", None), (1, "trump", None)],
                                 skill_list = [],
                                 story_keywords = ["thief"])
        elif self.select_character.witch_button.is_left_clicked():
            self.player = Player(program = self.program,
                                 name = "witch",
                                 hp = 3,
                                 max_defense = 5,
                                 armor = 0,
                                 card_list = [(2, "mana", "mage armor"), (2, "mana", "weakness"), (1, "mana", "bolt"),
                                              (1, "shield", None), (2, "shield", None),
                                              (1, "spear", None),
                                              (1, "trump", None), (2, "trump", None)],
                                 skill_list = [],
                                 story_keywords = ["witch"])
            
    def resolve_scene_effect(self, effect):
        effect_type_and_value = effect.split(":")
        if effect_type_and_value[0] == "gain_keyword":
            self.player.gain_keyword(effect_type_and_value[1])
            print("player gained keyword " + effect_type_and_value[1])
        elif effect_type_and_value[0] == "lose_keyword":
            self.player.lose_keyword(effect_type_and_value[1])
        elif effect_type_and_value[0] == "take_damage":
            self.player.hp -= int(effect_type_and_value[1])
        elif effect_type_and_value[0] == "heal":
            self.player.hp += int(effect_type_and_value[1])
        elif effect_type_and_value[0] == "gain_skill":
            self.player.gain_skill(effect_type_and_value[1])
        
    def update(self):
        self.delta_time = self.clock.tick(constants.fps)
        
        if self.state == "select_character":
            self.assign_character()

            if not self.player is None:
                self.select_character = None
                self.encounter = self.dungeon_master.create_scene(scene_library = self.dungeon_master.scene_library,
                                                                  location_index = self.point_crawl.get_player_node().index,
                                                                  scene_index = 0,
                                                                  player_keywords = self.player.story_keywords)
                self.state = "encounter"
        elif self.state == "point_crawl":
            self.point_crawl.update()
            if self.point_crawl.state == "arrived_at_new_location":
                self.encounter = self.dungeon_master.create_scene(scene_library = self.dungeon_master.scene_library,
                                                                  location_index = self.point_crawl.get_player_node().index,
                                                                  scene_index = 0,
                                                                  player_keywords = self.player.story_keywords)
                self.state = "encounter"
            elif self.point_crawl.state == "travel_encounter":
                self.encounter = self.dungeon_master.create_travel_encounter_scene(area_index = self.point_crawl.get_player_node().area,
                                                                                   player_keywords = self.player.story_keywords)
                self.state = "travel_encounter"
        elif self.state == "encounter" or self.state == "travel_encounter":
            self.encounter.update(self.player.story_keywords)
            if self.encounter.state == "scene_over":
                if self.encounter.scene_type == "fight":
                    if self.encounter.fighter_1.hp <= 0:
                        self.state = "game_over"
                    else:
                        self.player.hp = self.encounter.fighter_1.hp
                        
                if not self.state == "game_over":
                    if not self.encounter.effect is None:
                        print("resolving encounter effect")
                        self.resolve_scene_effect(self.encounter.effect)
                    
                    next_scene_index = self.dungeon_master.find_next_scene_index(self.encounter.next_scene_options,
                                                                                 self.player.story_keywords)
                    if next_scene_index < 0:
                        self.state = "point_crawl"
                        self.encounter = None
                    elif self.state == "encounter":
                        self.encounter = self.dungeon_master.create_scene(scene_library = self.dungeon_master.scene_library,
                                                                          location_index = self.encounter.scene_location, # self.point_crawl.get_player_node().index,
                                                                          scene_index = next_scene_index,
                                                                          player_keywords = self.player.story_keywords)
                    elif self.state == "travel_encounter":
                        self.encounter = self.dungeon_master.create_scene(scene_library = self.dungeon_master.travel_encounters,
                                                                          # I need the location which was selected upon creation of the travel encounter
                                                                          location_index = self.encounter.scene_location, # 0,
                                                                          scene_index = next_scene_index,
                                                                          player_keywords = self.player.story_keywords)
                
    def draw(self):
        pg.display.flip()
        if self.state == "select_character":
            self.select_character.draw()
        elif self.state == "point_crawl":
            self.point_crawl.draw()
        elif self.state == "encounter" or self.state == "travel_encounter":
            self.encounter.draw()
    
