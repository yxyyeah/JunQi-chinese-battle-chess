import pygame
import os
import game_func
from settings import Settings
from button import Button

def run_game():
    pygame.init()
    pygame.mixer.init()

    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.mouse.set_visible(False)

    settings = Settings()
    screen = settings.screen
    pygame.display.set_caption('Battle Chess')
    
    settings.play_button = Button(screen,settings,'Play')
    chesses = []
    dead_chesses = []
    game_func.create_whole_chess(settings,chesses,screen)
    settings.chesses = chesses[:]

    while True:
        for event in pygame.event.get():
            if not settings.game_end and not settings.game_rewind:
                game_func.check_event_ingame(chesses,settings,dead_chesses,screen,event)
            if settings.game_rewind:
                game_func.check_event_gamerewind(chesses,settings,dead_chesses,screen,event)
            if settings.game_end:
                game_func.check_event_gameend(chesses,settings,dead_chesses,screen,event)
            game_func.check_event_display(chesses,settings,dead_chesses,screen,event)

        game_func.update_screen(settings,screen,chesses,dead_chesses,
                                                        settings.play_button)

run_game()