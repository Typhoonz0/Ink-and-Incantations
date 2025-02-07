import random, pygame, time

def target(controlled, targets, gens):
    choice = random.randint(0, 1)
    if choice == 0:
        for i in range(len(controlled)):
            Targeted = random.choice(gens)
            controlled[i].target = [Targeted.x, Targeted.y]
    if choice == 1:
        for i in range(len(controlled)):
            Targeted = random.choice(targets)
            controlled[i].target = [Targeted.x, Targeted.y]

def summon(mana):
    choice = random.randint(0, 5)
    if choice == 0:
        if mana >= 1:
            return '0'
    if choice == 1:
        if mana >= 3:
            return '1'
    if choice == 2:
        if mana >= 3:
            return '2'
    if choice == 3:
        if mana >= 6:
            return '3'
    if choice == 4:
        if mana >= 8:
            return '4'
    if choice == 5:
        if mana >= 8:
            return '5'