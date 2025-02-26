import pygame as pg
import constants
from game import *
from ui import *

menu_background_color = "gray"
menu_text_color = "black"
menu_button_idle_color = "black"
menu_button_active_color = "white"
            
class ButtonNewGame(Button):
    def __init__(self, program,
                 center_position = (0.5, 0.6),
                 text = "New Game",
                 background_color = menu_background_color,
                 idle_color = menu_button_idle_color,
                 active_color = menu_button_active_color):
        super().__init__(program, center_position, program.font, text, background_color, idle_color, active_color)
        
    def listen(self):
        if self.is_left_clicked():
            self.program.game = Game(self.program)
            self.program.state = "game"
        
class Menu():
    def __init__(self, program):
        self.program = program
        
        self.game_title = self.program.font.render("Game Title", False, menu_text_color)
        self.game_title_rect = self.game_title.get_rect(center = (0.5 * constants.screen_width, 0.2 * constants.screen_height))
        
        self.new_game_button = ButtonNewGame(self.program)
        
    def draw(self):
        pg.display.flip()
        self.program.screen.fill(menu_background_color)
        self.program.screen.blit(self.game_title, self.game_title_rect)
        self.new_game_button.draw()
        
    # Not needed now (mouse is visible in-game as well)
    def update_at_game_over(self):
        pg.mouse.set_visible(True)
        pg.mouse.set_pos((0.5 * constants.screen_width, 0.9 * constants.screen_height))
            
    def listen_to_inputs(self):
        self.new_game_button.listen()
        
