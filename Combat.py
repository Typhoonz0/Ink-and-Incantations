import random, Units, pygame, time


def BatStart():
    player_mana = 5
    Enchanter_mana = 5
    player_HP = 20
    Enchanter_HP=20


    icon = pygame.image.load("Assets\Icon.png")

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
    pygame.mixer.music.set_volume(50)


    SpeechFont = pygame.font.Font("""Assets\Fonts\Speech.ttf""", 30)
    Ready = SpeechFont.render('Enchanter: Are you Ready?', True, (255, 255, 255))
    Begin = SpeechFont.render('Enchanter: Let us begin.', True, (255, 255, 255))

    for i in range(0, 5):
        gameDisplay.fill((0, 0, 0))
        if i==1:
            gameDisplay.blit(Ready, (800, 900))
        if i==3:
            gameDisplay.blit(Begin, (800, 900))
        pygame.display.flip()
        
        clock.tick(100)
        time.sleep(4)
    a = 0
    for i in range(255):
        a += 1