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
        suit_utility = 2
    else:
        suit_utility = 1
    return (suit_utility * card.value)

def utility_when_following(card, opponent_card):
    if opponent_card.suit == "trump":
        if card.suit == "trump":
            suit_utility = 1
            if card.value > opponent_card.value:
                value_utility = 1
            else:
                value_utility = 0
        else:
            suit_utility = -1
            value_utility = card.value
    else:
        if card.suit == "trump":
            suit_utility = 2
            value_utility = card.value
        elif card.suit == opponent_card.suit:
            suit_utility = 1
            if card.value > opponent_card.value:
                value_utility = 1
            else:
                value_utility = 3 - card.value
        else:
            suit_utility = -1
            value_utility = card.value
            
    return (suit_utility * value_utility)
    
def select_greedy(opponent_card_played, hand):
    n_cards = len(hand.card_list)
    utility = numpy.zeros(n_cards)
    if opponent_card_played is None:
        for i in range(n_cards):
            utility[i] = math.exp(utility_weight * utility_when_leading(hand.card_list[i]))
    else:
        for i in range(n_cards):
            utility[i] = math.exp(utility_weight * utility_when_following(hand.card_list[i], opponent_card_played))
    
    # the off-the-shelf finction returns a list
    choice_list = random.choices(range(n_cards), weights = utility, k = 1)
    return choice_list[0]
