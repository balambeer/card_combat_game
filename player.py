import pygame as pg
import settings
from card import *
from deck import *

class Player:
    def __init__(self, game,
                 is_left_player,
                 hp,
                 card_list,
                 color):
        self.game = game

        self.is_left_player = is_left_player
        self.color = color
        self.hp = hp
        self.font = pg.font.Font(None, settings.player_hp_size)
        self.hp_rendered = self.font.render(str(self.hp), False, self.color)
        self.hp_rect = self.set_hp_rect(self.is_left_player)
        
        self.animation_in_progress = False
        self.listening_to_inputs = False

        self.draw_deck = self.create_draw_deck(card_list, self.is_left_player)
        self.hand = self.create_hand(self.is_left_player)
        self.discard_pile = self.create_discard_pile(self.is_left_player)
        self.play_area = self.create_play_area(self.is_left_player)
        
        for i in range(settings.player_hand_size):
            self.update_decks()
        
    def set_hp_rect(self, is_left_player):
        hp_rect_center_left = int(settings.player_hp_rect_center_ratio.x * settings.screen_width)
        if not is_left_player:
            hp_rect_center_left = settings.screen_width - hp_rect_center_left
        return self.hp_rendered.get_rect(center = (hp_rect_center_left,
                                                   int(settings.player_hp_rect_center_ratio.y * settings.screen_height)))

    def create_draw_deck(self, card_list, is_left_player):
        if is_left_player:
            left = settings.player_left_draw_deck_left
        else:
            left = settings.player_right_draw_deck_left
        top = settings.player_draw_deck_top
        deck = Deck(game = self.game,
                    card_list = [],
                    left = left,
                    top = top,
                    face_up = False)
        for card_params in card_list:
            card = Card(game = self.game,
                        value = card_params[0],
                        suit = card_params[1],
                        color_back = self.color,
                        clickable = False,
                        draggable = False,
                        face_up = False)
            deck.add_card(card)
        deck.shuffle()
        deck.set_card_positions()
        deck.set_deck_rect()
        return deck

    def create_play_area(self, is_left_player):
        if is_left_player:
            left = settings.screen_half_width - settings.card_width
        else:
            left = settings.screen_half_width
        top = settings.player_draw_deck_top
        return Deck(game = self.game,
                    card_list = [],
                    left = left,
                    top = top,
                    face_up = True)
        
    def create_discard_pile(self, is_left_player):
        if is_left_player:
            left = settings.player_left_draw_deck_left
        else:
            left = settings.player_right_draw_deck_left
        top = settings.player_discard_pile_top
        return Deck(game = self.game,
                    card_list = [],
                    left = left,
                    top = top,
                    face_up = False)
    
    def create_hand(self, is_left_player):
        if is_left_player:
            left = settings.player_left_hand_left
        else:
            left = settings.player_right_hand_left
        top = settings.player_draw_deck_top
        return Deck(game = self.game,
                    card_list = [],
                    left = left,
                    top = top,
                    face_up = True)
    
    def display_hp(self):
        self.game.program.screen.blit(self.hp_rendered, self.hp_rect)
        
    def draw(self):
        self.draw_deck.draw()
        self.hand.draw()
        self.discard_pile.draw()
        self.play_area.draw()
        self.display_hp()
        
    def replenish_draw_deck(self):
        for i in range(len(self.discard_pile.card_list)):
            # pg.time.wait(50)
            self.draw_deck.add_card(self.discard_pile.card_list.pop())
        self.draw_deck.shuffle()
        self.draw_deck.set_card_positions()
        self.draw_deck.set_deck_rect()
        self.discard_pile.set_card_positions()
        self.discard_pile.set_deck_rect()
        
    def replenish_hand(self):
        n_cards_in_draw_deck = len(self.draw_deck.card_list)
        n_cards_to_draw_at_first = min(settings.player_hand_size, n_cards_in_draw_deck)
        for i in range(n_cards_to_draw_at_first):
            # pg.time.wait(250)
            card = self.draw_deck.card_list.pop()
            self.draw_deck.set_card_positions()
            self.draw_deck.set_deck_rect()
            card.face_up = True
            card.draggable = True
            self.hand.add_card(card)
        if n_cards_to_draw_at_first < settings.player_hand_size:
            self.replenish_draw_deck()
            n_cards_still_needed = settings.player_hand_size - n_cards_to_draw_at_first
            for i in range(min(n_cards_still_needed, len(self.draw_deck.card_list))):
                # pg.time.wait(250)
                card = self.draw_deck.card_list.pop()
                self.draw_deck.set_card_positions()
                self.draw_deck.set_deck_rect()
                card.face_up = True
                card.draggable = True
                self.hand.add_card(card)
        
    def draw_a_card_to_hand(self):
        card = self.draw_deck.card_list.pop()
        self.draw_deck.set_card_positions()
        self.draw_deck.set_deck_rect()
        card.face_up = True
        card.draggable = True
        self.hand.add_card(card)
        
    def listen_to_card_played(self):
        self.hand.update()
        if not self.hand.selected_card_index is None:
            if not pg.mouse.get_pressed()[0]:
                if self.play_area.deck_rect.collidepoint(pg.mouse.get_pos()):
                    card = self.hand.card_list[self.hand.selected_card_index]
                    card.draggable = False
                    
                    self.hand.active_card_index = None
                    self.hand.selected_card_index = None
                    self.hand.remove_card(card)
                    
                    self.play_area.add_card(card)
                else:
                    self.hand.active_card_index = None
                    self.hand.selected_card_index = None
                    self.hand.set_card_positions()
                    self.hand.set_deck_rect()
                    
    def update_decks(self):
        if self.hp > 0 and not self.listening_to_inputs:
            if len(self.hand.card_list) < settings.player_hand_size:
                if not self.draw_deck.is_empty():
                    self.draw_a_card_to_hand()
                elif not self.discard_pile.is_empty():
                    self.replenish_draw_deck()
                    self.draw_a_card_to_hand()
                else:
                    self.listening_to_inputs = True
            else:
                self.listening_to_inputs = True
            if self.hand.is_empty():
                self.hp = 0
    
    def clear_play_area(self):
        if not self.play_area.is_empty():
            for card in self.play_area.card_list:
                card.flip()
                self.play_area.remove_card(card)
                self.discard_pile.add_card(card)
            
    def slide_cards(self, from_deck, to_deck, n_cards_to_slide, slide_time_in_ms):
        n_steps = (slide_time_in_ms / 1000) * settings.fps
        v = support.XY(int((to_deck.left - from_deck.left) / n_steps),
                       int((to_deck.top - from_deck.top) / n_steps))
        num_cards_to_slide = min(n_cards_to_slide, len(from_deck.card_list))
        for i in range(num_cards_to_slide):
            new_left = from_deck.card_list[i].left + v.x
            new_top = from_deck.card_list[i].top + v.y
            if (new_left - to_deck.left) * (from_deck.left - to_deck.left) <= 0:
                new_left = to_deck.left
            if (new_top - to_deck.top) * (from_deck.top - to_deck.top) <= 0:
                new_top = to_deck.top
            from_deck.card_list[i].update_position(new_left, new_top)
        if from_deck.card_list[num_cards_to_slide - 1].left == to_deck.left and from_deck.card_list[num_cards_to_slide - 1].top == to_deck.top:
            self.animation_in_progress = False
                
    def take_damage(self, damage):
        self.hp = max(0, self.hp - damage)
        self.hp_rendered = self.font.render(str(self.hp), False, self.color)
        self.hp_rect = self.set_hp_rect(self.is_left_player)
        
#     def update(self):
#         if self.hp > 0:
#             if len(self.hand.card_list) < settings.player_hand_size:
#                 if not self.draw_deck.is_empty():
#                     self.draw_a_card_to_hand()
#                 elif not self.discard_pile.is_empty():
#                     self.replenish_draw_deck()
#             if self.hand.is_empty():
#                 self.hp = 0
#             else:
#                 # TODO: rename this so that it's clear that we listen to player inputs here
#                 self.hand.update()
#                 self.listen_to_card_played()
        
            
