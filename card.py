import pygame as pg
import constants

class Card():
    def __init__(self, game,
                 value,
                 suit,
                 effect,
                 color_back,
                 clickable,
                 draggable,
                 face_up):
        self.game = game

        self.left = 0
        self.top = 0
        self.card_rect = pg.Rect((self.left, self.top),
                                 (constants.card_width, constants.card_height))
        self.back_rect = pg.Rect((self.left + constants.card_back_border_width,
                                  self.top + constants.card_back_border_width),
                                 (constants.card_width - 2 * constants.card_back_border_width,
                                  constants.card_height - 2 * constants.card_back_border_width))
        
        self.value = value
        self.suit = suit
        self.effect = effect
        self.value_numeric = self.convert_value_to_numeric()
        self.face_up = face_up
        
        self.color = self.set_card_color()
        self.color_back = color_back
        self.font = pg.font.Font(None, constants.card_value_size)
        self.value_rendered = self.font.render(str(self.value), False, self.color)
        self.value_rect = self.value_rendered.get_rect(center = (int(self.left + constants.card_value_center[0] * constants.card_width),
                                                                 int(self.top + constants.card_value_center[1] * constants.card_height)))
        
        self.effect_rendered_list = self.render_effect(self.effect)
        self.effect_rect_list = self.set_effect_rects()
        
        self.clickable = clickable
        self.draggable = draggable
        self.pressed = False
        self.pressed_pos = (self.left, self.top)
        
    def render_effect(self, effect):
        if not effect is None:
            effect_words = effect.split(" ")
            rendered_list = []
            for word in effect_words:
                rendered_list.append(self.font.render(word, False, self.color))
            return rendered_list
        else:
            return None
            
    def set_effect_rects(self):
        if not self.effect_rendered_list is None:
            n_words = len(self.effect_rendered_list)
            if n_words == 1:
                return [ self.effect_rendered_list[0].get_rect(center = self.card_rect.center) ]
            elif n_words == 2:
                return [ self.effect_rendered_list[0].get_rect(midbottom = self.card_rect.center),
                         self.effect_rendered_list[1].get_rect(midtop = self.card_rect.center) ]
            elif n_words == 3:
                middle_word_rect = self.effect_rendered_list[1].get_rect(center = self.card_rect.center)
                return [ self.effect_rendered_list[0].get_rect(midbottom = middle_word_rect.midtop),
                         middle_word_rect,
                         self.effect_rendered_list[2].get_rect(midtop = middle_word_rect.midbottom) ]
            else:
                raise Exception("Don't support spells with more than 3 words")
        else:
            None
        
    def set_card_color(self):
        if self.suit == "spear":
            return "steelblue"
        elif self.suit == "shield":
            return "mediumseagreen"
        elif self.suit == "mana":
            return "mediumorchid"
        elif self.suit == "trump":
            return "black"
        
    def convert_value_to_numeric(self):
        if self.value == "A":
            return 1
        elif self.value == "J":
            return 11
        elif self.value == "Q":
            return 12
        elif self.value == "K":
            return 13
        elif self.value >= 2 and self.value <= 10:
            return self.value
        
    def draw_spear(self, topleft):
        pg.draw.polygon(surface = self.game.program.screen,
                        color = self.color,
                        points = [(topleft[0], topleft[1] + constants.card_suit_dimensions[1]),
                                  (topleft[0] + constants.card_suit_dimensions[0], topleft[1] + constants.card_suit_dimensions[1]),
                                  (topleft[0] + constants.card_suit_dimensions[0] // 2, topleft[1])])
        
    # This looks a little wonky
    def draw_shield(self, topleft):
        pg.draw.polygon(surface = self.game.program.screen,
                        color = self.color,
                        points = [(topleft[0], topleft[1]),
                                  (topleft[0] + constants.card_suit_dimensions[0], topleft[1]),
                                  (topleft[0] + constants.card_suit_dimensions[0], topleft[1] + constants.card_suit_dimensions[1] // 2),
                                  (topleft[0] + constants.card_suit_dimensions[0] // 2, topleft[1] + constants.card_suit_dimensions[1]),
                                  (topleft[0], topleft[1] + constants.card_suit_dimensions[1] // 2)])
    
    # This looks a little wonky...
    def draw_mana(self, topleft):
        pg.draw.polygon(surface = self.game.program.screen,
                        color = self.color,
                        points = [(topleft[0] + constants.card_suit_dimensions[0] // 2, topleft[1]),
                                  (topleft[0] + constants.card_suit_dimensions[0] * 2 // 3, topleft[1] + constants.card_suit_dimensions[1] // 3),
                                  (topleft[0] + constants.card_suit_dimensions[0], topleft[1] + constants.card_suit_dimensions[1] // 2),
                                  (topleft[0] + constants.card_suit_dimensions[0] * 2 // 3, topleft[1] + constants.card_suit_dimensions[1] * 2 // 3),
                                  (topleft[0] + constants.card_suit_dimensions[0] // 2, topleft[1] + constants.card_suit_dimensions[1]),
                                  (topleft[0] + constants.card_suit_dimensions[0] // 3, topleft[1] + constants.card_suit_dimensions[1] * 2 // 3),
                                  (topleft[0], topleft[1] + constants.card_suit_dimensions[1] // 2),
                                  (topleft[0] + constants.card_suit_dimensions[0] // 3, topleft[1] + constants.card_suit_dimensions[1] // 3)
                                  ])
        
    def draw_trump(self, topleft):
        pg.draw.polygon(surface = self.game.program.screen,
                        color = self.color,
                        points = [(topleft[0], topleft[1] + constants.card_suit_dimensions[1] // 2),
                                  (topleft[0] + constants.card_suit_dimensions[0] // 2, topleft[1]),
                                  (topleft[0] + constants.card_suit_dimensions[0], topleft[1] + constants.card_suit_dimensions[1] // 2),
                                  (topleft[0] + constants.card_suit_dimensions[0] // 2, topleft[1] + constants.card_suit_dimensions[1])])
        
    def draw_suit(self, topleft):
        if self.suit == "spear":
            self.draw_spear(topleft)
        elif self.suit == "mana":
            self.draw_mana(topleft)
        elif self.suit == "shield":
            self.draw_shield(topleft)
        elif self.suit == "trump":
            self.draw_trump(topleft)
        
    def highlight(self):
        if (self.clickable or self.draggable) and self.is_mouse_over():
            pg.draw.rect(surface = self.game.program.screen,
                     color = "orange",
                     rect = self.card_rect,
                     width = 2,
                     border_radius = constants.card_rounded_corner_size)
        
    def draw(self):        
        # card sheet
        pg.draw.rect(surface = self.game.program.screen,
                     color = "antiquewhite",
                     rect = self.card_rect,
                     border_radius = constants.card_rounded_corner_size)
        pg.draw.rect(surface = self.game.program.screen,
                     color = "black",
                     rect = self.card_rect,
                     width = 1,
                     border_radius = constants.card_rounded_corner_size)
        
        if self.face_up:
            # value
            self.game.program.screen.blit(self.value_rendered, self.value_rect)
            
            # suit
            suit_topleft = (int(self.left + (constants.card_suit_center[0] - constants.card_suit_size / 2) * constants.card_width),
                            int(self.top + (constants.card_suit_center[1] - constants.card_suit_size / 2) * constants.card_height))
            self.draw_suit(suit_topleft)
            
            # effect
            if not self.effect_rendered_list is None:
                for i in range(len(self.effect_rendered_list)):
                    self.game.program.screen.blit(self.effect_rendered_list[i], self.effect_rect_list[i])
        else:
            pg.draw.rect(surface = self.game.program.screen,
                     color = self.color_back,
                     rect = self.back_rect)
            pg.draw.rect(surface = self.game.program.screen,
                         color = "black",
                         rect = self.back_rect,
                         width = 2)
            
    # interaction
    def is_mouse_over(self):
        return self.card_rect.collidepoint(pg.mouse.get_pos())
            
    # TODO: Unfortunately we can press down outside of the card, drag the mouse in and release
    # and that would result in True below.
    # This is because pg.mouse.get_pressed() returns the current state of the buttons
    # Listening for a MOUSEBUTTONDOWN / UP event from the event queue would be better...
    def is_left_clicked(self):
        if pg.mouse.get_pressed()[0] and self.is_mouse_over():
            self.pressed = True
        if self.pressed:
            if not pg.mouse.get_pressed()[0]:
                self.pressed = False
                return self.is_mouse_over()
            
    def update_position(self, left, top):
        self.left = left
        self.top = top
        self.card_rect.update((self.left, self.top),
                                 (int(constants.card_width), int(constants.card_height)))
        self.back_rect.update((self.left + constants.card_back_border_width,
                                  self.top + constants.card_back_border_width),
                                 (constants.card_width - 2 * constants.card_back_border_width,
                                  constants.card_height - 2 * constants.card_back_border_width))
        self.value_rect.update(self.value_rendered.get_rect(center = (int(self.left + constants.card_value_center[0] * constants.card_width),
                                                                      int(self.top + constants.card_value_center[1] * constants.card_height))))
        if not self.effect_rendered_list is None:
            n_words = len(self.effect_rendered_list)
            if n_words == 1:
                self.effect_rect_list[0].update(self.effect_rendered_list[0].get_rect(center = self.card_rect.center))
            elif n_words == 2:
                self.effect_rect_list[0].update(self.effect_rendered_list[0].get_rect(midbottom = self.card_rect.center))
                self.effect_rect_list[1].update(self.effect_rendered_list[1].get_rect(midtop = self.card_rect.center))
            elif n_words == 3:
                self.effect_rect_list[1].update(self.effect_rendered_list[1].get_rect(center = self.card_rect.center))
                self.effect_rect_list[0].update(self.effect_rendered_list[0].get_rect(midbottom = self.effect_rect_list[1].midtop))
                self.effect_rect_list[2].update(self.effect_rendered_list[2].get_rect(midtop = self.effect_rect_list[1].midbottom))
            else:
                raise Exception("Don't support more than 3 word spells")
    
    def flip(self):
        self.face_up = not self.face_up
    
    def update(self):
        if self.clickable and not self.draggable:
            if self.is_left_clicked():
                self.flip()
        if self.draggable and not self.clickable:
            if self.is_mouse_over():
                if pg.mouse.get_pressed()[0] and not self.pressed:
                    self.pressed = True
                    self.pressed_pos = (pg.mouse.get_pos()[0] - self.left,
                                        pg.mouse.get_pos()[1] - self.top)
                elif not pg.mouse.get_pressed()[0]:
                    self.pressed = False
                    self.pressed_pos = (self.left, self.top)
            if self.pressed:
                self.update_position(pg.mouse.get_pos()[0] - self.pressed_pos[0],
                                     pg.mouse.get_pos()[1] - self.pressed_pos[1])
            