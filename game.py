import pygame as pg
import settings
import support
from card import *
from deck import *
from player import *

class Game:
    # Constructor
    def __init__(self, program):
        self.program = program
        
        self.game_over = True
        self.game_over_frames = 0
        
    def new_game(self):
        self.game_over = False
        self.clock = pg.time.Clock()
        self.delta_time = 0
        
        self.is_player_1_leading = True
        self.trick_resolved = False

        self.player_1 = Player(game = self,
                               is_left_player = True,
                               hp = 10,
                               card_list = [(1, "spades"), (2, "spades"), (3, "spades"),
                                            # (1, "hearts"), (2, "hearts"), (3, "hearts"),
                                            (1, "clubs"), (2, "clubs"), (3, "clubs"),
                                            (1, "diamonds"), (2, "diamonds"), (3, "diamonds"),
                                            ],
                               color = "cornflowerblue")
        self.player_2 = Player(game = self,
                               is_left_player = False,
                               hp = 10,
                               card_list = [(1, "spades"), (2, "spades"), (3, "spades"),
                                            (1, "hearts"), (2, "hearts"), (3, "hearts"),
                                            # (1, "clubs"), (2, "clubs"), (3, "clubs"),
                                            (1, "diamonds"), (2, "diamonds"), (3, "diamonds"),
                                            ],
                               color = "tomato")
        
    # Update game state
    def check_game_over_condition(self):
        a_player_died = self.player_1.hp <= 0 or self.player_2.hp <= 0
        return a_player_died or pg.mouse.get_pressed()[2]
    
    def resolve_trick(self):
        print("Trick Resolution:")
        if self.is_player_1_leading:
            leading_suit = self.player_1.play_area.card_list[0].suit
            leading_value = self.player_1.play_area.card_list[0].value
            following_suit = self.player_2.play_area.card_list[0].suit
            following_value = self.player_2.play_area.card_list[0].value
            print("  Player 1 led with " + str(leading_value) + " of " + leading_suit)
            print("  Player 2 followed with " + str(following_value) + " of " + following_suit)
        else:
            leading_suit = self.player_2.play_area.card_list[0].suit
            leading_value = self.player_2.play_area.card_list[0].value
            following_suit = self.player_1.play_area.card_list[0].suit
            following_value = self.player_1.play_area.card_list[0].value
            print("  Player 2 led with " + str(leading_value) + " of " + leading_suit)
            print("  Player 1 followed with " + str(following_value) + " of " + following_suit)
        
        if leading_suit == following_suit:
            if leading_value > following_value:
                leading_player_won = True
            else:
                leading_player_won = False
            damage = 0
        if not leading_suit == following_suit:
            if not following_suit == "diamonds":
                leading_player_won = True
                damage = leading_value
            else:
                leading_player_won = False
                damage = following_value
                  
        if self.is_player_1_leading:
            if leading_player_won:
                print("    player 2 takes " + str(damage) + " damage")
                print("    player 1 leads next")
                self.player_2.take_damage(damage)
            else:
                print("    player 1 takes " + str(damage) + " damage")
                print("    player 2 leads next")
                self.player_1.take_damage(damage)
                self.is_player_1_leading = not self.is_player_1_leading
        else:
            if leading_player_won:
                print("    player 1 takes " + str(damage) + " damage")
                print("    player 2 leads next")
                self.player_1.take_damage(damage)
            else:
                print("    player 2 takes " + str(damage) + " damage")
                print("    player 1 leads next")
                self.player_2.take_damage(damage)
                self.is_player_1_leading = not self.is_player_1_leading            
    
    def update_game_state(self):
        if self.check_game_over_condition():
            self.program.menu.update_at_game_over()
            self.game_over = True
        else:
            self.delta_time = self.clock.tick(settings.fps)
            # update game objects
            if (self.is_player_1_leading and not self.player_1.played_card) or (not self.is_player_1_leading and self.player_2.played_card):
                self.player_1.is_my_turn = True
            if (not self.is_player_1_leading and not self.player_2.played_card) or (self.is_player_1_leading and self.player_1.played_card):
                self.player_2.is_my_turn = True
            
            if self.player_1.played_card and self.player_2.played_card and not self.trick_resolved:
                self.resolve_trick()
                self.trick_resolved = True

            self.player_1.update()
            self.player_2.update()
                
            if (self.is_player_1_leading and self.player_1.listening_to_inputs) or (not self.is_player_1_leading and self.player_2.listening_to_inputs):
                self.trick_resolved = False
            
        pg.display.set_caption(f'{self.clock.get_fps(): .1f}')
        
    # Update screen
    def draw_background(self):
        pg.draw.rect(self.program.screen,
                     "lightskyblue1",
                     pg.Rect(0, 0, settings.screen_width, settings.battle_sky_height))
        pg.draw.rect(self.program.screen,
                     "olivedrab3",
                     pg.Rect(0, settings.battle_sky_height,
                             settings.screen_width, settings.screen_height - settings.battle_sky_height))
        
    def draw(self):
        pg.display.flip()
        self.draw_background()
        self.player_1.draw()
        self.player_2.draw()

        