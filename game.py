import pygame as pg
import constants
from point_crawl import *
from combat_encounter import *

class Game:
    # constructor
    def __init__(self, program):
        self.program = program
        
        # This will live elsewhere in the future
        graph = Graph(nodes = [GraphNode(0, support.XY(50, 50)), GraphNode(1, support.XY(100, 100))],
                      edges = [(0,1)])
        
        self.point_crawl = PointCrawl(program,
                                      graph,
                                      0)
        self.combat_encounter = None
        self.state = "point_crawl"
        
    def update(self):
        if self.state == "point_crawl":
            self.point_crawl.update()
            if self.point_crawl.state == "next_node_selected":
                # additional node-dependent inputs?
                self.combat_encounter = CombatEncounter(self.program)
                self.state = "combat_encounter"
        elif self.state == "combat_encounter":
            self.combat_encounter.update()
            if self.combat_encounter.state == "combat_over":
                if self.combat_encounter.player_1.hp <= 0:
                    self.state = "game_over"
                else:
                    self.state = "point_crawl"
                    self.point_crawl.state = "waiting_for_input"
                self.combat_encounter = None
            
    def draw(self):
        pg.display.flip()
        if self.state == "point_crawl":
            self.point_crawl.draw()
        elif self.state == "combat_encounter":
            self.combat_encounter.draw()
    
