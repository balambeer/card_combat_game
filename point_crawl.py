import pygame as pg
import constants
import support

point_crawl_background_color = "burlywood"
point_crawl_edge_color = "black"
point_crawl_node_color = "gray"
point_crawl_node_highlight_color = "orange"
point_crawl_node_pressed_color = "tomato"
point_crawl_player_color = "cornflowerblue"
point_crawl_node_size = int(0.1 * constants.screen_height)
point_crawl_node_rounded_corner_size = int(0.1 * point_crawl_node_size)
point_crawl_player_size = int(0.75 * point_crawl_node_size) // 2

class GraphNode():
    # constructor
    def __init__(self, index, position):
        self.rect = pg.Rect((position.x - point_crawl_node_size // 2,
                             position.y - point_crawl_node_size // 2),
                            (point_crawl_node_size, point_crawl_node_size))
        self.index = index

class Graph():
    # constructor
    def __init__(self, nodes, edges):
        self.nodes = nodes
        self.edges = edges
        
class PointCrawl:
    # constructor
    def __init__(self, program,
                 graph,
                 player_start_node_index):
        self.program = program
        
        self.graph = graph
        
        self.player_node_index = player_start_node_index
        self.active_node_index = None
        self.pressed_node_index = None
        
        self.state = "waiting_for_input"
        
        self.update_nodes()
        
    def get_player_node(self):
        return self.graph.nodes[self.player_node_index]
    
    def update_nodes(self):
        player_position = self.graph.nodes[self.player_node_index].rect.center
        for node in self.graph.nodes:
            offset =(node.rect.center[0] - player_position[0],
                     node.rect.center[1] - player_position[1])
            node.rect.update((constants.screen_half_width + offset[0] - point_crawl_node_size // 2,
                              constants.screen_half_height + offset[1] - point_crawl_node_size // 2),
                             (point_crawl_node_size, point_crawl_node_size))
            
    def update(self):
        self.update_nodes()
        if self.state == "waiting_for_input":
            self.active_node_index = None
            self.pressed_node_index = None
            for i in range(len(self.graph.nodes)):
                if self.graph.nodes[i].rect.collidepoint(pg.mouse.get_pos()):
                    self.active_node_index = i
                    if pg.mouse.get_pressed()[0]:
                        self.pressed_node_index = i
                        self.player_node_index = self.pressed_node_index
                        self.state = "next_node_selected"
        elif not self.pressed_node_index is None:
            self.state = "waiting_for_input"
            self.pressed_node_index = None
        
    def draw(self):
        self.program.screen.fill(point_crawl_background_color)
        
        # edges
        for edge in self.graph.edges:
            pg.draw.line(surface = self.program.screen,
                         color = point_crawl_edge_color,
                         start_pos = self.graph.nodes[edge[0]].rect.center,
                         end_pos = self.graph.nodes[edge[1]].rect.center,
                         width = 2)
        # nodes
        for node in self.graph.nodes:
            pg.draw.rect(surface = self.program.screen,
                         color = point_crawl_node_color,
                         rect = node.rect,
                         border_radius = point_crawl_node_rounded_corner_size)
            pg.draw.rect(surface = self.program.screen,
                         color = point_crawl_edge_color,
                         rect = node.rect,
                         width = 1,
                         border_radius = point_crawl_node_rounded_corner_size)
        # active node
        if not self.active_node_index is None:
            pg.draw.rect(surface = self.program.screen,
                         color = point_crawl_node_highlight_color,
                         rect = self.graph.nodes[self.active_node_index].rect,
                         width = 1,
                         border_radius = point_crawl_node_rounded_corner_size)
        if not self.pressed_node_index is None:
            pg.draw.rect(surface = self.program.screen,
                         color = point_crawl_node_pressed_color,
                         rect = self.graph.nodes[self.pressed_node_index].rect,
                         width = 1,
                         border_radius = point_crawl_node_rounded_corner_size)
        # player
        pg.draw.circle(surface = self.program.screen,
                       color = point_crawl_player_color,
                       center = (constants.screen_half_width, constants.screen_half_height),
                       radius = point_crawl_player_size)
        pg.draw.circle(surface = self.program.screen,
                       color = point_crawl_edge_color,
                       center = (constants.screen_half_width, constants.screen_half_height),
                       radius = point_crawl_player_size,
                       width = 1)
        