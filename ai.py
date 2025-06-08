import random
import math
import numpy

def select_random(n):
    if n > 0:
        return random.randint(0, n - 1)
    else:
        return 0
    
# utility based selection

utility_weight = 0.25

def utility_when_leading(card):
    if card.suit == "trump":
        suit_utility = 1
    else:
        suit_utility = 1.5
    return (suit_utility * (4 - card.value))

def utility_when_following(card, opponent_card):
    if opponent_card.suit == "trump":
        if card.suit == "trump":
            suit_utility = 1
            if card.value < opponent_card.value:
                value_utility = 1
            else:
                value_utility = -1
        elif card.suit == "shield":
            suit_utility = 1
            value_utility = card.value
        else:
            suit_utility = -1
            value_utility = card.value
    else:
        if card.suit == "trump":
            suit_utility = 1
            value_utility = card.value
        elif card.suit == opponent_card.suit:
            suit_utility = 2
            if card.value < opponent_card.value:
                value_utility = 1
            else:
                value_utility = -1
        else:
            if opponent_card.suit == "spear" or opponent_card.suit == "trump":
                if card.suit == "shield":
                    suit_utility = 2
                    value_utility = card.value
                else:
                    suit_utility = -1
                    value_utility = 1
            else:
                suit_utility = -1
                value_utility = 1
            
    return (suit_utility * value_utility)
    
def select_greedy(opponent_card_played, hand):
    can_play_this_card_list = [ hand.can_play_this_card(card, opponent_card_played) for card in hand.card_list ]
    
    n_cards = len(hand.card_list)
    utility = numpy.zeros(n_cards)
    if opponent_card_played is None:
        for i in range(n_cards):
            utility[i] = math.exp(utility_weight * utility_when_leading(hand.card_list[i]))
    else:
        for i in range(n_cards):
            if ((not any(can_play_this_card_list)) or can_play_this_card_list[i]):
                utility[i] = math.exp(utility_weight * utility_when_following(hand.card_list[i], opponent_card_played))
            else:
                utility[i] = math.exp(-100)
    
    # the off-the-shelf finction returns a list
    choice_list = random.choices(range(n_cards), weights = utility, k = 1)
    if not any(can_play_this_card_list):
        return choice_list[0]
    else:
        # Control the unlikely event of drawing a card that's not playable by redrawing 10 times
        choice_iteration = 1
        while (choice_iteration < 10 and (not can_play_this_card_list[choice_list[0]])):
            choice_list = random.choices(range(n_cards), weights = utility, k = 1)
            choice_iteration += 1
        if can_play_this_card_list[choice_list[0]]:
            return choice_list[0]
        else:
            # If still drew a card that was illegal to play
            return can_play_this_card_list.index(True)
