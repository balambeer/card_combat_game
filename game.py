import pygame as pg
import constants
from point_crawl import *
from combat_encounter import *
from exploration_encounter import *

class Game:
    # constructor
    def __init__(self, program):
        self.program = program
        
        # This will live elsewhere in the future
        graph = Graph(nodes = [GraphNode(0, support.XY(50, 50), "exploration", 0),
                               GraphNode(1, support.XY(350, 200), "combat", 1)],
                      edges = [(0,1)])
        
        self.point_crawl = PointCrawl(program,
                                      graph,
                                      0)
        self.encounter = ExplorationEncounter(program = self.program,
                                              encounter_text = "You set out to explore the ruins of Ithar.",
                                              option_1_text = "Go through the gate",
                                              option_2_text = "Turn back",
                                              option_3_text = "Climb the wall",
                                              resolution_options = ["You go through the gate.",
                                                                    "You want to turn back but something compels you to go in.",
                                                                    "You climb through the wall."])
        self.state = "exploration_encounter"
        
    def update(self):
        if self.state == "point_crawl":
            self.point_crawl.update()
            if self.point_crawl.state == "next_node_selected":
                # additional node-dependent inputs?
                selected_node = self.point_crawl.graph.nodes[self.point_crawl.pressed_node_index]
                if selected_node.encounter_type == "combat":
                    self.encounter = CombatEncounter(self.program)
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
                if self.encounter.player_1.hp <= 0:
                    self.state = "game_over"
                else:
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
        if self.state == "point_crawl":
            self.point_crawl.draw()
        elif self.state == "combat_encounter":
            self.encounter.draw()
        elif self.state == "exploration_encounter":
            self.encounter.draw()
    
