import pygame as pg
import constants

menu_background_color = "gray"
menu_text_color = "black"
menu_button_idle_color = "black"
menu_button_active_color = "white"

class Button():
    def __init__(self, program,
                 center_position,
                 text,
                 background_color,
                 idle_color,
                 active_color):
        self.program = program
        
        self.pressed = False
        
        self.background_color = background_color
        self.idle_color = idle_color
        self.active_color = active_color
        
        self.text = text
        self.text_rendered = self.program.font.render(text, False, self.idle_color)
        self.text_rect = self.text_rendered.get_rect(center = (int(center_position[0] * constants.resolution[0]),
                                                               int(center_position[1] * constants.resolution[1])))
        
        self.background_rect = self.text_rect.inflate(0.1 * self.text_rendered.get_width(),
                                                      0.1 * self.text_rendered.get_height())
        
    def draw(self):
        pg.draw.rect(self.program.screen, self.background_color, self.background_rect)
        if self.pressed and self.background_rect.collidepoint(pg.mouse.get_pos()):
            self.text_rendered = self.program.font.render(self.text, False, self.active_color)
            
            pg.draw.rect(self.program.screen, self.active_color, self.background_rect, int(0.1 * self.text_rendered.get_height()))
            self.program.screen.blit(self.text_rendered, self.text_rect)
        else:
            self.text_rendered = self.program.font.render(self.text, False, self.idle_color)
            
            pg.draw.rect(self.program.screen, self.idle_color, self.background_rect, int(0.1 * self.text_rendered.get_height()))
            self.program.screen.blit(self.text_rendered, self.text_rect)
            if self.background_rect.collidepoint(pg.mouse.get_pos()):
                pg.draw.rect(self.program.screen, menu_button_active_color, self.background_rect, 1)
        
    def is_left_clicked(self):
        if pg.mouse.get_pressed()[0]:
            if self.background_rect.collidepoint(pg.mouse.get_pos()):
                self.pressed = True
        if self.pressed:
            if not pg.mouse.get_pressed()[0]:
                self.pressed = False
                return self.background_rect.collidepoint(pg.mouse.get_pos())
            
class ButtonNewGame(Button):
    def __init__(self, program,
                 center_position = (0.5, 0.6),
                 text = "New Game",
                 background_color = menu_background_color,
                 idle_color = menu_button_idle_color,
                 active_color = menu_button_active_color):
        super().__init__(program, center_position, text, background_color, idle_color, active_color)
        
    def listen(self):
        if self.is_left_clicked():
            self.program.game.new_game()
        
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
        
    def update_at_game_over(self):
        pg.mouse.set_visible(True)
        pg.mouse.set_pos((0.5 * constants.screen_width, 0.9 * constants.screen_height))
            
    def listen_to_inputs(self):
        self.new_game_button.listen()
        
