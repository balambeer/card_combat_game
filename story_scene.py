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

class StoryScene:
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
        self.encounter_text_rendered_list = self.render_text_to_multiple_lines(self.encounter_text)
        self.encounter_text_rect_list = self.get_rendered_rects(self.encounter_text_rendered_list)
        
        self.option_1_button = Button(program = program,
                                      center_position = (0.5,
                                                         (self.encounter_text_rect_list[-1].bottom + 1.5 * font_size) / constants.screen_height),
                                      font = self.font,
                                      text = option_1_text,
                                      background_color = textbox_color,
                                      idle_color = button_idle_color,
                                      active_color = button_active_color)
        self.option_2_button = Button(program = program,
                                      center_position = (0.5,
                                                         (self.option_1_button.text_rect.bottom + 1.5 * font_size) / constants.screen_height),
                                      font = self.font,
                                      text = option_2_text,
                                      background_color = textbox_color,
                                      idle_color = button_idle_color,
                                      active_color = button_active_color)
        self.option_3_button = Button(program = program,
                                      center_position = (0.5,
                                                         (self.option_2_button.text_rect.bottom + 1.5 * font_size) / constants.screen_height),
                                      font = self.font,
                                      text = option_3_text,
                                      background_color = textbox_color,
                                      idle_color = button_idle_color,
                                      active_color = button_active_color)
        
        self.resolution_options = resolution_options
        self.resolution_text = None
        self.continue_button = None
        
    def render_next_line(self, remaining_text):
        text_rendered = self.font.render(remaining_text, False, text_color)
        text_rendered_rect = text_rendered.get_rect()
        text_max_width = self.textbox_rect.width - 2 * text_margin
        
        if text_rendered_rect.width <= text_max_width:
            return [text_rendered, None]
        else:
            remaining_words = remaining_text.split(sep = " ")
            n_words = len(remaining_words)

            n_words_to_include = min(n_words, int(n_words * (text_rendered_rect.width / text_max_width)))
            text_to_render = " ".join(remaining_words[:n_words_to_include])
            text_rendered = self.font.render(text_to_render, False, text_color)
            text_rendered_rect = text_rendered.get_rect()
            text_to_render_finalized = False
            include_more_words = text_rendered_rect.width < text_max_width
            
            while not text_to_render_finalized:
                if include_more_words:
                    n_words_to_include += 1
                else:
                    n_words_to_include -= 1
                text_to_render = " ".join(remaining_words[:n_words_to_include])
                text_rendered = self.font.render(text_to_render, False, text_color)
                text_rendered_rect = text_rendered.get_rect()
                
                if include_more_words:
                    if text_rendered_rect.width > text_max_width or n_words_to_include == (n_words - 1):
                        n_words_to_include -= 1
                        text_to_render_finalized = True
                else:
                    if text_rendered_rect.width < text_max_width or n_words_to_include == 1:
                        text_to_render_finalized = True
                    
            text_to_render = " ".join(remaining_words[:n_words_to_include])
            text_rendered = self.font.render(text_to_render, False, text_color)
            return [text_rendered, " ".join(remaining_words[n_words_to_include:])]
                
    def render_text_to_multiple_lines(self, text):
        crap = self.render_next_line(text)
        text_rendered_list = [crap[0]]
        while not crap[1] is None:
            crap = self.render_next_line(crap[1])
            text_rendered_list.append(crap[0])
        
        return text_rendered_list
    
    def get_rendered_rects(self, rendered_text_list):
        text_rect_list = [rendered_text_list[0].get_rect(topleft = (text_top, text_left))]
        for i in range(len(rendered_text_list)):
            if i > 0:
                new_text_rect = rendered_text_list[i].get_rect(topleft = text_rect_list[-1].bottomleft)
                text_rect_list.append(new_text_rect)
                
        return text_rect_list
        
    def draw(self):
        self.program.screen.fill(background_color)
        
        pg.draw.rect(self.program.screen,
                     textbox_color,
                     self.textbox_rect)
        if self.state == "waiting_for_input":
            for i in range(len(self.encounter_text_rendered_list)):
                self.program.screen.blit(self.encounter_text_rendered_list[i],
                                         self.encounter_text_rect_list[i])
            self.option_1_button.draw()
            self.option_2_button.draw()
            self.option_3_button.draw()
        elif self.state == "resolution":
            for i in range(len(self.resolution_text_rendered_list)):
                self.program.screen.blit(self.resolution_text_rendered_list[i],
                                         self.resolution_text_rect_list[i])
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
                self.resolution_text_rendered_list = self.render_text_to_multiple_lines(self.resolution_text)
                self.resolution_text_rect_list = self.get_rendered_rects(self.resolution_text_rendered_list)
                self.continue_button = Button(program = self.program,
                                              center_position = (0.5,
                                                             (self.resolution_text_rect_list[-1].bottom + 1.5 * font_size) / constants.screen_height),
                                              font = self.font,
                                              text = "continue",
                                              background_color = textbox_color,
                                              idle_color = button_idle_color,
                                              active_color = button_active_color)
        
        elif self.state == "resolution":
            if self.continue_button.is_left_clicked():
                self.state = "exploration_over"
        
        