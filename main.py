#pip installed/defalt libs
import pygame #Pygame cuz its a game
from pygame.locals import *
import time
#for networking (if i get around to it)
import socket
from pypresence import Presence, exceptions #For discord presence
import os
import threading
#game files
import Combat
icon = pygame.image.load("Assets\Icon.png")
menu_background = pygame.image.load("Assets\Openbook.png")
running = True

pid = os.getpid()
client_id = "1336631328195481722"
epoch = int(time.time())

def try_connect(RPC, success_flag):
    try:
        RPC.connect()
        success_flag.append(True)
    except exceptions as e:  # Catches Discord-related issues
        print(f"Failed to connect: {e}")
    except Exception as e:
        print(f"Failed to connect: {e}")

def connect_rpc(client_id, pid):
    RPC = Presence(client_id)
    success_flag = []
    thread = threading.Thread(target=try_connect, args=(RPC, success_flag))
    thread.start()
    thread.join(timeout=5)  # Wait for max 5 seconds

    if not success_flag:
        print("Connection timed out. Skipping...")
        return None

    RPC.update(
        pid=pid,
        state="Preparing for battle",
        details="current opponent: None",
        start=int(time.time()), 
        large_image="icon",
        large_text="The Enchanters Book awaits...."
    )
    return RPC, success_flag

RPC, Connect = connect_rpc(client_id, pid)



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
selector = pygame.image.load("Assets\Selector.jpg") #235x119 size

selector_enchater = SpeechFont.render('Mage', False, (255, 255, 255))
selector_monarch = SpeechFont.render('Monarch', False, (255, 255, 255))
selector_madman = SpeechFont.render('Madman', False, (255, 255, 255))


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
    selector.set_alpha(a)
    gameDisplay.blit(selector, (192, 850))
    gameDisplay.blit(menu_background, (632, 320))
    gameDisplay.blit(title, (770, 400))
    gameDisplay.blit(play, (930, 550))
    gameDisplay.blit(_quit, (930, 600))
    pygame.display.update()   
hover_enchanter = False
hover_monarch = False
hover_madman = False
ai = 'enchanter'

while running:
    RPC.update(
        pid=pid,
        state="Preparing for battle",
        details=f"Current opponent: {ai.capitalize()}",
        start=epoch, 
        large_image="icon",
        large_text="The Enchanters Book awaits....")
    gameDisplay.blit(selector, (192, 850))
    gameDisplay.blit(menu_background, (632, 320))
    gameDisplay.blit(title, (770, 400))
    gameDisplay.blit(play, (930, 550))
    gameDisplay.blit(_quit, (930, 600))
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
            running = False
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            #select opponent
            if event.pos[0] in range(192, 427, 1) and event.pos[1] in range(850, 969, 1):
                if event.pos[0] in range(192, int(192+(235/3)), 1):
                    ai = 'enchanter'
                elif event.pos[0] in range(int(192+(235/3)), int(192+(235/3)*2), 1):
                    ai = 'monarch'
                elif event.pos[0] in range(int(192+(235/3)*2), 427, 1):
                    ai = 'madman'
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
                    Again = Combat.BatStart(ai, gameDisplay, Connect, RPC, pid)
                running = False
            elif event.pos[0] in range(930, 1000, 1) and event.pos[1] in range(600,630, 1):
                running = False
        if event.type == MOUSEMOTION:
            #selector, showing names of villians on hover, each villian is 1/3 of the assets width
            if event.pos[0] in range(192, 427, 1) and event.pos[1] in range(850, 969, 1):
                if event.pos[0] in range(192, int(192+(235/3)), 1):
                    hover_enchanter = True
                    hover_monarch = False
                    hover_madman = False
                elif event.pos[0] in range(int(192+(235/3)), int(192+(235/3)*2), 1):
                    hover_enchanter = False
                    hover_monarch = True
                    hover_madman = False
                elif event.pos[0] in range(int(192+(235/3)*2), 427, 1):
                    hover_enchanter = False
                    hover_monarch = False
                    hover_madman = True
            else:
                hover_enchanter = False
                hover_monarch = False
                hover_madman = False

    mouseloc = pygame.mouse.get_pos()
    if hover_enchanter:
        text_rect = selector_enchater.get_rect(topleft=mouseloc)
        pygame.draw.rect(gameDisplay, (0, 0, 0), text_rect)
        gameDisplay.blit(selector_enchater, mouseloc)
    elif hover_monarch:
        text_rect = selector_monarch.get_rect(topleft=mouseloc)
        pygame.draw.rect(gameDisplay, (0, 0, 0), text_rect)
        gameDisplay.blit(selector_monarch, mouseloc)
    elif hover_madman:
        text_rect = selector_madman.get_rect(topleft=mouseloc)
        pygame.draw.rect(gameDisplay, (0, 0, 0), text_rect)
        gameDisplay.blit(selector_madman, mouseloc)
    pygame.display.flip()
    gameDisplay.fill((0, 0, 0))


# - constant game speed / FPS -

    clock.tick(100)
    