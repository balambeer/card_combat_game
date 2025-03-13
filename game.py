import pygame as pg
import constants
import menu
from player import *
from point_crawl import *
from combat_encounter import *
from exploration_encounter import *
from encounter_handler import *

class Game:
    # constructor
    def __init__(self, program):
        self.program = program
        
        self.clock = pg.time.Clock()
        self.delta_time = 0
        
        self.encounter_handler = EncounterHandler(self)
        
        self.player = None
        
        self.select_character = menu.SelectCharacter(program)
        self.point_crawl = self.encounter_handler.create_point_crawl(player_start_node = 0)
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
        
    def update(self):
        if self.state == "select_character":
            self.assign_character()

            if not self.player is None:
                self.select_character = None
                self.encounter = self.encounter_handler.create_exploration_encounter(self.point_crawl.get_player_node())
                self.state = "exploration_encounter"
        elif self.state == "point_crawl":
            self.point_crawl.update()
            if self.point_crawl.state == "next_node_selected":
                # additional node-dependent inputs?
                selected_node = self.point_crawl.graph.nodes[self.point_crawl.pressed_node_index]
                if selected_node.encounter_type == "combat":
                    self.encounter = self.encounter_handler.create_combat_encounter(selected_node)
                    self.state = "combat_encounter"
                elif selected_node.encounter_type == "exploration":
                    self.encounter = self.encounter_handler.create_exploration_encounter(selected_node)
                    self.state = "exploration_encounter"
        elif self.state == "combat_encounter":
            self.encounter.update()
            if self.encounter.state == "combat_over":
                if self.encounter.fighter_1.hp <= 0:
                    self.state = "game_over"
                else:
                    self.player.hp = self.encounter.fighter_1.hp
                    self.state = "point_crawl"
                    self.point_crawl.state = "waiting_for_input"
                self.encounter = None
        elif self.state == "exploration_encounter":
            self.encounter.update()
            if self.encounter.state == "exploration_over":
                self.state = "point_crawl"
                self.point_crawl_state = "waiting_for_input"
                self.encounter = None
                
    def draw(self):
        pg.display.flip()
        if self.state == "select_character":
            self.select_character.draw()
        elif self.state == "point_crawl":
            self.point_crawl.draw()
        elif self.state == "combat_encounter":
            self.encounter.draw()
        elif self.state == "exploration_encounter":
            self.encounter.draw()
    
