import pygame as pg
import constants
from card import *
from deck import *
from fighter import *
from ui import *

textbox_left = int(0.33 * constants.screen_width)
textbox_top = int(0.33 * constants.screen_height)
textbox_width = constants.screen_width - 2 * textbox_left
textbox_height = constants.screen_height - 2 * textbox_top

font_size = int(0.05 * constants.screen_height)

textbox_color = "gray"
text_color = "black"
button_idle_color = "black"
button_active_color = "white"

class FightScene:
    # Constructor
    def __init__(self, program,
                 player,
                 enemy,
                 next_scene_options):
        self.program = program
        
        self.state = "ongoing"
        self.scene_type = "fight"
        self.next_scene_options = next_scene_options
        self.effect = None
        
        self.is_fighter_1_leading = True
        self.trick_resolved = False

        self.fighter_1 = player
        self.fighter_2 = enemy
        
        self.font = pg.font.Font(None, font_size)
        self.rewards_rect = pg.Rect((textbox_left, textbox_top),
                                    (textbox_width, textbox_height))
        self.rewards_button = None
            
    def check_if_combat_over(self):
        a_player_died = self.fighter_1.hp <= 0 or self.fighter_2.hp <= 0
        final_animations_finished = self.fighter_1.character_animation_frame == 0 and self.fighter_2.character_animation_frame == 0
        
        return a_player_died and final_animations_finished
    
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
    
    # need to pass keywords to match signature of story scene update
    def update(self, story_keywords):
        if self.state == "ongoing":
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
            
            if self.check_if_combat_over():
                self.rewards_button = Button(program = self.program,
                                             center_position = (0.5, 0.5),
                                             font = self.font,
                                             text = "Continue",
                                             background_color = textbox_color,
                                             idle_color = button_idle_color,
                                             active_color = button_active_color)
                self.state = "combat_over"
        if self.state == "combat_over":
            if not self.rewards_button is None:
                if self.rewards_button.is_left_clicked():
                    self.state = "scene_over"
            
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
        if self.state == "combat_over":
            pg.draw.rect(surface = self.program.screen,
                         color = textbox_color,
                         rect = self.rewards_rect)
            pg.draw.rect(surface = self.program.screen,
                         color = "black",
                         rect = self.rewards_rect,
                         width = 2)
            self.rewards_button.draw()

        