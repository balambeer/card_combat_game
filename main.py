import sys
import pygame as pg
import constants
from menu import *
from game import *

class Program:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(constants.resolution)
        self.font = pg.font.Font(None, constants.menu_font_size)
        
        self.menu = MainMenu(self)
        self.game = None
        
        self.state = "menu"
        
    # Check events
    def check_for_quit(self, event):
        return event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)
    
    def check_events(self):
        for event in pg.event.get():
            if self.check_for_quit(event):
                pg.quit()
                sys.exit()
        
    # main funciton
    def run(self):
        while True:
            self.check_events()
            if self.state == "game":
                self.game.update()
                self.game.draw()
                if self.game.state == "game_over":
                    self.state = "menu"
                    self.game = None
            elif self.state == "menu":              
                self.menu.draw()
                self.menu.listen_to_inputs()
            
if __name__ == '__main__':
    program = Program()
    program.run()

