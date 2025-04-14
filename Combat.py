import Units, pygame, random, SaveUpdater, time
from Ai import Enchanter, Madman, Monarch
from pygame.locals import *
import os

def BatStart(Ai: str, display: pygame.Surface, RPC_on: bool, RPC: object, pid):
    # Get screen dimensions dynamically
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    print()

    # Initialize variables
    player_mana = 5
    Enchanter_mana = 5
    player_HP = 20
    Enchanter_HP = 20
    Won = False
    Enemy_ai = Enchanter
    score = 0
    max_time = 1200000
    start_time = time.time()
    gameDisplay = display
    BattleGround = pygame.image.load(os.path.join("Assets", "Sprites", "pixil-frame-0.png"))
    inkblot = pygame.image.load(os.path.join("Assets", "Sprites", "InkBlot.png"))
    clock = pygame.time.Clock()
    gameDisplay.fill((0, 0, 0))
    pygame.mixer.music.load(os.path.join("Assets", "Music", "DungeonSynth2Hr.mp3"))
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(1)

    # Scale assets dynamically
    BattleGround = pygame.transform.smoothscale(BattleGround, (screen_width * 0.55, screen_height*1))
    inkblot = pygame.transform.scale(inkblot, (screen_height*0.01, screen_height*0.01))

    # Scale fonts dynamically
    HPFont = pygame.font.Font(os.path.join("Assets", "Fonts", "Speech.ttf"), int(screen_height * 0.1))
    SpeechFont = pygame.font.Font(os.path.join("Assets", "Fonts", "Speech.ttf"), int(screen_height * 0.05))
    pause = SpeechFont.render('Paused', True, (255, 255, 255))

    # Scale UI elements dynamically
    summon_UI = pygame.image.load(os.path.join("Assets", "Sprites", "Selecetion grid.png"))
    summon_UI = pygame.transform.scale(summon_UI, (int(screen_width * 0.2), int(screen_height * 0.6)))

    manaCounter = pygame.image.load(os.path.join("Assets", "Sprites", "Mana_counter", "5.png"))
    manaCounter = pygame.transform.scale(manaCounter, (int(screen_width * 0.1), int(screen_height * 0.1)))

    # Dynamic positioning
    BattleGround_pos = (screen_width * 0.2, screen_height * 0)
    summon_UI_pos = (screen_width * 0.92, screen_height * 0)
    manaCounter_pos = (screen_width * 0, screen_height * 0.85)
    HP_pos = (screen_width * 0, screen_height * 0)

    # Adjust tutorial text positions dynamically
    tutorial_positions = [
        (screen_width * 0.35, screen_height * 0.8),
        (screen_width * 0.15, screen_height * 0.8),
        (screen_width * 0.4, screen_height * 0.3),
        (screen_width * 0.15, screen_height * 0.3),
        (screen_width * 0.4, screen_height * 0.4),
        (screen_width * 0.45, screen_height * 0.6),
        (screen_width * 0.45, screen_height * 0.6),
        (screen_width * 0.35, screen_height * 0.8)
    ]

    # Adjust other hardcoded positions dynamically
    Rloc = (screen_width * 0.4, screen_height * 0.9)
    Bloc = (screen_width * 0.45, screen_height * 0.9)

    # Adjust costs dynamically
    Footman_cost_pos = (screen_width * 0.88, screen_height * 0.15)
    Horse_cost_pos = (screen_width * 0.88, screen_height * 0.25)
    Soldier_cost_pos = (screen_width * 0.88, screen_height * 0.35)
    Summoner_cost_pos = (screen_width * 0.88, screen_height * 0.45)
    Runner_cost_pos = (screen_width * 0.88, screen_height * 0.55)
    Tank_cost_pos = (screen_width * 0.88, screen_height * 0.65)

    # Adjust endgame message positions dynamically
    endgame_message_pos = (screen_width * 0.4, screen_height * 0.9)
    
    # Adjust cursor size dynamically
    cursor_img = pygame.image.load(os.path.join("Assets", "Sprites", "Mouse.png"))
    cursor_img = pygame.transform.scale(cursor_img, (int(screen_width * 0.03), int(screen_height * 0.05)))

    X_MIN = int(BattleGround_pos[0] + (BattleGround.get_width() * 0.124))
    X_MAX = int(BattleGround_pos[0] + (BattleGround.get_width() * 0.865))
    Y_MIN = int(BattleGround_pos[1] + (BattleGround.get_height() * 0.19))
    Y_MAX = int(BattleGround_pos[1] + (BattleGround.get_height() * 0.89))

    
    BattleGround_width = X_MAX - X_MIN
    BattleGround_height = Y_MAX - Y_MIN

    BattleGround_debug_rect = pygame.Rect(X_MIN, Y_MIN, BattleGround_width, BattleGround_height)
    player_base = (int(X_MIN + (BattleGround_width // 2)), int(Y_MAX - (BattleGround_height * 0.1)))
    enemy_base = (int(X_MIN + (BattleGround_width // 2)),int(Y_MIN + (BattleGround_height * 0.1)))
    # Adjust pump positions dynamically to be centered and evenly spaced
    Pumps = [
        Units.Generator((X_MIN + (BattleGround_width * 0.20), Y_MIN + (BattleGround_height * 0.20))),
        Units.Generator((X_MIN + (BattleGround_width * 0.70), Y_MIN + (BattleGround_height * 0.20))),
        Units.Generator((X_MIN + (BattleGround_width * 0.20), Y_MIN + (BattleGround_height * 0.70))),
        Units.Generator((X_MIN + (BattleGround_width * 0.70), Y_MIN + (BattleGround_height * 0.70)))
    ]

    # Adjust selection bounds dynamically
    boundaries = {
        'left': X_MIN,
        'right': X_MAX,
        'top': Y_MIN,
        'bottom': Y_MAX
    }
    epoch = int(time.time())
    
    if RPC_on:
        RPC.update(
            pid=pid,
            state="Inking and Incanting",
            details=f"{player_HP}:{Enchanter_HP}",
            start=epoch,
            large_image="icon",
            large_text="The Enchanters Book awaits...."
        )
    if Ai == 'enchanter':
        Ready = SpeechFont.render('Are you Ready, Mage?', True, (255, 150, 255))
        Begin = SpeechFont.render('Let us begin.', True, (255, 150, 255))
        Rloc = (Ready.get_rect(center=(screen_width // 2, screen_height * 0.9)))
        Bloc = (Begin.get_rect(center=(screen_width // 2, screen_height * 0.9)))
        Enemy_ai = Enchanter
    elif Ai == 'monarch':
        Ready = SpeechFont.render('You know why I summoned you to my court?', True, (80, 200, 120))
        Begin = SpeechFont.render('To entertain me.', True, (80, 200, 120))
        Rloc = (Ready.get_rect(center=(screen_width // 2, screen_height * 0.9)))
        Bloc = (Begin.get_rect(center=(screen_width // 2, screen_height * 0.9)))
        Enemy_ai = Monarch
    elif Ai == 'madman':
        TitleFont = pygame.font.Font(os.path.join("Assets", "Fonts", "Books-Vhasenti.ttf"), 50)
        Ready = SpeechFont.render('The walls, I hear them in the walls. Those Ticks.', True, (255, 0, 0))
        Begin = TitleFont.render('Do you hear them too?', True, (255, 0, 0))
        Rloc = (Ready.get_rect(center=(screen_width // 2, screen_height * 0.9)))
        Bloc = (Begin.get_rect(center=(screen_width // 2, screen_height // 2)))
        Enemy_ai = Madman
    else:
        Ready = SpeechFont.render('Error', True, (255, 150, 255))
        Begin = SpeechFont.render('Error: No AI selected', True, (255, 150, 255))
        Rloc = (Ready.get_rect(center=(screen_width // 2, screen_height * 0.9)))
        Bloc = (Begin.get_rect(center=(screen_width // 2, screen_height * 0.9)))
        Enemy_ai = Enchanter

    # Enchanters speech
    for i in range(0, 5):
        gameDisplay.fill((0, 0, 0))
        if i == 1:
            gameDisplay.blit(Ready, Rloc)
        if i == 3:
            gameDisplay.blit(Begin, Bloc)
        pygame.display.flip()

        clock.tick(100)
        skip = False
        if i != 2 or i != 0:
            for i in range(4000):
                if skip:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        quit()
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        skip = True
                pygame.time.delay(1)

        else:
            for i in range(2000):
                if skip:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        quit()
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        skip = True
                pygame.time.delay(1)

    # Fade in the background
    a = 0
    for i in range(255):
        gameDisplay.fill((0, 0, 0))
        a += 1
        BattleGround.set_alpha(a)
        gameDisplay.blit(BattleGround, BattleGround_pos)
        pygame.display.flip()

    # Fade in the UI + pumps
    pygame.time.delay(1)
    running = True
    Hp = HPFont.render(str(player_HP) + ":" + str(Enchanter_HP), False, (255, 150, 255))
    Footman_cost = SpeechFont.render(str(Units.Footman.cost), True, (255, 0, 0))
    Horse_cost = SpeechFont.render(str(Units.Horse.cost), True, (255, 0, 0))
    Soldier_cost = SpeechFont.render(str(Units.Soldier.cost), True, (255, 0, 0))
    Summoner_cost = SpeechFont.render(str(Units.Summoner.cost), True, (255, 0, 0))
    Runner_cost = SpeechFont.render(str(Units.Runner.cost), True, (255, 0, 0))
    Tank_cost = SpeechFont.render(str(Units.Tank.cost), True, (255, 0, 0))
    summon_UI = pygame.image.load(os.path.join("Assets", "Sprites", "Selecetion grid.png"))
    a = 0
    manaCounter = pygame.image.load(os.path.join("Assets", "Sprites", "Mana_counter", "5.png"))
    for i in range(255):
        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(BattleGround, BattleGround_pos)
        a += 1
        for p in Pumps:
            p.Asset.set_alpha(a)
            gameDisplay.blit(p.Asset, (p.x, p.y))
        manaCounter.set_alpha(a)
        summon_UI.set_alpha(a)
        gameDisplay.blit(summon_UI, summon_UI_pos)
        gameDisplay.blit(manaCounter, manaCounter_pos)
        Footman_cost.set_alpha(a)
        gameDisplay.blit(Footman_cost, Footman_cost_pos)
        Horse_cost.set_alpha(a)
        gameDisplay.blit(Horse_cost, Horse_cost_pos)
        Soldier_cost.set_alpha(a)
        gameDisplay.blit(Soldier_cost, Soldier_cost_pos)
        Summoner_cost.set_alpha(a)
        gameDisplay.blit(Summoner_cost,Summoner_cost_pos)
        Runner_cost.set_alpha(a)
        gameDisplay.blit(Runner_cost, Runner_cost_pos)
        Tank_cost.set_alpha(a)
        gameDisplay.blit(Tank_cost, Tank_cost_pos)
        Hp.set_alpha(a)
        gameDisplay.blit(Hp, HP_pos)
        pygame.display.flip()

    # Loading Vars
    cursor_img = pygame.image.load(os.path.join("Assets", "Sprites", "Mouse.png"))
    pygame.mouse.set_visible(False)
    Selecting = False
    selected = []
    friendly = []
    enemy = []
    inkblots = []
    mouseinkblots = []
    if not SaveUpdater.decode_save_file()['tutorial']:
        tutorial_steps = [
            ("Welcome to the battlefield, Mage.", tutorial_positions[0]),
            ("This is your mana counter. You need mana to summon units.", tutorial_positions[1]),
            ("These are your summoning options. Each unit costs a different amount of mana.", tutorial_positions[2]),
            ("This is your health. If it reaches zero, you lose.", tutorial_positions[3]),
            ("These are your pumps. Control them to gain more mana.", tutorial_positions[4]),
            ("Click and drag to select your units.", tutorial_positions[5]),
            ("Right-click to move your selected units.", tutorial_positions[6]),
            ("Defeat the enemy by reducing their health to zero.", tutorial_positions[7])
        ]
        for step, loc in tutorial_steps:
            gameDisplay.fill((0, 0, 0))
            gameDisplay.blit(BattleGround, BattleGround_pos)
            for p in Pumps:
                gameDisplay.blit(p.Asset, (p.x, p.y))
            gameDisplay.blit(manaCounter, manaCounter_pos)
            gameDisplay.blit(summon_UI, summon_UI_pos)
            gameDisplay.blit(Hp, HP_pos)
            tutorial_text = SpeechFont.render(step, True, (255, 150, 255))
            text_rect = tutorial_text.get_rect(topleft=loc)
            pygame.draw.rect(gameDisplay, (0, 0, 0), text_rect)
            gameDisplay.blit(tutorial_text, loc)
            pygame.display.flip()
            pygame.time.delay(500)
            skip = False
            while not skip:
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                            pygame.quit()
                            return False
                if event.type == MOUSEBUTTONDOWN or event.type == KEYDOWN:
                        pygame.time.delay(100)
                        skip = True


        save = SaveUpdater.decode_save_file()
        save['tutorial'] = True
        SaveUpdater.encode_save_file(save)

    pygame.event.clear()

    # Initialize variables for delta time
    last_time = time.time()
    player_mana_timer = 0
    enchanter_mana_timer = 0
    summon_timer = 0
    targeting_timer = 0
    show_fps_debug = False
    show_mana_debug = False
    show_battle_debug = False
    # Main game loop
    running = True
    while running:
        # Calculate delta time
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
                pygame.quit()
                return False
            if event.type == KEYDOWN and event.key == K_F1:
                if not show_fps_debug:
                    show_fps_debug = True
                    show_mana_debug = False
                else:
                    show_fps_debug = False
                    show_mana_debug = False
            if event.type == KEYDOWN and event.key == K_F2:
                if show_mana_debug:
                    show_mana_debug = False
                    show_fps_debug = False
                else:
                    show_mana_debug = True
                    show_fps_debug = True
            if event.type == KEYDOWN and event.key == K_F3:
                show_battle_debug = not show_battle_debug
            if event.type == KEYDOWN and event.key == K_p:
                paused = True
                while paused:
                    gameDisplay.blit(pause, (800, 450))
                    pygame.display.flip()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                            running = False
                            paused = False
                        if event.type == KEYDOWN and event.key == K_p:
                            paused = False 
            # start of selection
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
    # Check if the click is within the battlefield bounds
                if X_MIN < event.pos[0] < X_MAX and not Selecting and Y_MIN < event.pos[1] < Y_MAX:
                    Selecting = True
                # Check if the click is within the summoning UI bounds
                elif summon_UI_pos[0] < event.pos[0] < summon_UI_pos[0] + int(screen_width * 0.2) and summon_UI_pos[1] < event.pos[1] < summon_UI_pos[1] + int(screen_height * 0.6):
                    # Determine which unit to summon based on the Y position of the click
                    if player_mana >= Units.Footman.cost and summon_UI_pos[1] <= event.pos[1] < summon_UI_pos[1] + int(screen_height * 0.125):
                        friendly.append(Units.Footman((player_base[0], player_base[1])))
                        friendly[-1].target = (player_base[0], player_base[1])
                        player_mana -= Units.Footman.cost
                    elif player_mana >= Units.Horse.cost and summon_UI_pos[1] + int(screen_height * 0.125) <= event.pos[1] < summon_UI_pos[1] + int(screen_height * 0.25):
                        friendly.append(Units.Horse((player_base[0], player_base[1])))
                        friendly[-1].target = (player_base[0], player_base[1])
                        player_mana -= Units.Horse.cost
                    elif player_mana >= Units.Soldier.cost and summon_UI_pos[1] + int(screen_height * 0.25) <= event.pos[1] < summon_UI_pos[1] + int(screen_height * 0.375):
                        friendly.append(Units.Soldier((player_base[0], player_base[1])))
                        friendly[-1].target = (player_base[0], player_base[1])
                        player_mana -= Units.Soldier.cost
                    elif player_mana >= Units.Summoner.cost and summon_UI_pos[1] + int(screen_height * 0.375) <= event.pos[1] < summon_UI_pos[1] + int(screen_height * 0.5):
                        friendly.append(Units.Summoner((player_base[0], player_base[1])))
                        friendly[-1].target = (player_base[0], player_base[1])
                        player_mana -= Units.Summoner.cost
                    elif player_mana >= Units.Runner.cost and summon_UI_pos[1] + int(screen_height * 0.5) <= event.pos[1] < summon_UI_pos[1] + int(screen_height * 0.625):
                        friendly.append(Units.Runner((player_base[0], player_base[1])))
                        friendly[-1].target = (player_base[0], player_base[1])
                        player_mana -= Units.Runner.cost
                    elif player_mana >= Units.Tank.cost and summon_UI_pos[1] + int(screen_height * 0.625) <= event.pos[1] < summon_UI_pos[1] + int(screen_height * 0.75):
                        friendly.append(Units.Tank((player_base[0], player_base[1])))
                        friendly[-1].target = (player_base[0], player_base[1])
                        player_mana -= Units.Tank.cost
                        
           # end of selection
            if event.type == MOUSEBUTTONUP and event.button == 1:
                # checking if in bounds of the field
                if Selecting:
                    Selecting = False
                    if mouseinkblots:
                        blotx=[]
                        bloty=[]
                        for ink in mouseinkblots:
                            blotx.append(ink[0][0])
                            bloty.append(ink[0][1])
                        blotx.sort()
                        bloty.sort()
                        startselect = (blotx[0], bloty[0])
                        endselect = (blotx[-1], bloty[-1])
                        selected = []
                        for f in friendly:
                            if startselect[0] <= f.x <= endselect[0] and startselect[1] <= f.y <= endselect[1]:
                                    selected.append(f)
                            # print(f"Selection from {startselect} to {endselect}")
                            # print(f"Selected units: {selected}")
            if event.type == MOUSEBUTTONDOWN and event.button == 3:
                for s in selected:
                    s.target = event.pos
            if event.type == MOUSEBUTTONDOWN and event.button == 2:
                #middle mouse button
                print(event.pos)
            # Adjust the boundary conditions in the MOUSEMOTION event handler
            if Selecting and event.type == MOUSEMOTION:
                pos = event.pos
                # Clamp the position within the battlefield bounds
                clamped_x = max(X_MIN, min(pos[0], X_MAX))
                clamped_y = max(Y_MIN, min(pos[1], Y_MAX))
                pos = (clamped_x, clamped_y)
                mouseinkblots.append([pos, 255, 100, random.randint(0, 360)])

        gameDisplay.blit(BattleGround, BattleGround_pos)
        # putting the inkblots on the field
        for blot in inkblots:
            blot[2] -= 1
            if blot[2] <= 0:
                blot[2] = 0
                blot[1] -= 1
                if blot[1] <=0:
                    inkblots.remove(blot)
                    continue
            inkblot.set_alpha(blot[1])
            pygame.transform.rotate(inkblot, blot[3])
            gameDisplay.blit(inkblot, blot[0])

        for blot in mouseinkblots:
                if not Selecting:
                    blot[2] -= 1
                    if blot[2] <= 0:
                        blot[2] = 0
                        blot[1] -= 1
                        if blot[1] <=0:
                            try:
                                inkblots.remove(blot)
                            except:
                                pass
                inkblot.set_alpha(blot[1])
                pygame.transform.rotate(inkblot, blot[3])
                gameDisplay.blit(inkblot, blot[0])

        # putting the pumps on the field
        for p in Pumps:
            gameDisplay.blit(p.Asset, (p.x, p.y))
            if p.hp <= 0:
                for f in friendly:
                    if p.x - 10 <= f.x <= p.x + 42 and p.y - 10 <= f.y <= p.y + 42:
                        # print("Friendly Pump gained")
                        score += 100
                        Pumps.remove(p)
                        friendly.append(Units.Generator([p.x, p.y]))
                        break
                for e in enemy:
                    if p.x - 42 <= e.x <= p.x + 42 and p.y - 42 <= e.y <= p.y + 42:
                        # print("Enemy Pump gained")
                        enemy.append(Units.Generator([p.x, p.y]))
                        Pumps.remove(p)
                        break
                # Remove the pump from the field if its HP is 0
            else:
                for f in friendly:
                    if p.x - 10 <= f.x <= p.x + 42 and p.y - 10 <= f.y <= p.y + 42:
                        p.hp -= 1
                for e in enemy:
                    if p.x - 10 <= e.x <= p.x + 42 and p.y - 10 <= e.y <= p.y + 42:
                        p.hp -= 1
        # putting the selected units on the field
        p_controled = 0
        for f in friendly:
            # checking for collision
            for e in enemy:
                if f.x in range(int(e.x), int(e.x + 12), 1) and f.y in range(int(e.y), int(e.y + 12), 1):
                    # combat
                    f.hp -= e.attack
                    e.hp -= f.attack
            # checking for enchanter damage
            if f.x in range(enemy_base[0]-5, enemy_base[0]+5) and f.y in range(enemy_base[1]-5, enemy_base[1]+5):
                Enchanter_HP -= f.attack
                f.hp = 0
            # unit death
            if f.hp <= 0:
                score -= 10
                if f.__class__.__name__ == "Generator":
                    # print("Friendly Pump destroyed")
                    enemy.append(Units.Generator([f.x, f.y]))
                else:
                    inkblots.append([(f.x, f.y), 255, 1000, random.randint(0, 360)])
                friendly.remove(f)
                continue
            # movement
            else:
                f.move(dt, friendly, boundaries)
                gameDisplay.blit(f.Asset, (f.x, f.y))
            # counting the number of controlled pumps
            if f.__class__.__name__ == "Generator":
                p_controled += 1
            if f.__class__.__name__ == "Summoner":
                if not hasattr(e, "spawn_timer"):
                    f.spawn_timer = 0  # Initialize spawn timer if not already set
                f.spawn_timer += dt  # Increment spawn timer by delta time
                if f.spawn_timer >= 1:  # Check if 1 second has passed
                    friendly.append(Units.Minion([e.x + 3, e.y + 3]))
                    friendly[-1].target = f.target
                    f.spawn_timer = 0  # Reset the spawn timer
            if f.__class__.__name__ == "Minion":
                f.lifetime += dt
                if f.lifetime >= 10:
                    inkblots.append([(f.x, f.y), 255, 1000, random.randint(0, 360)])
                    friendly.remove(f)
                    continue

        # similar to player controlled units, but for enchanter units
        p_e_controled = 0
        for e in enemy:
            # checking for player Damage
            if e.x in range(player_base[0]-5, player_base[0]+5) and e.y in range(player_base[1]-5, player_base[1]+5):
                player_HP -= e.attack
                e.hp = 0

            if e.hp <= 0:
                score += 10
                if e.__class__.__name__ == "Generator":
                    print("Enemy Pump destroyed")
                    friendly.append(Units.Generator([e.x, e.y]))
                else:
                    inkblots.append([(e.x, e.y), 255, 1000, random.randint(0, 360)])
                enemy.remove(e)
                continue
            else:
                e.move(dt, enemy, boundaries)
                gameDisplay.blit(e.Asset, (e.x, e.y))
            if e.__class__.__name__ == "Generator":
                p_e_controled += 1
            if e.__class__.__name__ == "Summoner":
                if not hasattr(e, "spawn_timer"):
                    e.spawn_timer = 0  # Initialize spawn timer if not already set
                e.spawn_timer += dt  # Increment spawn timer by delta time
                if e.spawn_timer >= 1:  # Check if 1 second has passed
                    enemy.append(Units.Minion([e.x + 3, e.y + 3]))
                    enemy[-1].target = e.target
                    e.spawn_timer = 0  # Reset the spawn timer
            if e.__class__.__name__ == "Minion":
                e.lifetime += dt
                if e.lifetime >= 10:
                    inkblots.append([(e.x, e.y), 255, 1000, random.randint(0, 360)])
                    enemy.remove(e)
                    continue

        # Mana Regen, for both player and Enchanter
        P_ratio = {0: 1, 1: 3, 2: 4, 3: 4, 4: 6}
        
        divisor = P_ratio[p_controled]
        player_mana_timer += dt
        if player_mana_timer >= (5/divisor):
            player_mana = min(player_mana + 1, 9)
            player_mana_timer = 0
        enchanter_mana_timer += dt
        divisor_text = SpeechFont.render(f"Divisor: {str(divisor)}", True, (255, 255, 255))
        divisor = P_ratio[p_e_controled]
        if enchanter_mana_timer >= (5/divisor):
            Enchanter_mana = min(Enchanter_mana + 1, 9)
            enchanter_mana_timer = 0

        if Ai == 'madman':
            #Yes, the madman Cheats, Hes mad, he doesnt care about the rules
            Enchanter_mana = 9
        # Summoning enemy units
        summon_timer += dt
        if summon_timer >= 5:
            summon = Enemy_ai.summon(Enchanter_mana, p_e_controled, enemy)
            print(summon)
            spawn_position = enemy_base  # Dynamic spawn position for enemy units
            if summon == 0:
                enemy.append(Units.Footman(spawn_position))
                Enchanter_mana -= 1
                last = [enemy[-1]]
                Enemy_ai.target(last, friendly, Pumps, player_HP, Enchanter_HP, player_base, enemy_base)
            elif summon == 1:
                enemy.append(Units.Horse(spawn_position))
                Enchanter_mana -= 3
                last = [enemy[-1]]
                Enemy_ai.target(last, friendly, Pumps, player_HP, Enchanter_HP, player_base, enemy_base)
            elif summon == 2:
                enemy.append(Units.Soldier(spawn_position))
                Enchanter_mana -= 3
                last = [enemy[-1]]
                Enemy_ai.target(last, friendly, Pumps, player_HP, Enchanter_HP, player_base, enemy_base)
            elif summon == 3:
                enemy.append(Units.Summoner(spawn_position))
                Enchanter_mana -= 6
                last = [enemy[-1]]
                Enemy_ai.target(last, friendly, Pumps, player_HP, Enchanter_HP, player_base, enemy_base)
            elif summon == 4:
                enemy.append(Units.Runner(spawn_position))
                Enchanter_mana -= 8
                last = [enemy[-1]]
                Enemy_ai.target(last, friendly, Pumps, player_HP, Enchanter_HP, player_base, enemy_base)
            elif summon == 5:
                enemy.append(Units.Tank(spawn_position))
                Enchanter_mana -= 8
                last = [enemy[-1]]
                Enemy_ai.target(last, friendly, Pumps, player_HP, Enchanter_HP, player_base, enemy_base)
            else:
                print("Summon failed")

        # Enchanter targeting
        targeting_timer += dt
        if targeting_timer >= 10:  # Update targeting every 10 seconds
            Enemy_ai.target(enemy, friendly, Pumps, player_HP, Enchanter_HP, player_base, enemy_base)
            targeting_timer = 0

        if player_HP <= 0:
            running = False
            
        if Enchanter_HP <= 0:
            running = False
            Won = True

        selection_icon = pygame.image.load(os.path.join("Assets", "Sprites", "unit_sprites", "Selected.png")) 
        for s in selected:
            gameDisplay.blit(selection_icon, (s.x, s.y))

        # player mana display
        manaPath = os.path.join("Assets", "Sprites", "Mana_counter", str(player_mana) + ".png")
        manaCounter = pygame.image.load(manaPath)
        gameDisplay.blit(manaCounter, manaCounter_pos)

        # Hp display
        hp = HPFont.render(str(player_HP) + ":" + str(Enchanter_HP), True, (255, 150, 255))
        gameDisplay.blit(hp, HP_pos)

        gameDisplay.blit(summon_UI, summon_UI_pos)
        gameDisplay.blit(Footman_cost, Footman_cost_pos)
        gameDisplay.blit(Horse_cost, Horse_cost_pos)
        gameDisplay.blit(Soldier_cost, Soldier_cost_pos)
        gameDisplay.blit(Summoner_cost, Summoner_cost_pos)
        gameDisplay.blit(Runner_cost, Runner_cost_pos)
        gameDisplay.blit(Tank_cost, Tank_cost_pos)
        
        # cursor display
        gameDisplay.blit(cursor_img, pygame.mouse.get_pos())
        if RPC_on:
            RPC.update(
            pid=pid,
            state="Inking and Incanting",
            details=f"{player_HP}:{Enchanter_HP}",
            start=epoch, 
            large_image="icon",
            large_text="The Enchanters Book awaits....")
        
        # Display FPS counter
        fps = int(clock.get_fps())
        if show_fps_debug:
            fps_text = SpeechFont.render(f"FPS: {fps}", True, (255, 255, 255))
            gameDisplay.blit(fps_text, (int(screen_width * 0), int(screen_height * 0.3)))  # Dynamic position for FPS
            dt_text = SpeechFont.render(f"dt: {round(dt * 1000, 3)}ms", True, (255, 255, 255))
            gameDisplay.blit(dt_text, (int(screen_width * 0), int(screen_height * 0.35)))  # Dynamic position for delta time
        if show_mana_debug:
            mana_text = SpeechFont.render(f"Mana Timer: {round(player_mana_timer, 3)}", True, (255, 255, 255))
            gameDisplay.blit(mana_text, (int(screen_width * 0), int(screen_height * 0.4)))  # Dynamic position for mana timer
            gameDisplay.blit(divisor_text, (int(screen_width * 0), int(screen_height * 0.45)))  # Dynamic position for divisor
            mana_text = SpeechFont.render(f"Enchanter Mana Timer: {round(enchanter_mana_timer, 3)}", True, (255, 255, 255))
            gameDisplay.blit(mana_text, (int(screen_width * 0), int(screen_height * 0.5)))  # Dynamic position for enchanter mana timer
            Enchanter_mana_text = SpeechFont.render(f"Enchanter Mana: {Enchanter_mana}", True, (255, 255, 255))
            gameDisplay.blit(Enchanter_mana_text, (int(screen_width * 0), int(screen_height * 0.55)))  # Dynamic position for enchanter mana
        if show_battle_debug:
            pygame.draw.rect(gameDisplay, (255, 0, 0), BattleGround_debug_rect, 2)  # Red rectangle with a thickness of 2
        pygame.display.flip()
        clock.tick(100)
        gameDisplay.fill((0, 0, 0))

    
    end_time = time.time()
    total_time = end_time - start_time
    time_score = max_time - total_time
    if time_score <= 0:
        time_score = 0
    score += time_score

    if Won:
        if Ai == 'enchanter':
            if SaveUpdater.decode_save_file()["beat_enchanter_first_time"]:
                Second_1 = SpeechFont.render('The game is the same', True, (255, 150, 255))
                Second_2 = SpeechFont.render('So you have learnt', True, (255, 150, 255))
                Second1Loc = Second_1.get_rect(center=(screen_width // 2, screen_height * 0.5))
                Second2Loc = Second_2.get_rect(center=(screen_width // 2, screen_height * 0.6))
                save = SaveUpdater.decode_save_file()
                save['enchanter'] = True
                SaveUpdater.encode_save_file(save)
                messages = [(Second_1, Second1Loc), (Second_2, Second2Loc)]
            else:
                First_Win = SpeechFont.render('You never learn', True, (255, 150, 255))
                Loss_1 = SpeechFont.render('All you need to do is learn', True, (255, 150, 255))
                Loss_2 = SpeechFont.render('Again', True, (255, 150, 255))
                FirstWLoc = First_Win.get_rect(center=(screen_width // 2, screen_height * 0.4))
                l1Loc = Loss_1.get_rect(center=(screen_width // 2, screen_height * 0.5))
                l2Loc = Loss_2.get_rect(center=(screen_width // 2, screen_height * 0.6))
                Enchanter_HP = 100
                player_HP = 1
                messages = [(First_Win, FirstWLoc), (Loss_1, l1Loc), (Loss_2, l2Loc)]
        elif Ai == 'monarch':
            M_win = SpeechFont.render('Oh quite a game, Shall we play again', True, (80, 200, 120))
            mWLoc = M_win.get_rect(center=(screen_width // 2, screen_height * 0.5))
            save = SaveUpdater.decode_save_file()
            save['monarch'] = True
            SaveUpdater.encode_save_file(save)
            messages = [(M_win, mWLoc)]
        elif Ai == 'madman':
            mad_1 = SpeechFont.render('This isnt a Prison, this is a Machine.', True, (255, 0, 0))
            mad_2 = SpeechFont.render('ISNT THAT RIGHT ' + Madman.scare(), True, (255, 0, 0))
            mad1loc = mad_1.get_rect(center=(screen_width // 2, screen_height * 0.4))
            mad2loc = mad_2.get_rect(center=(screen_width // 2, screen_height * 0.5))
            save = SaveUpdater.decode_save_file()
            save['madman'] = True
            SaveUpdater.encode_save_file(save)
            messages = [(mad_1, mad1loc), (mad_2, mad2loc)]
        else:
            No_win = SpeechFont.render('Error: No AI selected', True, (255, 150, 255))
            No_wLoc = No_win.get_rect(center=(screen_width // 2, screen_height * 0.5))
            messages = [(No_win, No_wLoc)]
    else:
        if Ai == 'enchanter':
            Loss_1 = SpeechFont.render('All you need to do is learn', True, (255, 150, 255))
            Loss_2 = SpeechFont.render('Again', True, (255, 150, 255))
            l1Loc = Loss_1.get_rect(center=(screen_width // 2, screen_height * 0.5))
            l2Loc = Loss_2.get_rect(center=(screen_width // 2, screen_height * 0.6))
            messages = [(Loss_1, l1Loc), (Loss_2, l2Loc)]
        elif Ai == 'monarch':
            Crash_1 = SpeechFont.render('You bore me, Guards', True, (80, 200, 120))
            crash_loc = Crash_1.get_rect(center=(screen_width // 2, screen_height * 0.5))
            messages = [(Crash_1, crash_loc)]
        elif Ai == 'madman':
            mad_1 = SpeechFont.render('This isnt a Prison, this is a Machine', True, (255, 0, 0))
            mad_2 = SpeechFont.render('ISNT THAT RIGHT ' + Madman.scare(), True, (255, 0, 0))
            mad1loc = mad_1.get_rect(center=(screen_width // 2, screen_height * 0.4))
            mad2loc = mad_2.get_rect(center=(screen_width // 2, screen_height * 0.5))
            messages = [(mad_1, mad1loc), (mad_2, mad2loc)]
        else:
            No_loss = SpeechFont.render('Error: No AI selected', True, (255, 150, 255))
            no_lLoc = No_loss.get_rect(center=(screen_width // 2, screen_height * 0.5))
            messages = [(No_loss, no_lLoc)]

    # Display end game messages
    

    if Ai == 'enchanter' and not SaveUpdater.decode_save_file()["beat_enchanter_first_time"]:
        for message, loc in messages:
            gameDisplay.fill((0, 0, 0))
            gameDisplay.blit(message, loc)
            pygame.display.flip()
            skip = False
            for i in range(4000):
                if skip:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        return False
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        skip = True
        save = SaveUpdater.decode_save_file()
        save["beat_enchanter_first_time"] = True
        SaveUpdater.encode_save_file(save)
        # Enchanter cheats
        Enchanter_HP = 100
        player_HP = 1
        running = True
        enemy = []
        # Spawn a bunch of enemy troops around the player spawn
        for _ in range(10):
            enemy.append(Units.Footman([random.randint(player_base[0], 980), random.randint(840, 880)]))
            enemy.append(Units.Horse([random.randint(player_base[0], 980), random.randint(840, 880)]))
            enemy.append(Units.Soldier([random.randint(player_base[0], 980), random.randint(840, 880)]))
            enemy.append(Units.Runner([random.randint(player_base[0], 980), random.randint(840, 880)]))

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    return False

            gameDisplay.fill((0, 0, 0))
            gameDisplay.blit(BattleGround, BattleGround_pos)

            for e in enemy:
                e.move(dt, enemy, boundaries)
                gameDisplay.blit(e.Asset, (e.x, e.y))
                if e.x in range(961, 971) and e.y in range(855, 865):
                    player_HP -= e.attack
                    e.hp = 0
                if e.hp <= 0:
                    enemy.remove(e)
                    continue

            if player_HP <= 0:
                running = False

            # Display player and enchanter HP
            hp = HPFont.render(str(player_HP) + ":" + str(Enchanter_HP), True, (255, 150, 255))
            gameDisplay.blit(hp, (200, 200))

            # Display cursor
            gameDisplay.blit(cursor_img, pygame.mouse.get_pos())

            pygame.display.flip()
            clock.tick(100)
        Loss_1 = SpeechFont.render(' All you need to do is learn…', True, (255, 150, 255))
        Loss_2 = SpeechFont.render('Again.', True, (255, 150, 255))
        l1Loc = (800, 900)
        l2Loc = (870, 900)
        messages = [(Loss_1, l1Loc), (Loss_2, l2Loc)]
        for message, loc in messages:
            gameDisplay.fill((0, 0, 0))
            gameDisplay.blit(message, loc)
            pygame.display.flip()
            skip = False
            for i in range(4000):
                if skip:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        return False
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        skip = True
                pygame.time.delay(1)

    elif Ai == 'monarch':
        # Monarch crashes the game
        Crash_1 = SpeechFont.render('You bore me, Guards!', True, (255, 150, 255))
        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(Crash_1, (800, 900))
        pygame.display.flip()
        pygame.time.delay(4000)
        pygame.quit()
        return False
    else:
        for message, loc in messages:
            gameDisplay.fill((0, 0, 0))
            gameDisplay.blit(message, loc)
            pygame.display.flip()
            skip = False
            for i in range(4000):
                if skip:
                    break
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                        pygame.quit()
                        return False
                    if event.type == MOUSEBUTTONDOWN and event.button == 1:
                        skip = True
            

    # Ask if the player wants to play again
    play_again_font = pygame.font.Font(os.path.join("Assets", "Fonts", "Speech.ttf"), int(screen_height * 0.05))  # Dynamic font size
    play_again_text = play_again_font.render('Do you want to play again? (Y/N)', True, (255, 255, 255))
    score_text = play_again_font.render(str(round(score)), True, (255, 255, 255))

    # Center the text dynamically
    play_again_text_rect = play_again_text.get_rect(center=(screen_width // 2, screen_height * 0.6))
    score_text_rect = score_text.get_rect(center=(screen_width // 2, screen_height * 0.5))

    gameDisplay.fill((0, 0, 0))
    gameDisplay.blit(play_again_text, play_again_text_rect)
    gameDisplay.blit(score_text, score_text_rect)
    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                return False
            if event.type == KEYDOWN:
                if event.key == K_y:
                    return True
                elif event.key == K_n:
                    return False
    #Show Score and ask if they wanna play again, if they player wants to return to menu, return False, Else return True (Doesnt apply to monarch as game is crashed)

