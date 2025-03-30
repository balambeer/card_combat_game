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
            # print(row[self.col_name_to_index["location_index"]])

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
        
        self.scene_library = DataTable(self, "encounters/scene_library.csv")
        self.point_crawl = DataTable(self, "encounters/point_crawl.csv")
        self.monster_manual = DataTable(self, "encounters/monster_manual.csv")
        
        self.current_scene_index = None
        
    def create_point_crawl_graph(self):
        nodes = []
        edges = []
        
        for row in self.point_crawl.data:
            node_index = row[self.point_crawl.col_name_to_index["location_index"]]
            new_node = GraphNode(index = node_index,
                                 position = support.XY(row[self.point_crawl.col_name_to_index["position_x"]],
                                                       row[self.point_crawl.col_name_to_index["position_y"]]))
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
    
    def trigger_by_keywords(self, skip_keyword, trigger_keyword, player_keywords):            
        if (skip_keyword is None) or (not skip_keyword in player_keywords):
            return (trigger_keyword is None) or (trigger_keyword in player_keywords)
        else:
            return False
    
    def find_scene_in_library(self, location_index, scene_index, player_keywords):
        scene_row = None
        
        for row in self.scene_library.data:
            row_location_index = row[self.scene_library.col_name_to_index["location_index"]]
            row_scene_index = row[self.scene_library.col_name_to_index["scene_index"]]
            if (row_location_index == location_index and row_scene_index == scene_index):
                row_skip_keyword = row[self.scene_library.col_name_to_index["skip_if_story_keyword"]]
                row_trigger_keyword = row[self.scene_library.col_name_to_index["only_if_story_keyword"]]
                if self.trigger_by_keywords(row_skip_keyword, row_trigger_keyword, player_keywords):
                    scene_row = row
                    break
            
        return scene_row
    
    def find_monster_in_manual(self, monster_name):
        monster_row = None
        for row in self.monster_manual.data:
            if row[self.monster_manual.col_name_to_index["monster_name"]] == monster_name:
                monster_row = row
                break
                
        return monster_row
    
    def create_enemy_fighter(self, monster_row):                
        if not monster_row is None:
            return Fighter(game = self.game,
                           is_left_player = False,
                           is_human_controlled = False,
                           hp = monster_row[self.monster_manual.col_name_to_index["hp"]],
                           max_stress = monster_row[self.monster_manual.col_name_to_index["max_defense"]],
                           card_list = monster_row[self.monster_manual.col_name_to_index["card_list"]],
                           show_hand = False,
                           color = "tomato")
        
    def find_next_scene_index(self, next_scene_options_string, player_keywords):
        stripped_string = next_scene_options_string.strip("[]")
        next_scene_options_list = stripped_string.split(";")
        
        next_scene_index = int(next_scene_options_list[0]) # default
        # take first option with matching keyword if any
        if len(next_scene_options_list) > 1:
            for i in range(1, len(next_scene_options_list)):
                keyword_and_index = next_scene_options_list[i].split(":")
                if keyword_and_index[0] in player_keywords:
                    next_scene_index = int(keyword_and_index[1])
                    break
        return next_scene_index 
        
    def create_fight_scene(self, scene_row):
        player_fighter = Fighter(game = self.game,
                                 is_left_player = True,
                                 is_human_controlled = True,
                                 hp = self.game.player.hp,
                                 max_stress = self.game.player.max_stress,
                                 card_list = self.game.player.card_list,
                                 show_hand = True,
                                 color = "cornflowerblue")

        monster_row = self.find_monster_in_manual(scene_row[self.scene_library.col_name_to_index["monster_name"]])
        enemy_fighter = self.create_enemy_fighter(monster_row)
        
        return FightScene(self.game.program,
                          player = player_fighter,
                          enemy = enemy_fighter,
                          next_scene_options = scene_row[self.scene_library.col_name_to_index["option_1_next_scene"]])
    
    def create_story_option(self, scene_row, option_index, player_keywords):
        option_skip_keyword = scene_row[self.scene_library.col_name_to_index["option_" + str(option_index) + "_skip_if"]]
        option_trigger_keyword = scene_row[self.scene_library.col_name_to_index["option_" + str(option_index) + "_only_if"]]
    
        if self.trigger_by_keywords(option_skip_keyword, option_trigger_keyword, player_keywords):
            return ProgressionOption(text = scene_row[self.scene_library.col_name_to_index["option_" + str(option_index) + "_text"]],
                                     effect = scene_row[self.scene_library.col_name_to_index["option_" + str(option_index) + "_effect"]],
                                     next_scene_options = scene_row[self.scene_library.col_name_to_index["option_" + str(option_index) + "_next_scene"]])
        else:
            return None
    
    def create_story_scene(self, scene_row, player_keywords):          
        option_1 = self.create_story_option(scene_row, 1, player_keywords)
        option_2 = self.create_story_option(scene_row, 2, player_keywords)
        option_3 = self.create_story_option(scene_row, 3, player_keywords)
        return StoryScene(program = self.game.program,
                          prompt = scene_row[self.scene_library.col_name_to_index["prompt"]],
                          option_1 = option_1,
                          option_2 = option_2,
                          option_3 = option_3)
    
    def create_scene(self, location_index, scene_index, player_keywords):
        scene_row = self.find_scene_in_library(location_index, scene_index, player_keywords)
        
        if scene_row[self.scene_library.col_name_to_index["scene_type"]] == "story":
            scene = self.create_story_scene(scene_row, player_keywords)
        elif scene_row[self.scene_library.col_name_to_index["scene_type"]] == "combat":
            scene = self.create_fight_scene(scene_row)
    
        return scene

                    