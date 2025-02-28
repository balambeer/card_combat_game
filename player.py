import pygame as pg

class Player:
    def __init__(self, program,
                 hp,
                 max_stress,
                 card_list,
                 skill_list):
        self.program = program
        
        self.hp = hp
        self.max_stress = max_stress
        self.card_list = card_list
        self.skill_list = skill_list
       
    # redundant?
    def set_hp(self, new_hp):
        self.hp = new_hp
        
    def add_card(self, new_card):
        self.card_list.append(new_card)
        
    def add_skill(self, new_skill):
        self.skill_list.append(new_skill)