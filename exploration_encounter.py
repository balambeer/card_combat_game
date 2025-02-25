import pygame as pg
import constants
from ui import *

textbox_margin = int(0.1 * constants.screen_width)
textbox_left = textbox_margin
textbox_top = int(0.2 * constants.screen_height)
textbox_width = constants.screen_width - 2 * textbox_margin
textbox_height = constants.screen_height - textbox_margin - textbox_top

text_margin = int(0.05 * constants.screen_width)
text_left = textbox_left + text_margin
text_top = textbox_top + text_margin

font_size = int(0.05 * constants.screen_height)

background_color = "midnightblue"
textbox_color = "gray"
text_color = "black"
button_idle_color = "black"
button_active_color = "white"

class ExplorationEncounter:
    def __init__(self, program,
                 encounter_text,
                 option_1_text,
                 option_2_text,
                 option_3_text,
                 resolution_options):
        self.program = program
        self.state = "waiting_for_input"
        
        self.font = pg.font.Font(None, font_size)
        
        self.encounter_text = encounter_text
        self.option_1_text = option_1_text
        self.option_2_text = option_2_text
        self.option_3_text = option_3_text
        
        self.textbox_rect = pg.Rect((textbox_left, textbox_top),
                                    (textbox_width, textbox_height))
        self.encounter_text_rendered = self.font.render(self.encounter_text, False, text_color)
        self.encounter_text_rect = self.encounter_text_rendered.get_rect(topleft = (text_top, text_left))
        
        self.option_1_button = Button(program = program,
                                      center_position = (0.5,
                                                         (self.encounter_text_rect.bottom + 1.5 * font_size) / constants.screen_height),
                                      text = option_1_text,
                                      background_color = textbox_color,
                                      idle_color = button_idle_color,
                                      active_color = button_active_color)
        self.option_2_button = Button(program = program,
                                      center_position = (0.5,
                                                         (self.option_1_button.text_rect.bottom + 1.5 * font_size) / constants.screen_height),
                                      text = option_2_text,
                                      background_color = textbox_color,
                                      idle_color = button_idle_color,
                                      active_color = button_active_color)
        self.option_3_button = Button(program = program,
                                      center_position = (0.5,
                                                         (self.option_2_button.text_rect.bottom + 1.5 * font_size) / constants.screen_height),
                                      text = option_3_text,
                                      background_color = textbox_color,
                                      idle_color = button_idle_color,
                                      active_color = button_active_color)
        
        self.resolution_options = resolution_options
        self.resolution_text = None
        self.continue_button = None
        
    def draw(self):
        self.program.screen.fill(background_color)
        
        pg.draw.rect(self.program.screen,
                     textbox_color,
                     self.textbox_rect)
        if self.state == "waiting_for_input":
            self.program.screen.blit(self.encounter_text_rendered,
                                     self.encounter_text_rect)
            self.option_1_button.draw()
            self.option_2_button.draw()
            self.option_3_button.draw()
        elif self.state == "resolution":
            self.program.screen.blit(self.resolution_text_rendered,
                                     self.resolution_text_rect)
            self.continue_button.draw()
        
    def update(self):
        if self.state == "waiting_for_input":
            if self.option_1_button.is_left_clicked():
                self.state = "resolution"
                self.resolution_text = self.resolution_options[0]
                self.option_1_button = None
                self.option_2_button = None
                self.option_3_button = None
            elif self.option_2_button.is_left_clicked():
                self.state = "resolution"
                self.resolution_text = self.resolution_options[1]
                self.option_1_button = None
                self.option_2_button = None
                self.option_3_button = None
            elif self.option_3_button.is_left_clicked():
                self.state = "resolution"
                self.resolution_text = self.resolution_options[2]
                self.option_1_button = None
                self.option_2_button = None
                self.option_3_button = None
            
            if not self.resolution_text is None:
                self.resolution_text_rendered = self.font.render(self.resolution_text, False, text_color)
                self.resolution_text_rect = self.resolution_text_rendered.get_rect(topleft = (text_top, text_left))
                self.continue_button = Button(program = self.program,
                                              center_position = (0.5,
                                                             (self.resolution_text_rect.bottom + 1.5 * font_size) / constants.screen_height),
                                              text = "continue",
                                              background_color = textbox_color,
                                              idle_color = button_idle_color,
                                              active_color = button_active_color)
        
        elif self.state == "resolution":
            if self.continue_button.is_left_clicked():
                self.state = "exploration_over"
        
        