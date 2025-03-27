import pygame as pg
import constants
import support
from card import *
from deck import *
from fighter import *

class FightScene:
    # Constructor
    def __init__(self, program,
                 player,
                 enemy,
                 next_scene):
        self.program = program
        
        self.state = "ongoing"
        self.scene_type = "fight"
        self.next_scene = next_scene
        self.effect = None
        
        self.is_fighter_1_leading = True
        self.trick_resolved = False

        self.fighter_1 = player
        self.fighter_2 = enemy
        
    # Update game state
    def check_combat_over_condition(self):
        a_player_died = self.fighter_1.hp <= 0 or self.fighter_2.hp <= 0
        final_animations_finished = self.fighter_1.character_animation_frame == 0 and self.fighter_2.character_animation_frame == 0
        
        return a_player_died and final_animations_finished and pg.mouse.get_pressed()[0]
    
    def determine_damage_and_next_leader(self, leading_card, following_card):
        if leading_card.suit == following_card.suit:
            if leading_card.value > following_card.value:
                return (0, self.is_fighter_1_leading)
            else:
                return (0, not self.is_fighter_1_leading)
        else:
            if following_card.suit == "trump":
                return (following_card.value, not self.is_fighter_1_leading)
            else:
                return (leading_card.value, self.is_fighter_1_leading)
    
    def resolve_trick(self):
        print("Trick Resolution:")
        if self.is_fighter_1_leading:
            damage_and_next_lead = self.determine_damage_and_next_leader(self.fighter_1.play_area.card_list[0],
                                                                         self.fighter_2.play_area.card_list[0])
        else:
            damage_and_next_lead = self.determine_damage_and_next_leader(self.fighter_2.play_area.card_list[0],
                                                                         self.fighter_1.play_area.card_list[0])
        
        if self.is_fighter_1_leading:
            if damage_and_next_lead[1]:
                print("    player 2 takes " + str(damage_and_next_lead[0]) + " damage")
                print("    player 1 leads next")
                self.fighter_1.perform_attack(self.fighter_2.damage_tolerance() <= damage_and_next_lead[0])
                self.fighter_2.take_damage(damage_and_next_lead[0], False)
            else:
                print("    player 1 takes " + str(damage_and_next_lead[0]) + " damage")
                print("    player 2 leads next")
                self.fighter_2.perform_riposte(self.fighter_1.damage_tolerance() <= damage_and_next_lead[0])
                self.fighter_1.take_damage(damage_and_next_lead[0], True)
                self.is_fighter_1_leading = not self.is_fighter_1_leading
        else:
            if not damage_and_next_lead[1]:
                print("    player 1 takes " + str(damage_and_next_lead[0]) + " damage")
                print("    player 2 leads next")
                self.fighter_2.perform_attack(self.fighter_1.damage_tolerance() <= damage_and_next_lead[0])
                self.fighter_1.take_damage(damage_and_next_lead[0], False)
            else:
                print("    player 2 takes " + str(damage_and_next_lead[0]) + " damage")
                print("    player 1 leads next")
                self.fighter_1.perform_riposte(self.fighter_2.damage_tolerance() <= damage_and_next_lead[0])
                self.fighter_2.take_damage(damage_and_next_lead[0], True)
                self.is_fighter_1_leading = not self.is_fighter_1_leading            
    
    # def update_game_state(self):
    def update(self):
        if self.check_combat_over_condition():
            self.state = "scene_over"
        else:
            self.program.game.delta_time = self.program.game.clock.tick(constants.fps)
            # manage players
            if self.fighter_1.state == "waiting" and self.fighter_2.state == "waiting":
                if self.is_fighter_1_leading:
                    self.fighter_1.state = "my_turn"
                else:
                    self.fighter_2.state = "my_turn"
            elif self.fighter_1.state == "waiting" and self.fighter_2.state == "played_card":
                self.fighter_1.state = "my_turn"
            elif self.fighter_1.state == "played_card" and self.fighter_2.state == "waiting":
                self.fighter_2.state = "my_turn"
            elif self.fighter_1.state == "played_card" and self.fighter_2.state == "played_card":
                self.resolve_trick()

            if len(self.fighter_1.play_area.card_list) == 1:
                fighter_1_card_played = self.fighter_1.play_area.card_list[0]
            else:
                fighter_1_card_played = None
            if len(self.fighter_2.play_area.card_list) == 1:
                fighter_2_card_played = self.fighter_2.play_area.card_list[0]
            else:
                fighter_2_card_played = None
            self.fighter_1.update(self.is_fighter_1_leading, fighter_2_card_played)
            self.fighter_2.update(not self.is_fighter_1_leading, fighter_1_card_played)
            
        pg.display.set_caption(f'{self.program.game.clock.get_fps(): .1f}')
        
    # Update screen
    def draw_background(self):
        pg.draw.rect(self.program.screen,
                     "lightskyblue1",
                     pg.Rect(0, 0, constants.screen_width, constants.battle_sky_height))
        pg.draw.rect(self.program.screen,
                     "olivedrab3",
                     pg.Rect(0, constants.battle_sky_height,
                             constants.screen_width, constants.screen_height - constants.battle_sky_height))
        
    def draw(self):
        self.draw_background()
        self.fighter_1.display()
        self.fighter_2.display()

        