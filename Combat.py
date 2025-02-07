import random, Units, pygame, time
from Ai import Enchanter
from pygame.locals import *


def BatStart():
    player_mana = 5
    Enchanter_mana = 5
    player_HP = 20
    Enchanter_HP=20


    icon = pygame.image.load("Assets\Icon.png")
    BattleGround = pygame.image.load("Assets\Sprites\pixil-frame-0.png")


    load = True
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
    Ready = SpeechFont.render('Are you Ready, Mage?', True, (255, 150, 255))
    Begin = SpeechFont.render('Let us begin.', True, (255, 150, 255))

    #enchanters speech
    for i in range(0, 5):
        gameDisplay.fill((0, 0, 0))
        if i==1:
            gameDisplay.blit(Ready, (800, 900))
        if i==3:
            gameDisplay.blit(Begin, (870, 900))
        pygame.display.flip()
        
        clock.tick(100)
        if i != 2 or i != 0:
            time.sleep(4)
        else:
            time.sleep(2)
        
    #fade in the background
    a = 0
    for i in range(255):
        gameDisplay.fill((0,0,0))
        a += 1
        BattleGround.set_alpha(a)
        gameDisplay.blit(BattleGround, (460, 0))
        pygame.display.flip()

    #fade in the UI + pumps    
    time.sleep(1)
    runnint = True
    Pumps = [Units.Generator((760, 315)), Units.Generator((1120, 315)), Units.Generator((760, 650)), Units.Generator((1120, 650))]
    a = 0
    manaCounter = pygame.image.load("Assets\Sprites\Mana_counter\\5.png")
    for i in range(255):
        gameDisplay.fill((0,0,0))
        gameDisplay.blit(BattleGround, (460, 0))
        a += 1
        for p in Pumps:

            p.Asset.set_alpha(a)
            gameDisplay.blit(p.Asset, (p.x, p.y))
        manaCounter.set_alpha(a)
        gameDisplay.blit(manaCounter, (200, 850))
        pygame.display.flip()

    #loading Vars
    cursor_img = pygame.image.load("Assets\Sprites\Mouse.png")
    pygame.mouse.set_visible(False)
    cursor_img_rect = cursor_img.get_rect()
    startselect = (960,540)
    endselect = (0,0)
    frame = 0
    Selecting = False
    selected = []
    friendly = []
    enemy = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                running = False
            #start of selection
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if 598 < event.pos[0] < 1322 and not Selecting and 154 < event.pos[1] < 876:
                    startselect = event.pos
                    Selecting = True
                print(event.pos)
            #end of selection
            if event.type == MOUSEBUTTONUP and event.button == 1:
                #checking if in bounds of the field
                if 598 < event.pos[0] < 1322 and Selecting and 154 < event.pos[1] < 876:
                    endselect = event.pos
                    Selecting = False
                    selected = []
                    for f in friendly:
                        if f.x in range(startselect[0], endselect[0], 1) and f.y in range(startselect[1], endselect[1], 1):
                            selected.append(f)
                elif Selecting:
                    #if not in bounds, find which co-ords are in bounds, if none, find the closest
                    if 598 < event.pos[0] < 1322:
                        endselect = event.pos[0], min((154, 876), key=lambda x:abs(event.pos[1]))
                    elif 154 < event.pos[1] < 876: 
                        endselect = min((598, 1322), key=lambda x:abs(event.pos[0])), event.pos[1]
                    else:
                        endselect = min((598, 1322), key=lambda x:abs(event.pos[0])), min((154, 876), key=lambda x:abs(event.pos[1]))
                    selected = []   
                    Selecting = False
                    for f in friendly:
                        if f.x in range(startselect[0], endselect[0], 1) and f.y in range(startselect[1], endselect[1], 1):
                            selected.append(f)
            
            if event.type == MOUSEBUTTONDOWN and event.button == 3:
                for s in selected:
                    s.target = event.pos

        gameDisplay.blit(BattleGround, (460, 0))

        #putting the pumps on the field
        for p in Pumps:
            gameDisplay.blit(p.Asset, (p.x, p.y))

        #putting the selected units on the field
        p_controled = 0
        for f in friendly:
            #checking for collision
            for e in enemy:
                if f.x in range(e.x-5, e.x+5, 1) and f.y in range(e.y-5, e.y+5, 1):
                    #combat
                    f.hp -= e.attack
                    e.hp -= f.attack
            #checking for enchanter damage
            if f.x == 966 and f.y == 185: 
                Enchanter_HP -= f.attack
                f.hp = 0
            #unit death
            if f.hp <= 0:
                friendly.remove(f)
            #movement
            else:
                f.move()
                gameDisplay.blit(f.Asset, (f.x, f.y))
            #counting the number of controlled pumps
            if f.__class__.__name__ == "Generator":
                p_controled += 1

        #similar to player controlled units, but for enchanter units
        p_e_controled = 0
        for e in enemy:
            #chcking for player Damage
            if e.x == 966 and e.y == 860:
                player_HP -= e.attack
                e.hp = 0

            if e.hp <= 0:
                enemy.remove(e)
            else:
                e.move()
                gameDisplay.blit(e.Asset, (e.x, e.y))
            if e.__class__.__name__ == "Generator":
                p_e_controled += 1

        # Mana Regen, for both player and Enchanter
        P_ratio = {0:1 , 1:3, 2:4, 3:4, 4:6, }
        divisor = P_ratio[p_controled]
        if frame >= int(500/divisor):
            frame = 0
            player_mana += 1
            if player_mana > 9:
                player_mana = 9
        
        divisor = P_ratio[p_e_controled]
        if frame >= int(500/divisor):
            frame = 0
            Enchanter_mana += 1
            if Enchanter_mana > 9:
                Enchanter_mana = 9


        # Summoning enchanter units
        summon = Enchanter.summon(Enchanter_mana)
        if summon == 0:
            enemy.append(Units.Footman([966, 185]))
        elif summon == 1:
            enemy.append(Units.Horse([966, 185]))
        elif summon == 2:
            enemy.append(Units.Soldier([966, 185]))
        elif summon == 3:
            enemy.append(Units.Summoner([966, 185]))
        elif summon == 4:
            enemy.append(Units.Runner([966, 185]))
        elif summon == 5:
            enemy.append(Units.Tank([966, 185]))

        #enchanter targeting
        Enchanter.target(enemy, friendly, Pumps)

        #player mana display
        manaPath = "Assets\Sprites\Mana_counter\\"+str(player_mana)+".png"
        manaCounter = pygame.image.load(manaPath)
        gameDisplay.blit(manaCounter, (200, 850))


        #cursor display
        cursor_img_rect.center = pygame.mouse.get_pos()
        gameDisplay.blit(cursor_img, cursor_img_rect)

        #display update, counters, and FPS
        pygame.display.flip()
        clock.tick(100)
        gameDisplay.fill((0,0,0))
        frame+=1