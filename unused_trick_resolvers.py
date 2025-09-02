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

class TrickResolverAllDamage:
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
                modified_damage.ignores_defense = True
            if self.fight_scene.fighter_1.has_condition("enraged"):
                print("    fighter 1 is enraged, damage +1")
                modified_damage.amount += 1
            if self.fight_scene.fighter_1.has_condition("weakened"):
                print("    fighter 1 is weakened, damage -1")
                modified_damage.amount -= 1
            if self.fight_scene.fighter_2.has_condition("hidden"):
                print("    fighter 2 is hidden, attack misses!")
                modified_damage.amount = 0
                self.fight_scene.fighter_2.remove_condition("hidden")
        else:
            if self.fight_scene.fighter_2.has_condition("hidden"):
                print("    fighter 2 is hidden, sneak attack!")
                modified_damage.ignores_defense = True
            if self.fight_scene.fighter_2.has_condition("enraged"):
                print("    fighter 2 enraged, damage +1")
                modified_damage.amount += 1
            if self.fight_scene.fighter_2.has_condition("enraged"):
                print("    fighter 2 is weakened, damage -1")
                modified_damage.amount -= 1
            if self.fight_scene.fighter_2.has_condition("hidden"):
                print("    fighter 1 is hidden, attack misses!")
                modified_damage.amount = 0
                self.fight_scene.fighter_2.remove_condition("hidden")
                
        return max(0, modified_damage)
    
    def calculate_defense_based_on_conditions(self, did_fighter_1_win_trick):
        if did_fighter_1_win_trick:
            if self.fight_scene.fighter_1.has_condition("hidden"):
                print("    fighter 1 is hidden, defends double!")
                return 2
            else:
                return 1
        else:
            if self.fight_scene.fighter_2.has_condition("hidden"):
                print("    fighter 2 is hidden, defends double!")
                return 2
            else:
                return 1
        
    def designate_attack_actions(self, did_fighter_1_win_trick, damage):
        if did_fighter_1_win_trick:
            print("    fighter 2 takes " + str(damage.amount) + " damage")
            is_killing_blow = not self.fight_scene.fighter_2.can_survive_damage(damage)
            self.fight_scene.fighter_1.perform_attack(is_killing_blow)
            self.fight_scene.fighter_2.take_damage(damage, False)
        else:
            print("    fighter 1 takes " + str(damage.amount) + " damage")
            is_killing_blow = not self.fight_scene.fighter_1.can_survive_damage(damage)
            self.fight_scene.fighter_2.perform_attack(is_killing_blow)
            self.fight_scene.fighter_1.take_damage(damage, False)
            
    def designate_defend_actions(self, did_fighter_1_win_trick, damage, defense_boost):
        if did_fighter_1_win_trick:
            print("    fighter 1 defends " + str(defense_boost))
            print("    fighter 2 takes " + str(damage.amount) + " damage")
            is_killing_blow = self.fight_scene.fighter_2.damage_tolerance() <= damage
            self.fight_scene.fighter_1.perform_attack_defend(defense_boost, is_killing_blow)
            self.fight_scene.fighter_2.take_damage(damage, is_killing_blow)
        else:
            print("    fighter 2 defends " + str(defense_boost))
            print("    fighter 1 takes " + str(damage.amount) + " damage")
            is_killing_blow = self.fight_scene.fighter_1.damage_tolerance() <= damage
            self.fight_scene.fighter_2.perform_attack_defend(defense_boost, is_killing_blow)
            self.fight_scene.fighter_1.take_damage(damage, is_killing_blow)
            
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

    def designate_casting_actions(self, did_fighter_1_win_trick, damage, spell_name):
        spell_effects = self.spell_effect_library(spell_name)
            
        if did_fighter_1_win_trick:
            print("    fighter 1 casts " + spell_name)
        else:
            print("    fighter 2 casts " + spell_name)
            
        if spell_effects[0] == "attack":
            self.designate_attack_actions(did_fighter_1_win_trick, damage)
        elif spell_effects[0] == "defense":
            defense_boost = spell_effects[1]
            self.designate_defend_actions(did_fighter_1_win_trick, damage, defense_boost)
        elif spell_effects[0] == "buff" or spell_effects[0] == "nerf":
            self.designate_attack_actions(did_fighter_1_win_trick, damage)
            if did_fighter_1_win_trick:
                if spell_effects[0] == "buff":
                    print("    fighter 1 gains " + spell_effects[1])
                    self.fight_scene.fighter_1.gain_condition(spell_effects[1])
                else:
                    print("    fighter 2 gains " + spell_effects[1])
                    self.fight_scene.fighter_2.gain_condition(spell_effects[1])
            else:
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

        damage = self.work_out_damage(did_fighter_1_win_trick, winning_card)
        
        if winning_card.suit == "spear":
            self.designate_attack_actions(did_fighter_1_win_trick, damage)
        elif winning_card.suit == "shield":
            defense_boost = self.calculate_defense_based_on_conditions(did_fighter_1_win_trick)
            self.designate_defend_actions(did_fighter_1_win_trick, damage, defense_boost)
        elif winning_card.suit == "mana":
            self.designate_casting_actions(did_fighter_1_win_trick, damage, winning_card.effect)
        elif winning_card.suit == "trump":
            if leading_player_won_trick:
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