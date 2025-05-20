import pygame as pg

class Player:
    def __init__(self, program,
                 name,
                 hp,
                 max_defense,
                 card_list,
                 skill_list,
                 story_keywords):
        self.program = program
        
        self.name = name
        self.hp = hp
        self.max_defense = max_defense
        self.card_list = card_list
        self.skill_list = skill_list
        self.story_keywords = story_keywords
       
    # redundant?
    def set_hp(self, new_hp):
        self.hp = new_hp
        
    def gain_card(self, new_card):
        self.card_list.append(new_card)
        
    def gain_skill(self, new_skill):
        self.skill_list.append(new_skill)
        
    def gain_keyword(self, new_keyword):
        self.story_keywords.append(new_keyword)
        
    def lose_keyword(self, keyword):
        self.story_keywords.remove(keyword)