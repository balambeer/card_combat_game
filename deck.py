import pygame as pg
import random
from card import *
import constants

class Deck:
    def __init__(self, game,
                 card_list,
                 left,
                 top,
                 face_up,
                 is_pile):
        self.game = game
        
        self.card_list = card_list
        self.face_up = face_up
        self.is_pile = is_pile
        
        self.left = left
        self.top = top
        self.n_cards_to_display = 0
        self.set_n_cards_to_display()
        
        self.deck_rect = None
        self.set_deck_rect()
        self.set_card_positions()
        
        self.active_card_index = None
        self.selected_card_index = None
        
    def set_n_cards_to_display(self):
        if not self.is_pile:
            self.n_cards_to_display = len(self.card_list)
        else:
            self.n_cards_to_display = (len(self.card_list) + constants.deck_pile_draw_card_skip - 1) // constants.deck_pile_draw_card_skip
        
    def set_deck_rect(self):
        self.set_n_cards_to_display()
        if not self.is_pile:
            self.deck_rect = pg.Rect((self.left, self.top),
                                     (max(0, self.n_cards_to_display - 1) * constants.deck_not_pile_shift * constants.card_width + constants.card_width,
                                      constants.card_height))
        else:
            self.deck_rect = pg.Rect((self.left, self.top - max(0, self.n_cards_to_display - 1) * constants.deck_pile_shift * constants.card_width),
                                     (max(0, self.n_cards_to_display - 1) * constants.deck_pile_shift * constants.card_width + constants.card_width,
                                      max(0, self.n_cards_to_display - 1) * constants.deck_pile_shift * constants.card_width + constants.card_height))
    
    def set_card_positions(self):
        for i in range(len(self.card_list)):
            if not self.is_pile:
                self.card_list[i].update_position(self.left + int(i * constants.deck_not_pile_shift * constants.card_width),
                                                  self.top)
            else:
                self.card_list[i].update_position(self.left + int(i * constants.deck_pile_shift * constants.card_width),
                                                  self.top - int(i * constants.deck_pile_shift * constants.card_width))
        
    def draw(self):
        pg.draw.rect(surface = self.game.program.screen,
                     color = "yellow",
                     rect = self.deck_rect,
                     width = 2)
        for i in range(self.n_cards_to_display):
            if not self.active_card_index == i:
                self.card_list[i].draw()
        if not self.active_card_index == None:
            self.card_list[self.active_card_index].draw()
            self.card_list[self.active_card_index].highlight()

    def add_card(self, card):
        if self.face_up:
            card.face_up = True
        else:
            card.face_up = False
        self.card_list.append(card)
        self.set_card_positions()
        self.set_deck_rect()

    def remove_card(self, card):
        self.card_list.remove(card)
        self.set_card_positions()
        self.set_deck_rect()

    def shuffle(self):
        random.shuffle(self.card_list)
        
    def is_empty(self):
        return len(self.card_list) == 0
            
    def update(self):
        if self.selected_card_index is None:
            self.active_card_index = None
            for i in range(len(self.card_list)):
                if self.card_list[i].is_mouse_over():
                    self.active_card_index = i
            if not self.active_card_index is None:
                if pg.mouse.get_pressed()[0]:
                    self.selected_card_index = self.active_card_index
        else:
            self.card_list[self.selected_card_index].update()
#             if not pg.mouse.get_pressed()[0]:
#                 self.selected_card_index = None
