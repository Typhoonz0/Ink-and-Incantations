import Units, pygame, time
from Ai import Enchanter
from pygame.locals import *


def BatStart():
    player_mana = 5
    Enchanter_mana = 5
    player_HP = 20
    Enchanter_HP=20


    icon = pygame.image.load("Assets\Icon.png")
    BattleGround = pygame.image.load("Assets\Sprites\pixil-frame-0.png")
    inkblot = pygame.image.load("Assets\Sprites\InkBlot.png")

    running = True
    clock = pygame.time.Clock()
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()
    pygame.display.set_icon(icon)
    gameDisplay = pygame.display.set_mode((1920,1080))
    pygame.display.set_caption('Ink and Incantations')
    gameDisplay.fill((0,0,0))
    pygame.mixer.music.load("Assets\Music\last-fight-dungeon-synth-music-281592.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(1)

    SpeechFont = pygame.font.Font("""Assets\Fonts\Speech.ttf""", 30)
    HPFont = pygame.font.Font("""Assets\Fonts\Speech.ttf""", 60)
    Ready = SpeechFont.render('Are you Ready, Mage?', True, (255, 150, 255))
    Begin = SpeechFont.render('Let us begin.', True, (255, 150, 255))

    # enchanters speech
    for i in range(0, 5):
        gameDisplay.fill((0, 0, 0))
        if i == 1:
            gameDisplay.blit(Ready, (800, 900))
        if i == 3:
            gameDisplay.blit(Begin, (870, 900))
        pygame.display.flip()
        
        clock.tick(100)
        if i != 2 or i != 0:
            time.sleep(4)
        else:
            time.sleep(2)
        
    # fade in the background
    a = 0
    for i in range(255):
        gameDisplay.fill((0, 0, 0))
        a += 1
        BattleGround.set_alpha(a)
        gameDisplay.blit(BattleGround, (460, 0))
        pygame.display.flip()

    # fade in the UI + pumps    
    time.sleep(1)
    runnint = True
    Pumps = [Units.Generator((760, 315)), Units.Generator((1120, 315)), Units.Generator((760, 650)), Units.Generator((1120, 650))]
    Hp = HPFont.render(str(player_HP) + ":" + str(Enchanter_HP), True, (255, 150, 255))
    summon_UI = pygame.image.load("Assets\Sprites\Selecetion grid.png")
    a = 0
    manaCounter = pygame.image.load("Assets\Sprites\Mana_counter\\5.png")
    for i in range(255):
        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(BattleGround, (460, 0))
        a += 1
        for p in Pumps:
            p.Asset.set_alpha(a)
            gameDisplay.blit(p.Asset, (p.x, p.y))
        manaCounter.set_alpha(a)
        gameDisplay.blit(manaCounter, (200, 850))
        Hp.set_alpha(a)
        gameDisplay.blit(Hp, (200, 200))
        summon_UI.set_alpha(a)
        gameDisplay.blit(summon_UI, (1600, 200))
        pygame.display.flip()

    # loading Vars
    cursor_img = pygame.image.load("Assets\Sprites\Mouse.png")
    pygame.mouse.set_visible(False)
    cursor_img_rect = cursor_img.get_rect()
    startselect = (960, 540)
    endselect = (0, 0)
    frame = 0
    Selecting = False
    selected = []
    friendly = []
    enemy = []
    inkblots = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            # start of selection
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if 598 < event.pos[0] < 1322 and not Selecting and 154 < event.pos[1] < 876:
                    startselect = event.pos
                    Selecting = True
                elif 1600 < event.pos[0] < 1920 and 200 < event.pos[1] < 940:
                    if player_mana >= 1 and event.pos[1] in range(200, 323, 1):
                        friendly.append(Units.Footman([966, 860]))
                        friendly[-1].target = [966, 860]
                        player_mana -= 1
                    elif player_mana >= 3 and event.pos[1] in range(323, 446, 1):
                        friendly.append(Units.Horse([966, 860]))
                        friendly[-1].target = [966, 860]
                        player_mana -= 3
                    elif player_mana >= 3 and event.pos[1] in range(446, 569, 1):
                        friendly.append(Units.Soldier([966, 860]))
                        friendly[-1].target = [966, 860]
                        player_mana -= 3
                    elif player_mana >= 6 and event.pos[1] in range(569, 692, 1):
                        friendly.append(Units.Summoner([966, 860]))
                        friendly[-1].target = [966, 860]
                        player_mana -= 6
                    elif player_mana >= 8 and event.pos[1] in range(692, 815, 1):
                        friendly.append(Units.Runner([966, 860]))
                        friendly[-1].target = [966, 860]
                        player_mana -= 8
                    elif player_mana >= 8 and event.pos[1] in range(815, 940, 1):
                        friendly.append(Units.Tank([966, 860]))
                        friendly[-1].target = [966, 860]
                        player_mana -= 8
                        
           # end of selection
            if event.type == MOUSEBUTTONUP and event.button == 1:
                # checking if in bounds of the field
                if 598 < event.pos[0] < 1322 and Selecting and 154 < event.pos[1] < 876:
                    endselect = event.pos
                    Selecting = False
                    selected = []
                    for f in friendly:
                        if startselect[0] <= f.x <= endselect[0] and startselect[1] <= f.y <= endselect[1]:
                            selected.append(f)
                elif Selecting:
                    # if not in bounds, find which co-ords are in bounds, if none, find the closest
                    xrange = [598, 1322]
                    yrange = [154, 876]
                    if 598 < event.pos[0] < 1322:
                        endselect = (event.pos[0], min(yrange, key=lambda y: abs(y - event.pos[1])))
                    elif 154 < event.pos[1] < 876:
                        endselect = (min(xrange, key=lambda x: abs(x - event.pos[0])), event.pos[1])
                    else:
                        endselect = (min(xrange, key=lambda x: abs(x - event.pos[0])), min(yrange, key=lambda y: abs(y - event.pos[1])))
                    selected = []
                    Selecting = False
                    for f in friendly:
                        if startselect[0] <= f.x <= endselect[0] and startselect[1] <= f.y <= endselect[1]:
                            selected.append(f)

            if event.type == MOUSEBUTTONDOWN and event.button == 3:
                for s in selected:
                    s.target = event.pos

        gameDisplay.blit(BattleGround, (460, 0))
        # putting the inkblots on the field
        for blot in inkblots:
            blot[2] -= 1
            if blot[2] <= 0:
                blot[2] = 0
                blot[1] -= 1
                if blot[1] <=0:
                    inkblots.remove(blot)
            inkblot.set_alpha(blot[1])
            gameDisplay.blit(inkblot, blot[0])

            # putting the pumps on the field
        for p in Pumps:
            gameDisplay.blit(p.Asset, (p.x, p.y))
            if p.hp <= 0:
                for f in friendly:
                    if p.x - 10 <= f.x <= p.x + 10 and p.y - 10 <= f.y <= p.y + 10:
                        print("Friendly Pump gained")
                        Pumps.remove(p)
                        friendly.append(Units.Generator([p.x, p.y]))
                        break
                for e in enemy:
                    if p.x - 10 <= e.x <= p.x + 10 and p.y - 10 <= e.y <= p.y + 10:
                        print("Enemy Pump gained")
                        enemy.append(Units.Generator([p.x, p.y]))
                        Pumps.remove(p)
                        break
                # Remove the pump from the field if its HP is 0
            else:
                for f in friendly:
                    if p.x - 10 <= f.x <= p.x + 10 and p.y - 10 <= f.y <= p.y + 10:
                        p.hp -= 1
                for e in enemy:
                    if p.x - 10 <= e.x <= p.x + 10 and p.y - 10 <= e.y <= p.y + 10:
                        p.hp -= 1
        # putting the selected units on the field
        p_controled = 0
        for f in friendly:
            # checking for collision
            for e in enemy:
                if f.x in range(e.x - 5, e.x + 5, 1) and f.y in range(e.y - 5, e.y + 5, 1):
                    # combat
                    f.hp -= e.attack
                    e.hp -= f.attack
            # checking for enchanter damage
            if f.x in range(961, 971) and f.y in range(180, 190):
                Enchanter_HP -= f.attack
                f.hp = 0
            # unit death
            if f.hp <= 0:
                if f.__class__.__name__ == "Generator":
                    print("Friendly Pump destroyed")
                    enemy.append(Units.Generator([f.x, f.y]))
                else:
                    inkblots.append([(f.x, f.y), 255, 1000])
                friendly.remove(f)
            # movement
            else:
                f.move(frame, friendly)
                gameDisplay.blit(f.Asset, (f.x, f.y))
            # counting the number of controlled pumps
            if f.__class__.__name__ == "Generator":
                p_controled += 1
            if f.__class__.__name__ == "Summoner" and frame in range(0, 500, 100):
                friendly.append(Units.Minion([f.x+3, f.y+3]))
                friendly[-1].target = f.target
            if f.__class__.__name__ == "Minion":
                f.lifetime += 1
                if f.lifetime >= 1000:
                    inkblots.append([(f.x, f.y), 255, 1000])
                    friendly.remove(f)

        # similar to player controlled units, but for enchanter units
        p_e_controled = 0
        for e in enemy:
            # checking for player Damage
            if e.x in range(961, 971) and e.y in range(855, 865):
                player_HP -= e.attack
                e.hp = 0

            if e.hp <= 0:
                
                if e.__class__.__name__ == "Generator":
                    print("Enemy Pump destroyed")
                    friendly.append(Units.Generator([e.x, e.y]))
                else:
                    inkblots.append([(e.x, e.y), 255, 1000])
                enemy.remove(e)
            else:
                e.move(frame, enemy)
                gameDisplay.blit(e.Asset, (e.x, e.y))
            if e.__class__.__name__ == "Generator":
                p_e_controled += 1
            if e.__class__.__name__ == "Summoner" and frame in range(0, 500, 100):
                enemy.append(Units.Minion([e.x+3, e.y+3]))
                enemy[-1].target = e.target
            if e.__class__.__name__ == "Minion":
                e.lifetime += 1
                if e.lifetime >= 1000:
                    inkblots.append([(e.x, e.y), 255, 1000])
                    enemy.remove(e)

        # Mana Regen, for both player and Enchanter
        P_ratio = {0: 1, 1: 3, 2: 4, 3: 4, 4: 6}

        divisor = P_ratio[p_controled]
        if frame in range(0, 500,int(500/divisor)):
            player_mana += 1
            if player_mana > 9:
                player_mana = 9
        
        divisor = P_ratio[p_e_controled]
        if frame in range(0, 500,int(500/divisor)):
            Enchanter_mana += 1
            if Enchanter_mana > 9:
                Enchanter_mana = 9

        # Summoning enchanter units
        if frame in (100, 200, 300, 400, 500):
            summon = Enchanter.summon(Enchanter_mana)
            # print(summon)
            if summon == '0':
                enemy.append(Units.Footman([966, 185]))
                Enchanter_mana -= 1
            elif summon == '1':
                enemy.append(Units.Horse([966, 185]))
                Enchanter_mana -= 3
            elif summon == '2':
                enemy.append(Units.Soldier([966, 185]))
                Enchanter_mana -= 3
            elif summon == '3':
                enemy.append(Units.Summoner([966, 185]))
                Enchanter_mana -= 6
            elif summon == '4':
                enemy.append(Units.Runner([966, 185]))
                Enchanter_mana -= 8
            elif summon == '5':
                enemy.append(Units.Tank([966, 185]))
                Enchanter_mana -= 8

            # print("summon failed")
            if enemy:
                enemy[-1].target = [966, 185]

            # enchanter targeting

        if frame >= 500:
            frame = 0
            Enchanter.target(enemy, friendly, Pumps)
        # player mana display
        manaPath = "Assets\Sprites\Mana_counter\\" + str(player_mana) + ".png"
        manaCounter = pygame.image.load(manaPath)
        gameDisplay.blit(manaCounter, (200, 850))

        # Hp display
        hp = HPFont.render(str(player_HP) + ":" + str(Enchanter_HP), True, (255, 150, 255))
        gameDisplay.blit(hp, (200, 200))

        gameDisplay.blit(summon_UI, (1600, 200))
        
        # cursor display
        gameDisplay.blit(cursor_img, pygame.mouse.get_pos())

        # display update, counters, and FPS
        pygame.display.flip()
        clock.tick(100)
        gameDisplay.fill((0, 0, 0))
        frame += 1