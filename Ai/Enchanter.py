import random, pygame, time

def target(controlled, targets, gens):
    p_e_controled = 0
    choice = random.randint(0, 1)
    for e in controlled:
            if e.__class__.__name__ == "Generator":
                p_e_controled += 1
    if choice == 0 or p_e_controled < 1:
        weighted = []
        if len(gens) == 4:
            for i in range(22):
                if i <= 10:
                    weighted.append(gens[0])
                elif i <= 20:
                    weighted.append(gens[1])
                elif i == 21:
                    weighted.append(gens[2])
                else:
                    weighted.append(gens[3])
        else:
            weighted = gens
        #target a random generator
        for i in range(len(controlled)):
            Targeted = random.choice(weighted)
            controlled[i].target = [Targeted.x, Targeted.y]
    if choice == 1:
        for i in range(len(controlled)):
            #if there are targets, target them
            if len(targets) > 0:
                Targeted = random.choice(targets)
                controlled[i].target = [Targeted.x, Targeted.y]
            #else target the player
            else:
                controlled[i].target = [966, 860]

def summon(mana):
    choice = random.randint(0, 5)
    if choice == 0:
        if mana >= 1:
            return '0'
        else:
            print("Insufficient mana to summon unit 0")
    elif choice == 1:
        if mana >= 3:
            return '1'
        else:
            print("Insufficient mana to summon unit 1")
    elif choice == 2:
        if mana >= 3:
            return '2'
        else:
            print("Insufficient mana to summon unit 2")
    elif choice == 3:
        if mana >= 6:
            return '3'
        else:
            print("Insufficient mana to summon unit 3")
    elif choice == 4:
        if mana >= 8:
            return '4'
        else:
            print("Insufficient mana to summon unit 4")

    elif choice == 5:
        if mana >= 8:
            return '5'
        else:
            print("Insufficient mana to summon unit 5")
    else:
        print("Choice failed")