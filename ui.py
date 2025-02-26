import pygame as pg
import constants

class Button():
    def __init__(self, program,
                 center_position,
                 font,
                 text,
                 background_color,
                 idle_color,
                 active_color):
        self.program = program
        
        self.pressed = False
        
        self.background_color = background_color
        self.idle_color = idle_color
        self.active_color = active_color
        
        self.font = font
        self.text = text
        self.text_rendered = self.font.render(text, False, self.idle_color)
        self.text_rect = self.text_rendered.get_rect(center = (int(center_position[0] * constants.resolution[0]),
                                                               int(center_position[1] * constants.resolution[1])))
        
        self.background_rect = self.text_rect.inflate(0.1 * self.text_rendered.get_width(),
                                                      0.1 * self.text_rendered.get_height())
        
    def draw(self):
        pg.draw.rect(self.program.screen, self.background_color, self.background_rect)
        if self.pressed and self.background_rect.collidepoint(pg.mouse.get_pos()):
            self.text_rendered = self.font.render(self.text, False, self.active_color)
            
            pg.draw.rect(self.program.screen, self.active_color, self.background_rect, int(0.1 * self.text_rendered.get_height()))
            self.program.screen.blit(self.text_rendered, self.text_rect)
        else:
            self.text_rendered = self.font.render(self.text, False, self.idle_color)
            
            pg.draw.rect(self.program.screen, self.idle_color, self.background_rect, int(0.1 * self.text_rendered.get_height()))
            self.program.screen.blit(self.text_rendered, self.text_rect)
            if self.background_rect.collidepoint(pg.mouse.get_pos()):
                pg.draw.rect(self.program.screen, self.active_color, self.background_rect, 1)
        
    def is_left_clicked(self):
        if pg.mouse.get_pressed()[0]:
            if self.background_rect.collidepoint(pg.mouse.get_pos()):
                self.pressed = True
        if self.pressed:
            if not pg.mouse.get_pressed()[0]:
                self.pressed = False
                return self.background_rect.collidepoint(pg.mouse.get_pos())