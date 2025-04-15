# pip installed/default libs
import pygame  # Pygame cuz it's a game
from pygame.locals import *
import time
import os
import multiprocessing  # Replacing threading with multiprocessing
from pypresence import Presence, exceptions  # For Discord presence
import Combat
import SaveUpdater

flags = FULLSCREEN | DOUBLEBUF

def try_connect(client_id, success_flag):
    """
    Create the Presence object inside the child process and attempt to connect.
    """
    try:
        RPC = Presence(client_id)
        RPC.connect()
        success_flag.value = True
    except exceptions as e:  # Catches Discord-related issues
        print(f"Failed to connect: {e}")
    except Exception as e:
        print(f"Failed to connect: {e}")


def connect_rpc(client_id):
    """
    Use multiprocessing to attempt connecting to Discord RPC.
    """
    success_flag = multiprocessing.Value('b', False)  # Shared boolean value
    process = multiprocessing.Process(target=try_connect, args=(client_id, success_flag))
    process.start()
    process.join(timeout=5)  # Wait for max 5 seconds

    if not success_flag.value:
        print("Connection timed out. Skipping...")
        return None
    else:
        print("Connected to Discord RPC.")
        # Return a new Presence object for the main process
        RPC = Presence(client_id)
        RPC.connect()
        return RPC, success_flag.value


if __name__ == "__main__":
    # Ensure multiprocessing works correctly on Windows
    multiprocessing.freeze_support()

    # Initialize Pygame
    pygame.init()
    pygame.font.init()
    pygame.mixer.init()

    # Get screen dimensions dynamically
    screen_info = pygame.display.Info()
    screen_width, screen_height = screen_info.current_w, screen_info.current_h
    print(screen_width, screen_height)
    # Initialize display
    gameDisplay = pygame.display.set_mode((screen_width, screen_height), flags)
    pygame.display.set_caption('Ink and Incantations')
    gameDisplay.fill((0, 0, 0))

    # Load assets
    icon = pygame.image.load(os.path.join("Assets", "Icon.png"))
    menu_background = pygame.image.load(os.path.join("Assets", "Openbook.png"))
    selector = pygame.image.load(os.path.join("Assets", "Selector.jpg"))  # 235x119 size
    pygame.display.set_icon(icon)
    if not SaveUpdater.decode_save_file()['shut_up']:
        music = pygame.mixer.Sound(os.path.join("Assets", "Music", "last-fight-dungeon-synth-music-281592.mp3"))
        music.set_volume(1)
        music.play(-1)  # Loop the music indefinitely


    # Scale factor for all assets
    SCALE_FACTOR = 1.25

    # Scale images dynamically
    menu_background = pygame.transform.scale(
        menu_background,
        (int(menu_background.get_width() * SCALE_FACTOR), int(menu_background.get_height() * SCALE_FACTOR))
    )
    selector = pygame.transform.scale(
        selector,
        (int(selector.get_width() * SCALE_FACTOR), int(selector.get_height() * SCALE_FACTOR))
    )

    # Scale fonts dynamically
    title_font_size = int(screen_height * 0.05 * SCALE_FACTOR)
    speech_font_size = int(screen_height * 0.03 * SCALE_FACTOR)
    TitleFont = pygame.font.Font(os.path.join("Assets", "Fonts", "Books-Vhasenti.ttf"), title_font_size)
    SpeechFont = pygame.font.Font(os.path.join("Assets", "Fonts", "Speech.ttf"), speech_font_size)

    # Render scaled text
    title = TitleFont.render('Ink & Incantations', False, (255, 0, 255))
    play = SpeechFont.render('PLAY', False, (255, 255, 255))
    if not SaveUpdater.decode_save_file()['holy_yap']:
        warning = TitleFont.render('Warning: This game is work in progress, some features are incomplete', False, (255, 0, 0))
    _quit = SpeechFont.render('QUIT', False, (255, 255, 255))

    selector_enchanter = SpeechFont.render('Mage', False, (255, 255, 255))
    selector_monarch = SpeechFont.render('Monarch', False, (255, 255, 255))
    selector_madman = SpeechFont.render('Madman', False, (255, 255, 255))

    # Center elements dynamically
    title_rect = title.get_rect(center=(screen_width // 2, screen_height * 0.3))
    play_rect = play.get_rect(center=(screen_width // 2, screen_height * 0.5))
    quit_rect = _quit.get_rect(center=(screen_width // 2, screen_height * 0.55))
    menu_background_rect = menu_background.get_rect(center=(screen_width // 2, screen_height // 2))

    # Discord RPC
    pid = os.getpid()
    client_id = "1336631328195481722"
    epoch = int(time.time())
    if SaveUpdater.decode_save_file()['i_dont_want_discord']:
        Connect = False
        RPC = Presence("1336631328195481722")
    else:
        try:
            RPC, Connect = connect_rpc(client_id)
        except Exception as e:
            print(f"Failed to connect to Discord RPC: {e}")
            Connect = False
            RPC = Presence(client_id)

    # Main menu and game logic
    running = True
    if not SaveUpdater.decode_save_file()['holy_yap']:
        a = 0
        for i in range(255):
            gameDisplay.fill((0, 0, 0))
            a += 1
            warning.set_alpha(a)

            gameDisplay.blit(warning, (screen_width * 0.025, screen_height * 0.4))

            pygame.display.update()

        gameDisplay.fill((0, 0, 0))
        gameDisplay.blit(warning, (screen_width * 0.025, screen_height * 0.4))
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

            gameDisplay.blit(warning, (screen_width * 0.025, screen_height * 0.4))
    
            pygame.display.update()

    a = 0
    v = 0
    for i in range(255):
        gameDisplay.fill((0, 0, 0))
        a += 1
        v += 0.004
        pygame.mixer.music.set_volume(v)
        title.set_alpha(a)
        play.set_alpha(a)
        _quit.set_alpha(a)
        menu_background.set_alpha(a)
        selector.set_alpha(a)
        gameDisplay.blit(selector, (screen_width * 0, screen_height * 0.87))  # AI selector remains unchanged
        gameDisplay.blit(menu_background, menu_background_rect.topleft)
        gameDisplay.blit(title, title_rect.topleft)
        gameDisplay.blit(play, play_rect.topleft)
        gameDisplay.blit(_quit, quit_rect.topleft)
        pygame.display.update()

    hover_enchanter = False
    hover_monarch = False
    hover_madman = False
    ai = 'enchanter'

    while running:
        if Connect:
            RPC.update(
                pid=pid,
                state="Preparing for battle",
                details=f"Current opponent: {ai.capitalize()}",
                start=epoch,
                large_image="icon",
                large_text="The Enchanters Book awaits....")
        gameDisplay.blit(selector, (0, screen_height * 0.87))  # AI selector remains unchanged
        gameDisplay.blit(menu_background, menu_background_rect.topleft)
        gameDisplay.blit(title, title_rect.topleft)
        gameDisplay.blit(play, play_rect.topleft)
        gameDisplay.blit(_quit, quit_rect.topleft)
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                running = False
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                # Select opponent
                if event.pos[0] in range(int(screen_width * 0), int(screen_width * 0 + selector.get_width()), 1) and event.pos[1] in range(int(screen_height * 0.8), int(screen_height * 0.8 + selector.get_height()), 1):
                    if event.pos[0] in range(int(screen_width * 0), int(screen_width * 0 + (selector.get_width() / 3)), 1):
                        ai = 'enchanter'
                    elif event.pos[0] in range(int(screen_width * 0 + (selector.get_width() / 3)), int(screen_width * 0 + (selector.get_width() / 3) * 2), 1):
                        ai = 'monarch'
                    elif event.pos[0] in range(int(screen_width * 0 + (selector.get_width() / 3) * 2), int(screen_width * 0 + selector.get_width()), 1):
                        ai = 'madman'
                # PLAY button
                if event.pos[0] in range(play_rect.left - 10, play_rect.right + 10) and event.pos[1] in range(play_rect.top - 10, play_rect.bottom + 10):
                    a = 255
                    v = 1
                    if not SaveUpdater.decode_save_file()['holy_yap']:
                        for i in range(255):
                            gameDisplay.fill((0, 0, 0))
                            a -= 1
                            v -= 0.004
                            pygame.mixer.music.set_volume(v)
                            title.set_alpha(a)
                            play.set_alpha(a)
                            _quit.set_alpha(a)
                            menu_background.set_alpha(a)
                            selector.set_alpha(a)
                            gameDisplay.blit(selector, (screen_width * 0, screen_height * 0.87))
                            gameDisplay.blit(menu_background, menu_background_rect.topleft)
                            gameDisplay.blit(title, title_rect.topleft)
                            gameDisplay.blit(play, play_rect.topleft)
                            gameDisplay.blit(_quit, quit_rect.topleft)
                            pygame.time.delay(1)
                            pygame.display.update()
                        pygame.time.delay(1000)
                        Again = True
                        while Again:
                            if not SaveUpdater.decode_save_file()['shut_up']:
                                music.stop()
                            gameDisplay.fill((0, 0, 0))
                        
                    Again = Combat.BatStart(ai, gameDisplay, Connect, RPC, pid)
                    running = False
                # QUIT button
                elif event.pos[0] in range(quit_rect.left - 10, quit_rect.right + 10) and event.pos[1] in range(quit_rect.top - 10, quit_rect.bottom + 10):
                    running = False
        if event.type == MOUSEMOTION:
            # Selector, showing names of villains on hover, each villain is 1/3 of the assets width
            if event.pos[0] in range(int(screen_width * 0), int(screen_width * 0 + selector.get_width()), 1) and event.pos[1] in range(int(screen_height * 0.8), int(screen_height * 0.8 + selector.get_height()), 1):
                if event.pos[0] in range(int(screen_width * 0), int(screen_width * 0 + (selector.get_width() / 3)), 1):
                    hover_enchanter = True
                    hover_monarch = False
                    hover_madman = False
                elif event.pos[0] in range(int(screen_width * 0 + (selector.get_width() / 3)), int(screen_width * 0 + (selector.get_width() / 3) * 2), 1):
                    hover_enchanter = False
                    hover_monarch = True
                    hover_madman = False
                elif event.pos[0] in range(int(screen_width * 0 + (selector.get_width() / 3) * 2), int(screen_width * 0 + selector.get_width()), 1):
                    hover_enchanter = False
                    hover_monarch = False
                    hover_madman = True
            else:
                hover_enchanter = False
                hover_monarch = False
                hover_madman = False

        mouseloc = pygame.mouse.get_pos()
        if hover_enchanter:
            text_rect = selector_enchanter.get_rect(bottomleft=mouseloc)
            pygame.draw.rect(gameDisplay, (0, 0, 0), text_rect)
            gameDisplay.blit(selector_enchanter, text_rect.topleft)
        elif hover_monarch:
            text_rect = selector_monarch.get_rect(bottomleft=mouseloc)
            pygame.draw.rect(gameDisplay, (0, 0, 0), text_rect)
            gameDisplay.blit(selector_monarch, text_rect.topleft)
        elif hover_madman:
            text_rect = selector_madman.get_rect(bottomleft=mouseloc)
            pygame.draw.rect(gameDisplay, (0, 0, 0), text_rect)
            gameDisplay.blit(selector_madman, text_rect.topleft)
        pygame.display.flip()
        gameDisplay.fill((0, 0, 0))

