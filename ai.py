import random

def select_random(n):
    if n > 0:
        return random.randint(0, n - 1)
    else:
        return 0