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
# RPC = Presence(client_id)
# RPC.connect()
# RPC.update(
#     pid=pid,
#     state="Dev testing",
#     details="Inking and Incanting",
#     start=int(time.time()), 
#     large_image="icon",
#     large_text="The Enchanters Book awaits...."
# )



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
pygame.mixer.music.set_volume(0)

TitleFont = pygame.font.Font("""Assets\Fonts\Books-Vhasenti.ttf""", 50)
SpeechFont = pygame.font.Font("""Assets\Fonts\Speech.ttf""", 30)
title = TitleFont.render('Ink & Incantations', False, (255, 0, 255))
play = SpeechFont.render('PLAY', False, (255, 255, 255))
warning = TitleFont.render('Warning: This game is work in progress, some fueatures are incomplete', False, (255, 0, 0))
note = SpeechFont.render('Pygame is a little bit weird and scales the screen based on your windows display settings', False, (255, 255, 255))
note2 = SpeechFont.render('The game is designed for a 1920x1080 display @ 125% scaling', False, (255, 255, 255))
_quit = SpeechFont.render('QUIT', False, (255, 255, 255))
a = 0
for i in range(255):
    gameDisplay.fill((0, 0, 0))
    a += 1
    warning.set_alpha(a)
    note.set_alpha(a)
    note2.set_alpha(a)
    gameDisplay.blit(warning, (300, 400))
    gameDisplay.blit(note, (500, 550))
    gameDisplay.blit(note2, (500, 600))
    pygame.display.update()

gameDisplay.fill((0, 0, 0))
gameDisplay.blit(warning, (300, 400))
gameDisplay.blit(note, (500, 550))
gameDisplay.blit(note2, (500, 600))
pygame.display.update()
skip = False
for i in range(4000):
    if skip:
        break
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            skip = True
    pygame.time.delay(1)


for i in range(255):
    gameDisplay.fill((0, 0, 0))
    a -= 1
    warning.set_alpha(a)
    note.set_alpha(a)
    note2.set_alpha(a)
    gameDisplay.blit(warning, (300, 400))
    gameDisplay.blit(note, (500, 550))
    gameDisplay.blit(note2, (500, 600))
    pygame.display.update()

a = 0
v = 0
for i in range(255):
    gameDisplay.fill((0, 0, 0))
    a +=1
    v += 0.004
    pygame.mixer.music.set_volume(v)
    title.set_alpha(a)
    play.set_alpha(a)
    _quit.set_alpha(a)
    menu_background.set_alpha(a)
    gameDisplay.blit(menu_background, (632, 320))
    gameDisplay.blit(title, (770, 400))
    gameDisplay.blit(play, (930, 550))
    gameDisplay.blit(_quit, (930, 600))
    pygame.display.update()   

ai = 'enchanter'
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
                    pygame.time.delay(1)
                    pygame.display.update()
                pygame.time.delay(1000)   
                Again = True
                while Again:
                    Again = Combat.BatStart(ai, gameDisplay)
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
    