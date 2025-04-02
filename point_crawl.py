import pygame as pg
import constants
import support
import math

point_crawl_background_color = "burlywood"
point_crawl_edge_color = "black"
point_crawl_node_color = "gray"
point_crawl_node_highlight_color = "orange"
point_crawl_node_pressed_color = "tomato"
point_crawl_player_color = "cornflowerblue"
point_crawl_node_size = int(0.1 * constants.screen_height)
point_crawl_node_rounded_corner_size = int(0.1 * point_crawl_node_size)
point_crawl_player_size = int(0.75 * point_crawl_node_size) // 2
point_crawl_player_v_per_ms = constants.screen_height / 2000

class GraphNode():
    # constructor
    def __init__(self, index, position):
        self.rect = pg.Rect((position.x - point_crawl_node_size // 2,
                             position.y - point_crawl_node_size // 2),
                            (point_crawl_node_size, point_crawl_node_size))
        self.index = index
        
class GraphEdge():
    def __init__(self, nodes, junctions_list):
        self.node_indexes = (nodes[0].index, nodes[1].index)
        self.junction_positions = [ nodes[0].rect.center ] + junctions_list + [ nodes[1].rect.center ]
        self.n_segments = 1 + len(junctions_list)


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
        
        self.neighbor_node_indexes = self.find_neighbors()
        self.active_node_index = None
        self.pressed_node_index = None
        
        self.player_traveling_edge = None
        self.player_traveling_segment = None
        self.player_traveling_forward = None
        
        self.state = "waiting_for_input"
        
        self.player_position = self.graph.nodes[self.player_node_index].rect.center
        self.center_camera_on_player()
        
    def get_player_node(self):
        return self.graph.nodes[self.player_node_index]
    
    def find_neighbors(self):
        neighbors = []
        for edge in self.graph.edges:
            if edge.node_indexes[0] == self.player_node_index:
                if not edge.node_indexes[1] in neighbors:
                    neighbors.append(edge.node_indexes[1])
            if edge.node_indexes[1] == self.player_node_index:
                if not edge.node_indexes[0] in neighbors:
                    neighbors.append(edge.node_indexes[0])
                    
        return neighbors
    
    def convert_to_screen_position(self, obj_position):
        offset = (obj_position[0] - self.camera_center[0],
                  obj_position[1] - self.camera_center[1])
        
        return (constants.screen_half_width + offset[0],
                constants.screen_half_height + offset[1])
    
    def center_camera_on_player(self):
        self.camera_center = self.player_position

        for node in self.graph.nodes:
            screen_pos = self.convert_to_screen_position(node.rect.center)
            node.rect.update((screen_pos[0] - point_crawl_node_size // 2,
                              screen_pos[1] - point_crawl_node_size // 2),
                             (point_crawl_node_size, point_crawl_node_size))
            
        for edge in self.graph.edges:
            edge.junction_positions = [ self.convert_to_screen_position(position) for position in edge.junction_positions ]
            
        self.player_position = self.convert_to_screen_position(self.player_position)
         
    def find_traveling_edge(self):
        traveling_on_edge = None
        for edge in self.graph.edges:
            if ((edge.node_indexes[0] == self.player_node_index and edge.node_indexes[1] == self.pressed_node_index) or
                (edge.node_indexes[1] == self.player_node_index and edge.node_indexes[0] == self.pressed_node_index)):
                traveling_on_edge = edge
                break
        return traveling_on_edge
                    
    def update_player_position(self):
        if not self.player_traveling_edge is None:
            if self.player_traveling_segment <= self.player_traveling_edge.n_segments:
                if self.player_traveling_forward:
                    traveling_from = self.player_traveling_edge.junction_positions[self.player_traveling_segment - 1]
                    traveling_to = self.player_traveling_edge.junction_positions[self.player_traveling_segment]
                else:
                    traveling_from = self.player_traveling_edge.junction_positions[-self.player_traveling_segment]
                    traveling_to = self.player_traveling_edge.junction_positions[-(self.player_traveling_segment + 1)]
                d = math.sqrt((traveling_to[0] - traveling_from[0]) ** 2 + (traveling_to[1] - traveling_from[1]) ** 2)
                n_steps = d / (point_crawl_player_v_per_ms * self.program.game.delta_time)
                position_increment = ((traveling_to[0] - traveling_from[0]) / n_steps,
                                      (traveling_to[1] - traveling_from[1]) / n_steps)

#                 angle = math.atan((traveling_to[1] - traveling_from[1]) / (traveling_to[0] - traveling_from[0]))
#                 v = point_crawl_player_v_per_ms * self.program.game.delta_time
#                 position_increment = (int(v * math.cos(angle)), (v * math.sin(angle)))
                
                self.player_position = (self.player_position[0] + position_increment[0],
                                        self.player_position[1] + position_increment[1])
                
                # snap to location
                if ((traveling_to[0] >= traveling_from[0] and self.player_position[0] >= traveling_to[0]) or
                    (traveling_to[0] < traveling_from[0] and self.player_position[0] <= traveling_to[0])):
                    self.player_position = (traveling_to[0], self.player_position[1])
                if ((traveling_to[1] >= traveling_from[1] and self.player_position[1] >= traveling_to[1]) or
                    (traveling_to[1] < traveling_from[1] and self.player_position[1] <= traveling_to[1])):
                    self.player_position = (self.player_position[0], traveling_to[1])
                    
                if self.player_position[0] == traveling_to[0] and self.player_position[1] == traveling_to[1]:
                    self.player_traveling_segment += 1
            else:
                self.player_node_index = self.pressed_node_index
                self.player_traveling_edge = None
                self.player_traveling_segment = None
                self.player_traveling_forward = None
                self.center_camera_on_player()
                self.neighbor_node_indexes = self.find_neighbors()
                self.state = "arrived_at_new_location"
            
    def update(self):
        if self.state == "waiting_for_input":
            self.active_node_index = None
            self.pressed_node_index = None
            for i in self.neighbor_node_indexes:
                if self.graph.nodes[i].rect.collidepoint(pg.mouse.get_pos()):
                    self.active_node_index = i
                    if pg.mouse.get_pressed()[0]:
                        self.pressed_node_index = i
                        self.player_traveling_edge = self.find_traveling_edge()
                        self.player_traveling_segment = 1
                        self.player_traveling_forward = (self.player_node_index == self.player_traveling_edge.node_indexes[0])
                        self.state = "traveling"
        elif self.state == "traveling":
            self.update_player_position()
        
    def draw(self):
        self.program.screen.fill(point_crawl_background_color)
        
        # edges
        for edge in self.graph.edges:
            for i in range(edge.n_segments):
                pg.draw.line(surface = self.program.screen,
                             color = point_crawl_edge_color,
                             start_pos = edge.junction_positions[i],
                             end_pos = edge.junction_positions[i + 1],
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
                       center = (int(self.player_position[0]), int(self.player_position[1])),
                       radius = point_crawl_player_size)
        pg.draw.circle(surface = self.program.screen,
                       color = point_crawl_edge_color,
                       center = (int(self.player_position[0]), int(self.player_position[1])),
                       radius = point_crawl_player_size,
                       width = 1)
        