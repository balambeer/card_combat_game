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
                               is_human_controlled = True,
                               hp = 10,
                               card_list = [(1, "spades"), (2, "spades"), (3, "spades"),
                                            # (1, "hearts"), (2, "hearts"), (3, "hearts"),
                                            (1, "clubs"), (2, "clubs"), (3, "clubs"),
                                            (1, "diamonds"), (2, "diamonds"), (3, "diamonds"),
                                            ],
                               show_hand = True,
                               color = "cornflowerblue")
        self.player_2 = Player(game = self,
                               is_left_player = False,
                               is_human_controlled = False,
                               hp = 10,
                               card_list = [(1, "spades"), (2, "spades"), (3, "spades"),
                                            (1, "hearts"), (2, "hearts"), (3, "hearts"),
                                            # (1, "clubs"), (2, "clubs"), (3, "clubs"),
                                            (1, "diamonds"), (2, "diamonds"), (3, "diamonds"),
                                            ],
                               show_hand = False,
                               color = "tomato")
        
    # Update game state
    def check_game_over_condition(self):
        a_player_died = self.player_1.hp <= 0 or self.player_2.hp <= 0
        final_animations_finished = self.player_1.character_animation_frame == 0 and self.player_2.character_animation_frame == 0
        
        return a_player_died and final_animations_finished and pg.mouse.get_pressed()[0]
    
    def determine_damage_and_next_leader(self, leading_card, following_card):
        if leading_card.suit == following_card.suit:
            if leading_card.value > following_card.value:
                return (0, self.is_player_1_leading)
            else:
                return (0, not self.is_player_1_leading)
        else:
            if following_card.suit == "diamonds":
                return (following_card.value, not self.is_player_1_leading)
            else:
                return (leading_card.value, self.is_player_1_leading)
    
    def resolve_trick(self):
        print("Trick Resolution:")
        if self.is_player_1_leading:
            damage_and_next_lead = self.determine_damage_and_next_leader(self.player_1.play_area.card_list[0],
                                                                         self.player_2.play_area.card_list[0])
        else:
            damage_and_next_lead = self.determine_damage_and_next_leader(self.player_2.play_area.card_list[0],
                                                                         self.player_1.play_area.card_list[0])
                  
        if self.is_player_1_leading:
            if damage_and_next_lead[1]:
                print("    player 2 takes " + str(damage_and_next_lead[0]) + " damage")
                print("    player 1 leads next")
                self.player_1.perform_attack(self.player_2.hp <= damage_and_next_lead[0])
                self.player_2.take_damage(damage_and_next_lead[0], False)
            else:
                print("    player 1 takes " + str(damage_and_next_lead[0]) + " damage")
                print("    player 2 leads next")
                self.player_2.perform_riposte(self.player_1.hp <= damage_and_next_lead[0])
                self.player_1.take_damage(damage_and_next_lead[0], True)
                self.is_player_1_leading = not self.is_player_1_leading
        else:
            if not damage_and_next_lead[1]:
                print("    player 1 takes " + str(damage_and_next_lead[0]) + " damage")
                print("    player 2 leads next")
                self.player_2.perform_attack(self.player_1.hp <= damage_and_next_lead[0])
                self.player_1.take_damage(damage_and_next_lead[0], False)
            else:
                print("    player 2 takes " + str(damage_and_next_lead[0]) + " damage")
                print("    player 1 leads next")
                self.player_1.perform_riposte(self.player_2.hp <= damage_and_next_lead[0])
                self.player_2.take_damage(damage_and_next_lead[0], True)
                self.is_player_1_leading = not self.is_player_1_leading            
    
    def update_game_state(self):
        if self.check_game_over_condition():
            self.program.menu.update_at_game_over()
            self.game_over = True
        else:
            self.delta_time = self.clock.tick(settings.fps)
            # manage players
            if self.player_1.state == "waiting" and self.player_2.state == "waiting":
                if self.is_player_1_leading:
                    self.player_1.state = "my_turn"
                else:
                    self.player_2.state = "my_turn"
            elif self.player_1.state == "waiting" and self.player_2.state == "played_card":
                self.player_1.state = "my_turn"
            elif self.player_1.state == "played_card" and self.player_2.state == "waiting":
                self.player_2.state = "my_turn"
            elif self.player_1.state == "played_card" and self.player_2.state == "played_card":
                self.resolve_trick()

            self.player_1.update(self.is_player_1_leading)
            self.player_2.update(not self.is_player_1_leading)
            
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
        self.player_1.display()
        self.player_2.display()

        