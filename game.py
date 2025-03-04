import pygame as pg
import constants
import menu
from player import *
from point_crawl import *
from combat_encounter import *
from exploration_encounter import *

class Game:
    # constructor
    def __init__(self, program):
        self.program = program
        
        self.clock = pg.time.Clock()
        self.delta_time = 0
        
        # This will live elsewhere in the future
        graph = Graph(nodes = [GraphNode(0, support.XY(50, 50), "exploration", 0),
                               GraphNode(1, support.XY(350, 200), "combat", 1)],
                      edges = [(0,1)])
        
        self.player = None
        
        self.select_character = menu.SelectCharacter(program)
        self.point_crawl = PointCrawl(program,
                                      graph,
                                      0)
        self.encounter = None
        self.state = "select_character"
        
    def update(self):
        if self.state == "select_character":
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
                
            if not self.player is None:
                self.select_character = None
                self.state = "exploration_encounter"
                self.encounter = ExplorationEncounter(program = self.program,
                                                          encounter_text = "You set out to explore the ruins of Ithar. Some more text to force multiple lines. Even more and more and more... And some more even, maybe we can even get to three lines if we're lucky.",
                                                          option_1_text = "Go through the gate",
                                                          option_2_text = "Turn back",
                                                          option_3_text = "Climb the wall",
                                                          resolution_options = ["You go through the gate. Let's try to force this to be in multiple lines as well. I'll write another sentence just to make sure that it goes to multiple lines. Should be enough now.",
                                                                                "You want to turn back but something compels you to go in.",
                                                                                "You climb through the wall."])
        elif self.state == "point_crawl":
            self.point_crawl.update()
            if self.point_crawl.state == "next_node_selected":
                # additional node-dependent inputs?
                selected_node = self.point_crawl.graph.nodes[self.point_crawl.pressed_node_index]
                if selected_node.encounter_type == "combat":
                    player_fighter = Fighter(game = self,
                                             is_left_player = True,
                                             is_human_controlled = True,
                                             hp = self.player.hp,
                                             max_stress = self.player.max_stress,
                                             card_list = self.player.card_list,
                                             show_hand = True,
                                             color = "cornflowerblue")
                    enemy_fighter = Fighter(game = self,
                                            is_left_player = False,
                                            is_human_controlled = False,
                                            hp = 3,
                                            max_stress = 7,
                                            card_list = [(1, "spear"), (2, "spear"), (3, "spear"),
                                                         (1, "mana"), (2, "mana"), (3, "mana"),
                                                         # (1, "shield"), (2, "shield"), (3, "shield"),
                                                         (1, "trump"), (2, "trump"), (3, "trump")],
                                            show_hand = False,
                                            color = "tomato")
                    self.encounter = CombatEncounter(self.program,
                                                     player = player_fighter,
                                                     enemy = enemy_fighter)
                    self.state = "combat_encounter"
                elif selected_node.encounter_type == "exploration":
                    self.encounter = ExplorationEncounter(program = self.program,
                                                          encounter_text = "You set out to explore the ruins of Ithar.",
                                                          option_1_text = "Go through the gate",
                                                          option_2_text = "Turn back",
                                                          option_3_text = "Climb the wall",
                                                          resolution_options = ["You go through the gate.",
                                                                                "You want to turn back but something compels you to go in.",
                                                                                "You climb through the wall."])
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
    
