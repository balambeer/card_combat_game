import pygame as pg
import constants
import ai
import math
from card import *
from deck import *

class Fighter:
    def __init__(self, game,
                 is_left_player,
                 is_human_controlled,
                 hp,
                 card_list,
                 show_hand,
                 color):
        self.game = game

        self.is_left_player = is_left_player
        self.is_human_controlled = is_human_controlled
        self.ai_timer = constants.player_ai_delay
        self.ai_card_index = None
        
        self.color = color
        self.hp = hp
        self.font = pg.font.Font(None, constants.player_hp_size)
        self.hp_rendered = self.font.render(str(self.hp), False, self.color)
        self.hp_rect = self.set_hp_rect(self.is_left_player)
        
        self.state = "clean_up"
        self.todo = "nothing"
        
        self.damage_animation_clock = 0
        self.damage_rendered = self.font.render(str(0), False, self.color)
        self.damage_rect = self.damage_rendered.get_rect(midbottom = self.hp_rect.midtop)
        
        self.character_animation_state = "idle"
        self.character_animation_frame = 0
        # self.character_animation_rendered = self.font.render(self.character_animation_state + " " + str(self.character_animation_frame), False, self.color)
        self.character_animation_rendered = self.font.render(self.character_animation_state, False, self.color)
        self.character_animation_rect = self.set_character_animation_rect()
        
        self.draw_deck = self.create_draw_deck(card_list, self.is_left_player)
        self.hand = self.create_hand(self.is_left_player, show_hand)
        self.discard_pile = self.create_discard_pile(self.is_left_player)
        self.play_area = self.create_play_area(self.is_left_player)
        
    def set_hp_rect(self, is_left_player):
        hp_rect_center_left = int(constants.player_hp_rect_center_ratio.x * constants.screen_width)
        if not is_left_player:
            hp_rect_center_left = constants.screen_width - hp_rect_center_left
        return self.hp_rendered.get_rect(center = (hp_rect_center_left,
                                                   int(constants.player_hp_rect_center_ratio.y * constants.screen_height)))
    
    def set_character_animation_rect(self):
        if self.is_left_player:
            character_animation_rect_x = constants.player_left_character_animation_center_x
        else:
            character_animation_rect_x = constants.player_right_character_animation_center_x
        character_animation_rect_y = constants.player_character_animation_center_y
        return self.character_animation_rendered.get_rect(center = (character_animation_rect_x, character_animation_rect_y))

    def create_draw_deck(self, card_list, is_left_player):
        if is_left_player:
            left = constants.player_left_draw_deck_left
        else:
            left = constants.player_right_draw_deck_left
        top = constants.player_draw_deck_top
        deck = Deck(game = self.game,
                    card_list = [],
                    left = left,
                    top = top,
                    face_up = False,
                    is_pile = True)
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
            left = constants.screen_half_width - constants.card_width
        else:
            left = constants.screen_half_width
        top = constants.player_draw_deck_top
        return Deck(game = self.game,
                    card_list = [],
                    left = left,
                    top = top,
                    face_up = True,
                    is_pile = False)
        
    def create_discard_pile(self, is_left_player):
        if is_left_player:
            left = constants.player_left_draw_deck_left
        else:
            left = constants.player_right_draw_deck_left
        top = constants.player_discard_pile_top
        return Deck(game = self.game,
                    card_list = [],
                    left = left,
                    top = top,
                    face_up = False,
                    is_pile = True)
    
    def create_hand(self, is_left_player, show_hand):
        if is_left_player:
            left = constants.player_left_hand_left
        else:
            left = constants.player_right_hand_left
        top = constants.player_draw_deck_top
        return Deck(game = self.game,
                    card_list = [],
                    left = left,
                    top = top,
                    face_up = show_hand,
                    is_pile = False)
    
    def display_hp(self):
        self.game.program.screen.blit(self.hp_rendered, self.hp_rect)
        
    def display_damage(self):
        self.damage_rect.update((self.damage_rect.left, self.damage_rect.top - constants.player_damage_drift_v * self.game.delta_time),
                                (self.damage_rect.width, self.damage_rect.height))
        self.game.program.screen.blit(self.damage_rendered, self.damage_rect)
        
    def display_character(self):
        self.character_animation_rendered = self.font.render(self.character_animation_state, # + " " + str(self.character_animation_frame),
                                                             False,
                                                             self.color)
        self.character_animation_rect.update(self.character_animation_rendered.get_rect(center = self.character_animation_rect.center))
        self.game.program.screen.blit(self.character_animation_rendered, self.character_animation_rect)
        
    def display(self):
        self.draw_deck.draw()
        self.hand.draw()
        self.discard_pile.draw()
        self.play_area.draw()
        self.display_character()
        self.display_hp()
        if self.damage_animation_clock > 0:
            self.damage_animation_clock -= self.game.delta_time
            self.display_damage()
                
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
                    self.state = "played_card"
                else:
                    self.hand.active_card_index = None
                    self.hand.selected_card_index = None
                    self.hand.set_card_positions()
                    self.hand.set_deck_rect()
      
    def listen_to_ai_input(self, opponent_card_played):
        if self.ai_timer <= 0:
            if self.ai_card_index is None:
                # self.ai_card_index = ai.select_random(len(self.hand.card_list))
                self.ai_card_index = ai.select_greedy(opponent_card_played, self.hand)
            self.slide_cards(from_deck = self.hand,
                             to_deck = self.play_area,
                             card_indexes = [self.ai_card_index],
                             slide_v_per_ms = constants.animation_card_slide_v_per_ms)
            if self.is_slide_animation_finished(from_deck = self.hand,
                                                to_deck = self.play_area,
                                                card_indexes = [self.ai_card_index]):
                card = self.hand.card_list[self.ai_card_index]
                self.hand.remove_card(card)
                self.play_area.add_card(card)
                
                self.state = "played_card"
                self.ai_timer = constants.player_ai_delay
                self.ai_card_index = None
        else:
            self.ai_timer -= self.game.delta_time
                
    def perform_attack(self, is_killing_blow):
        if not is_killing_blow:
            self.character_animation_state = "attack"
            self.character_animation_frame = constants.player_character_animation_attack_frame_count
        else:
            self.perform_killing_blow()
        
    def perform_riposte(self, is_killing_blow):
        if not is_killing_blow:
            self.character_animation_state = "riposte"
            self.character_animation_frame = constants.player_character_animation_riposte_frame_count
        else:
            self.perform_killing_blow()
        
    def perform_killing_blow(self):
        self.character_animation_state = "killing_blow"
        self.character_animation_frame = constants.player_character_animation_killing_blow_frame_count
                
    def take_damage(self, damage, was_riposte):
        self.hp = max(0, self.hp - damage)
        self.hp_rendered = self.font.render(str(self.hp), False, self.color)
        self.hp_rect = self.set_hp_rect(self.is_left_player)
        
        if damage > 0:
            self.damage_animation_clock = constants.player_damage_animation_length_in_ms
            self.damage_rendered = self.font.render(str(-damage), False, self.color)
            self.damage_rect = self.damage_rendered.get_rect(midbottom = self.hp_rect.midtop)
            
            if self.hp > 0:
                if was_riposte:
                    self.character_animation_state = "riposte_pain"
                    self.character_animation_frame = constants.player_character_animation_riposte_pain_frame_count
                else:
                    self.character_animation_state = "pain"
                    self.character_animation_frame = constants.player_character_animation_pain_frame_count
            else:
                self.character_animation_state = "death"
                self.character_animation_frame = constants.player_character_animation_death_frame_count
        else:
            if was_riposte:
                self.character_animation_state = "riposte_blocked"
                self.character_animation_frame = constants.player_character_animation_riposte_blocked_frame_count
            else:
                self.character_animation_state = "blocked"
                self.character_animation_frame = constants.player_character_animation_blocked_frame_count
        
    def slide_cards(self, from_deck, to_deck, card_indexes, slide_v_per_ms):
        d = math.sqrt((to_deck.left - from_deck.left) ** 2 + (to_deck.top - from_deck.top) ** 2)
        n_steps = d / (slide_v_per_ms * 1000 / constants.fps)
        v = support.XY(int((to_deck.left - from_deck.left) / n_steps),
                       int((to_deck.top - from_deck.top) / n_steps))
        for i in card_indexes:
            new_left = from_deck.card_list[i].left + v.x
            new_top = from_deck.card_list[i].top + v.y
            if (new_left - to_deck.left) * (from_deck.left - to_deck.left) <= 0:
                new_left = to_deck.left
            if (new_top - to_deck.top) * (from_deck.top - to_deck.top) <= 0:
                new_top = to_deck.top
            from_deck.card_list[i].update_position(new_left, new_top)
        
    def is_slide_animation_finished(self, from_deck, to_deck, card_indexes):
        last_card_index = max(card_indexes)
        return from_deck.card_list[last_card_index].left == to_deck.left and from_deck.card_list[last_card_index].top == to_deck.top
            
    def clear_play_area(self):
        self.slide_cards(from_deck = self.play_area,
                         to_deck = self.discard_pile,
                         card_indexes = [0],
                         slide_v_per_ms = constants.animation_card_slide_v_per_ms)
        if self.is_slide_animation_finished(from_deck = self.play_area,
                                  to_deck = self.discard_pile,
                                  card_indexes = [0]):
            for card in self.play_area.card_list:
                card.flip()
                self.play_area.remove_card(card)
                self.discard_pile.add_card(card)
            self.todo_clear_play_area = False
            
    def replenish_draw_deck(self):
        self.slide_cards(from_deck = self.discard_pile,
                         to_deck = self.draw_deck,
                         card_indexes = range(len(self.discard_pile.card_list)),
                         slide_v_per_ms = constants.animation_card_slide_v_per_ms)
        if self.is_slide_animation_finished(from_deck = self.discard_pile,
                                            to_deck = self.draw_deck,
                                            card_indexes = range(len(self.discard_pile.card_list))):
            for i in range(len(self.discard_pile.card_list)):
                self.draw_deck.add_card(self.discard_pile.card_list.pop())
            self.draw_deck.shuffle()
            self.draw_deck.set_card_positions()
            self.draw_deck.set_deck_rect()
            self.discard_pile.set_card_positions()
            self.discard_pile.set_deck_rect()
            self.todo_replenish_draw_deck = False
        
    def draw_a_card_to_hand(self):
        self.slide_cards(from_deck = self.draw_deck,
                         to_deck = self.hand,
                         card_indexes = [0],
                         slide_v_per_ms = constants.animation_card_slide_v_per_ms)
        if self.is_slide_animation_finished(from_deck = self.draw_deck,
                                            to_deck = self.hand,
                                            card_indexes = [0]):
            card = self.draw_deck.card_list.pop()
            self.draw_deck.set_card_positions()
            self.draw_deck.set_deck_rect()
            if self.hand.face_up:
                card.face_up = True
            if self.is_human_controlled:
                card.draggable = True
            self.hand.add_card(card)
            self.todo_draw_a_card_to_hand = False
        
    def update_todo_list(self):
        if self.state == "clean_up":
            if not self.play_area.is_empty():
                self.todo = "clear_play_area"
            elif len(self.hand.card_list) < constants.player_hand_size:
                if not self.draw_deck.is_empty():
                    self.todo = "draw_a_card_to_hand"
                elif not self.discard_pile.is_empty():
                    self.todo = "replenish_draw_deck"
            else:
                self.todo = "nothing"
                
            if self.todo == "nothing":
                self.state = "waiting"
                
    def update_character(self, is_leading_player):
        if self.character_animation_frame == 0:
            if not (self.character_animation_state == "death" or self.character_animation_state == "killing_blow"):
                if is_leading_player:
                    self.character_animation_state = "idle_active"
                else:
                    self.character_animation_state = "idle_passive"
                self.character_animation_frame = constants.player_character_animation_idle_frame_count
        else:
            self.character_animation_frame -= 1
        
    def update(self, is_leading_player, opponent_card_played):
        self.update_character(is_leading_player)
        if not (self.character_animation_state == "idle_active" or self.character_animation_state == "idle_passive"):
            self.state = "animating"
        
        if self.state == "my_turn":
            if self.is_human_controlled:
                self.listen_to_card_played()
            else:
                self.listen_to_ai_input(opponent_card_played)
        elif self.state == "animating":
            if self.character_animation_state == "idle_active" or self.character_animation_state == "idle_passive":
                self.state = "clean_up"
        elif self.state == "clean_up":
            self.update_todo_list()
            if self.todo == "clear_play_area":
                self.clear_play_area()
            elif self.todo == "replenish_draw_deck":
                self.replenish_draw_deck()
            elif self.todo == "draw_a_card_to_hand":
                self.draw_a_card_to_hand()
        
            
