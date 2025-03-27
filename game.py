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
                                 hp = 3,
                                 max_stress = 7,
                         card_list = [(1, "spear"), (2, "spear"), (3, "spear"),
                                      (1, "shield"), (2, "shield"), (3, "shield"),
                                      (1, "trump"), (2, "trump"), (3, "trump")],
                         skill_list = [])
        elif self.select_character.thief_button.is_left_clicked():
            self.player = Player(program = self.program,
                         hp = 3,
                                 max_stress = 5,
                         card_list = [(1, "spear"), (2, "spear"), (3, "spear"),
                                      (1, "mana"), (2, "mana"), (3, "mana"),
                                      (1, "trump"), (2, "trump"), (3, "trump")],
                         skill_list = [])
        elif self.select_character.witch_button.is_left_clicked():
            self.player = Player(program = self.program,
                         hp = 3,
                                 max_stress = 5,
                         card_list = [(1, "mana"), (2, "mana"), (3, "mana"),
                                      (1, "shield"), (2, "shield"), (3, "shield"),
                                      (1, "trump"), (2, "trump"), (3, "trump")],
                         skill_list = [])
            
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
        if self.state == "select_character":
            self.assign_character()

            if not self.player is None:
                self.select_character = None
                self.encounter = self.dungeon_master.create_scene(location_index = self.point_crawl.get_player_node().index,
                                                                  scene_index = 0,
                                                                  player_keywords = self.player.story_keywords)
                self.state = "encounter"
        elif self.state == "point_crawl":
            self.point_crawl.update()
            if self.point_crawl.state == "next_node_selected":
                self.encounter = self.dungeon_master.create_scene(location_index = self.point_crawl.get_player_node().index,
                                                                  scene_index = 0,
                                                                  player_keywords = self.player.story_keywords)
                self.state = "encounter"
        elif self.state == "encounter":
            self.encounter.update()
            if self.encounter.state == "scene_over":
                if self.encounter.scene_type == "fight":
                    if self.encounter.fighter_1.hp <= 0:
                        self.state = "game_over"
                    else:
                        self.player.hp = self.encounter.fighter_1.hp
                        
                if not self.encounter.effect is None:
                    print("resolving encounter effect")
                    self.resolve_scene_effect(self.encounter.effect)
                
                if self.encounter.next_scene < 0:
                    self.state = "point_crawl"
                    self.point_crawl.state = "waiting_for_input"
                    self.encounter = None
                else:
                    self.encounter = self.dungeon_master.create_scene(location_index = self.point_crawl.get_player_node().index,
                                                                      scene_index = self.encounter.next_scene,
                                                                      player_keywords = self.player.story_keywords)
                
    def draw(self):
        pg.display.flip()
        if self.state == "select_character":
            self.select_character.draw()
        elif self.state == "point_crawl":
            self.point_crawl.draw()
        elif self.state == "encounter":
            self.encounter.draw()
    
