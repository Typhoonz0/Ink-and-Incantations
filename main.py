#pip installed/defalt libs
import pygame #Pygame cuz its a game
from pygame.locals import *
import time
 #for networking (if i get around to it)
from pypresence import Presence #For discord presence
import os

#game files
import Combat

icon = pygame.image.load("Assets\Icon.png")
menu_background = pygame.image.load("Assets\Openbook.png")
running = True

pid = os.getpid()
client_id = "1336631328195481722"
epoch = int(time.time())
RPC = Presence(client_id)
RPC.connect()

RPC.update(
    pid=pid,
    state="Dev testing",
    details="Inking and Incanting",
    start=int(time.time()), 
    large_image="icon",
    large_text="The Enchanters Book awaits...."
)



clock = pygame.time.Clock()
pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_icon(icon)
gameDisplay = pygame.display.set_mode((1920,1080))
pygame.display.set_caption('Ink and Incantations')
gameDisplay.fill((0,0,0))
pygame.mixer.music.load("Assets\Music\dark-fantasy-ambient-dungeon-synth-248213.mp3")
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(1)

TitleFont = pygame.font.Font("""Assets\Fonts\Books-Vhasenti.ttf""", 50)
SpeechFont = pygame.font.Font("""Assets\Fonts\Speech.ttf""", 30)
title = TitleFont.render('Ink & Incantations', True, (255, 0, 255))
play = SpeechFont.render('PLAY', True, (255, 255, 255))
_quit = SpeechFont.render('QUIT', True, (255, 255, 255))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
            running = False
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if event.pos[0] in range(930, 1000, 1) and event.pos[1] in range(550,575, 1):
                a = 255
                v = 1
                for i in range(255):
                    gameDisplay.fill((0, 0, 0))
                    a -=1
                    v -= 0.004
                    pygame.mixer.music.set_volume(v)
                    title.set_alpha(a)
                    play.set_alpha(a)
                    _quit.set_alpha(a)
                    menu_background.set_alpha(a)
                    gameDisplay.blit(menu_background, (632, 320))
                    gameDisplay.blit(title, (770, 400))
                    gameDisplay.blit(play, (930, 550))
                    gameDisplay.blit(_quit, (930, 600))
                    pygame.time.delay(10)
                    pygame.display.update()
                time.sleep(3)    

                Combat.BatStart()
                running = False
            elif event.pos[0] in range(930, 1000, 1) and event.pos[1] in range(600,630, 1):
                running = False


    gameDisplay.blit(menu_background, (632, 320))
    gameDisplay.blit(title, (770, 400))
    gameDisplay.blit(play, (930, 550))
    gameDisplay.blit(_quit, (930, 600))
    pygame.display.flip()
    gameDisplay.fill((0, 0, 0))



# - constant game speed / FPS -

    clock.tick(100)