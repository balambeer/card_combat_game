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

class TrickResolverSimple:
    def __init__(self, fight_scene):
        self.fight_scene = fight_scene
        
    def determine_damage_and_next_leader(self, leading_card, following_card):
        if leading_card.suit == following_card.suit:
            if leading_card.value > following_card.value:
                return (0, self.fight_scene.is_fighter_1_leading)
            else:
                return (0, not self.fight_scene.is_fighter_1_leading)
        else:
            if following_card.suit == "trump":
                return (0, not self.fight_scene.is_fighter_1_leading)
            else:
                return (leading_card.value, self.fight_scene.is_fighter_1_leading)
            
    def resolve_trick(self):
        print("Trick Resolution:")
        if self.fight_scene.is_fighter_1_leading:
            damage_and_next_lead = self.determine_damage_and_next_leader(self.fight_scene.fighter_1.play_area.card_list[0],
                                                                         self.fight_scene.fighter_2.play_area.card_list[0])
        else:
            damage_and_next_lead = self.determine_damage_and_next_leader(self.fight_scene.fighter_2.play_area.card_list[0],
                                                                         self.fight_scene.fighter_1.play_area.card_list[0])
        
        if self.fight_scene.is_fighter_1_leading:
            if damage_and_next_lead[1]:
                print("    player 2 takes " + str(damage_and_next_lead[0]) + " damage")
                print("    player 1 leads next")
                self.fight_scene.fighter_1.perform_attack(self.fight_scene.fighter_2.damage_tolerance() <= damage_and_next_lead[0])
                self.fight_scene.fighter_2.take_damage(damage_and_next_lead[0], False)
            else:
                print("    player 1 takes " + str(damage_and_next_lead[0]) + " damage")
                print("    player 2 leads next")
                self.fight_scene.fighter_2.perform_riposte(self.fight_scene.fighter_1.damage_tolerance() <= damage_and_next_lead[0])
                self.fight_scene.fighter_1.take_damage(damage_and_next_lead[0], True)
                self.fight_scene.is_fighter_1_leading = not self.fight_scene.is_fighter_1_leading
        else:
            if not damage_and_next_lead[1]:
                print("    player 1 takes " + str(damage_and_next_lead[0]) + " damage")
                print("    player 2 leads next")
                self.fight_scene.fighter_2.perform_attack(self.fight_scene.fighter_1.damage_tolerance() <= damage_and_next_lead[0])
                self.fight_scene.fighter_1.take_damage(damage_and_next_lead[0], False)
            else:
                print("    player 2 takes " + str(damage_and_next_lead[0]) + " damage")
                print("    player 1 leads next")
                self.fight_scene.fighter_1.perform_riposte(self.fight_scene.fighter_2.damage_tolerance() <= damage_and_next_lead[0])
                self.fight_scene.fighter_2.take_damage(damage_and_next_lead[0], True)
                self.fight_scene.is_fighter_1_leading = not self.fight_scene.is_fighter_1_leading

class TrickResolverActions:
    def __init__(self, fight_scene):
        self.fight_scene = fight_scene
                
    def did_leading_player_win_trick(self, leading_card, trailing_card):
        if leading_card.suit == trailing_card.suit:
            return leading_card.value <= trailing_card.value
        else:
            return (not trailing_card.suit == "trump")
        
    def modify_damage_based_on_conditions(self, did_fighter_1_win_trick, damage):
        modified_damage = damage
        if did_fighter_1_win_trick:
            if self.fight_scene.fighter_1.has_condition("hidden"):
                print("    fighter 1 is hidden, sneak attack!")
                modified_damage = 2 * modified_damage
            if self.fight_scene.fighter_1.has_condition("enraged"):
                print("    fighter 1 is enraged, damage +1")
                modified_damage += 1
            if self.fight_scene.fighter_1.has_condition("weakened"):
                print("    fighter 1 is weakened, damage -1")
                modified_damage -= 1
            if self.fight_scene.fighter_2.has_condition("hidden"):
                print("    fighter 2 is hidden, attack misses!")
                modified_damage = 0
                self.fight_scene.fighter_2.remove_condition("hidden")
        else:
            if self.fight_scene.fighter_2.has_condition("hidden"):
                print("    fighter 2 is hidden, sneak attack!")
                modified_damage = 2 * modified_damage
            if self.fight_scene.fighter_2.has_condition("enraged"):
                print("    fighter 2 enraged, damage +1")
                modified_damage += 1
            if self.fight_scene.fighter_2.has_condition("enraged"):
                print("    fighter 2 is weakened, damage -1")
                modified_damage -= 1
            if self.fight_scene.fighter_2.has_condition("hidden"):
                print("    fighter 1 is hidden, attack misses!")
                modified_damage = 0
                self.fight_scene.fighter_2.remove_condition("hidden")
                
        return max(0, modified_damage)
        
    def designate_attack_actions(self, did_fighter_1_win_trick, damage):
        if did_fighter_1_win_trick:
            print("    fighter 2 takes " + str(damage) + " damage")
            self.fight_scene.fighter_1.perform_attack(self.fight_scene.fighter_2.damage_tolerance() <= damage)
            self.fight_scene.fighter_2.take_damage(damage, False)
        else:
            print("    fighter 1 takes " + str(damage) + " damage")
            self.fight_scene.fighter_2.perform_attack(self.fight_scene.fighter_1.damage_tolerance() <= damage)
            self.fight_scene.fighter_1.take_damage(damage, False)
            
    def designate_defend_actions(self, did_fighter_1_win_trick, defense):
        if did_fighter_1_win_trick:
            print("    fighter 1 defends " + str(defense))
            self.fight_scene.fighter_1.perform_defend(defense)
            self.fight_scene.fighter_2.perform_flatfooted()
        else:
            print("    fighter 2 defends " + str(defense))
            self.fight_scene.fighter_2.perform_defend(defense)
            self.fight_scene.fighter_1.perform_flatfooted()
            
    # Returns tuple (spell_type, spell_effect)
    def spell_effect_library(self, spell_name):
        # attack spells
        if spell_name == "bolt":
            return ("attack", 1)
        elif spell_name == "chill touch":
            return ("attack", 1)
        elif spell_name == "howl":
            return ("attack", 2)
        
        # defense spells
        elif spell_name == "mage armor":
            return ("defense", 2)
            
        # buffs
        elif spell_name == "hide":
            return ("buff", "hidden")
        elif spell_name == "rage":
            return ("buff", "enraged")
        
        # nerfs
        elif spell_name == "poison":
            return ("nerf", "poisoned")
        elif spell_name == "weakness":
            return ("nerf", "weakened")
        
        else:
            raise Exception("Unknown spell")
            
    def designate_casting_actions(self, did_fighter_1_win_trick, spell_name):
        spell_effects = self.spell_effect_library(spell_name)
            
        if did_fighter_1_win_trick:
            print("    fighter 1 casts " + spell_name)
        else:
            print("    fighter 2 casts " + spell_name)
            
        if spell_effects[0] == "attack":
            damage = self.modify_damage_based_on_conditions(did_fighter_1_win_trick,
                                                            spell_effects[1])
            self.designate_attack_actions(did_fighter_1_win_trick, damage)
        elif spell_effects[0] == "defense":
            self.designate_defend_actions(did_fighter_1_win_trick, max(1, spell_effects[1] // 2))
        elif spell_effects[0] == "buff" or spell_effects[0] == "nerf":
            if did_fighter_1_win_trick:
                # animations
                self.fight_scene.fighter_1.perform_cast()
                self.fight_scene.fighter_2.perform_flatfooted()
                
                # mechanical stuff
                if spell_effects[0] == "buff":
                    print("    fighter 1 gains " + spell_effects[1])
                    self.fight_scene.fighter_1.gain_condition(spell_effects[1])
                else:
                    print("    fighter 2 gains " + spell_effects[1])
                    self.fight_scene.fighter_2.gain_condition(spell_effects[1])
            else:
                # animations
                self.fight_scene.fighter_2.perform_cast()
                self.fight_scene.fighter_1.perform_flatfooted()
        
                # mechanical stuff
                if spell_effects[0] == "buff":
                    print("    fighter 2 gains " + spell_effects[1])
                    self.fight_scene.fighter_2.gain_condition(spell_effects[1])
                else:
                    print("    fighter 1 gains " + spell_effects[1])
                    self.fight_scene.fighter_1.gain_condition(spell_effects[1])
        else:
            raise Exception("Unknown spell type")
            
    def designate_riposte_actions(self, did_fighter_1_win_trick):
        if did_fighter_1_win_trick:
            print("    fighter 1 takes initiative")
            self.fight_scene.fighter_1.perform_riposte(self.fight_scene.fighter_2.damage_tolerance() <= 0)
            self.fight_scene.fighter_2.take_damage(0, True)
        else:
            print("    fighter 2 takes initiative")
            self.fight_scene.fighter_2.perform_riposte(self.fight_scene.fighter_1.damage_tolerance() <= 0)
            self.fight_scene.fighter_1.take_damage(0, True)
        
    def designate_actions(self, leading_player_won_trick, leading_card, trailing_card):
        did_fighter_1_win_trick = ( (self.fight_scene.is_fighter_1_leading and
                                     leading_player_won_trick) or
                                   ( (not self.fight_scene.is_fighter_1_leading) and
                                     (not leading_player_won_trick)))
        if leading_player_won_trick:
            winning_card = leading_card
            losing_card = trailing_card
        else:
            winning_card = trailing_card
            losing_card = leading_card
        
        if winning_card.suit == "spear":
            damage = self.modify_damage_based_on_conditions(did_fighter_1_win_trick, winning_card.value)
            if losing_card.suit == "shield":
                damage = max(0, damage - losing_card.value)
            self.designate_attack_actions(did_fighter_1_win_trick, damage)
        elif winning_card.suit == "shield":
            defense = max(1, winning_card.value // 2)
            self.designate_defend_actions(did_fighter_1_win_trick, defense)
        elif winning_card.suit == "mana":
            spell_name = winning_card.effect
            self.designate_casting_actions(did_fighter_1_win_trick, spell_name)
        elif winning_card.suit == "trump":
            if leading_player_won_trick:
                damage = self.modify_damage_based_on_conditions(did_fighter_1_win_trick, winning_card.value)
                if losing_card.suit == "shield":
                    damage = max(0, damage - losing_card.value)
                self.designate_attack_actions(did_fighter_1_win_trick, damage)
            else:
                self.designate_riposte_actions(did_fighter_1_win_trick)
        else:
            raise Exception("Winning suit must be one of spear, shield, mana, trump.")

    def resolve_trick(self):
        print("--- new trick ---")
        if self.fight_scene.is_fighter_1_leading:
            leading_card = self.fight_scene.fighter_1.play_area.card_list[0]
            trailing_card = self.fight_scene.fighter_2.play_area.card_list[0]        
        else:
            leading_card = self.fight_scene.fighter_2.play_area.card_list[0]
            trailing_card = self.fight_scene.fighter_1.play_area.card_list[0]
            
        leading_player_won_trick = self.did_leading_player_win_trick(leading_card, trailing_card)
        print("  leading player played " + str(leading_card.value) + " of " + leading_card.suit)
        print("  trailing player played " + str(trailing_card.value) + " of " + trailing_card.suit)
        print("    leading player won the trick: " + str(leading_player_won_trick))
        
        self.designate_actions(leading_player_won_trick,
                               leading_card,
                               trailing_card)
                
        if not leading_player_won_trick:
            self.fight_scene.is_fighter_1_leading = not self.fight_scene.is_fighter_1_leading
        
        if self.fight_scene.is_fighter_1_leading:
            print("    fighter 1 leads next")
        else:
            print("    fighter_2_leads next")
        

class FightScene:
    # Constructor
    def __init__(self, program,
                 location_index,
                 player,
                 enemy,
                 next_scene_options):
        self.program = program
        
        self.state = "ongoing"
        self.scene_type = "fight"
        self.scene_location = location_index
        self.next_scene_options = next_scene_options
        self.effect = None
        # self.trick_resolver = TrickResolverSimple(self)
        self.trick_resolver = TrickResolverActions(self)
        
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
                self.trick_resolver.resolve_trick()

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

        