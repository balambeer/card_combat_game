import csv
import pygame as pg
import constants
from point_crawl import *
from fight_scene import *
from story_scene import *

class DataTable:
    def __init__(self, game,
                 csv_path):
        self.game = game
        
        self.read_csv(csv_path)
        
        for row in self.data:
            print(row)
            print(type(row))
            print(row[self.col_name_to_index["node_index"]])

    def read_csv(self, path):
        raw_table = []
        with open(path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                raw_table.append(row)
                
        self.n_rows = len(raw_table)
        self.n_cols = len(raw_table[0])
                
        self.process_csv(raw_table)
        
    def process_cardlist(self, cardlist_string):
        stripped_string = cardlist_string.strip("[]")
        card_list = stripped_string.split(";")
        
        def process_card(card_string):
            value_and_suit = card_string.strip("()").split(",")
            return (int(value_and_suit[0]), value_and_suit[1])
        
        return [ process_card(x) for x in card_list ]
    
    def process_neighborlist(self, neighborlist_string):
        stripped_string = neighborlist_string.strip("[]")
        
        return [ int(x) for x in stripped_string.split(";") ]
    
    def process_csv(self, table):
        # the * operator creates 2 lists and the zip
        col_name_and_type_pairs = [ item.split("-") for item in table[0] ]
        col_names_and_types = [ list(x) for x in zip(*col_name_and_type_pairs) ]
        self.header = col_names_and_types[0]
        types = col_names_and_types[1]
        
        self.data = []
        for i in range(1, self.n_rows):
            processed_row = table[i]
            for j in range(self.n_cols):
                if processed_row[j] == "NA":
                    processed_row[j] = None
                else:
                    if types[j] == "int":
                        processed_row[j] = int(processed_row[j])
                    elif types[j] == "cardlist":
                        processed_row[j] = self.process_cardlist(processed_row[j])
                    elif types[j] == "neighborlist":
                        processed_row[j] = self.process_neighborlist(processed_row[j])
            self.data.append(processed_row)
        
        self.col_name_to_index = dict([ (self.header[i], i) for i in range(len(self.header)) ])

class DungeonMaster:
    def __init__(self, game):
        self.game = game
        
        self.exploration_encounters = DataTable(self, "encounters/exploration.csv")
        self.point_crawl = DataTable(self, "encounters/point_crawl.csv")
        self.monsters = DataTable(self, "encounters/monsters.csv")
        
    def create_point_crawl_graph(self):
        nodes = []
        edges = []
        
        for row in self.point_crawl.data:
            node_index = row[self.point_crawl.col_name_to_index["node_index"]]
            new_node = GraphNode(index = node_index,
                                 position = support.XY(row[self.point_crawl.col_name_to_index["position_x"]],
                                                       row[self.point_crawl.col_name_to_index["position_y"]]),
                                 encounter_type = row[self.point_crawl.col_name_to_index["encounter_type"]])
            nodes.append(new_node)
            
            for i in row[self.point_crawl.col_name_to_index["neighbor_nodes"]]:
                if i > node_index:
                    edges.append((node_index, i))
                    
        return Graph(nodes, edges)
    
    def create_point_crawl(self, player_start_node):
        graph = self.create_point_crawl_graph()
        
        return PointCrawl(self.game.program,
                          graph,
                          player_start_node)
    
    def find_enemy_fighter(self, node_index):
        monster_row = None
        for row in self.monsters.data:
            if row[self.monsters.col_name_to_index["node_index"]] == node_index:
                # TODO: break out of the loop when the monster is found
                monster_row = row
                
        if not monster_row is None:
            return Fighter(game = self.game,
                           is_left_player = False,
                           is_human_controlled = False,
                           hp = monster_row[self.monsters.col_name_to_index["hp"]],
                           max_stress = monster_row[self.monsters.col_name_to_index["max_defense"]],
                           card_list = monster_row[self.monsters.col_name_to_index["card_list"]],
                           show_hand = False,
                           color = "tomato")
        
    def create_fight_scene(self, selected_node):
        player_fighter = Fighter(game = self.game,
                                 is_left_player = True,
                                 is_human_controlled = True,
                                 hp = self.game.player.hp,
                                 max_stress = self.game.player.max_stress,
                                 card_list = self.game.player.card_list,
                                 show_hand = True,
                                 color = "cornflowerblue")
        
        enemy_fighter = self.find_enemy_fighter(selected_node.index)
        
        return FightScene(self.game.program,
                          player = player_fighter,
                          enemy = enemy_fighter)
    
    def create_story_scene(self, selected_node):
        encounter_row = None
        option_1_resolution_text = None
        option_2_resolution_text = None
        option_3_resolution_text = None
        
        for row in self.exploration_encounters.data:
            if row[self.exploration_encounters.col_name_to_index["node_index"]] == selected_node.index:
                if row[self.exploration_encounters.col_name_to_index["encounter_index"]] == 0:
                    encounter_row = row
                elif row[self.exploration_encounters.col_name_to_index["encounter_index"]] == 1:
                    option_1_resolution_text = row[self.exploration_encounters.col_name_to_index["prompt"]]
                elif row[self.exploration_encounters.col_name_to_index["encounter_index"]] == 2:
                    option_2_resolution_text = row[self.exploration_encounters.col_name_to_index["prompt"]]
                elif row[self.exploration_encounters.col_name_to_index["encounter_index"]] == 3:
                    option_3_resolution_text = row[self.exploration_encounters.col_name_to_index["prompt"]]
        
        return StoryScene(program = self.game.program,
                          encounter_text = encounter_row[self.exploration_encounters.col_name_to_index["prompt"]],
                          option_1_text = encounter_row[self.exploration_encounters.col_name_to_index["option_1_text"]],
                          option_2_text = encounter_row[self.exploration_encounters.col_name_to_index["option_2_text"]],
                          option_3_text = encounter_row[self.exploration_encounters.col_name_to_index["option_3_text"]],
                          resolution_options = [option_1_resolution_text,
                                                option_2_resolution_text,
                                                option_3_resolution_text])
                    