import pygame
import os
from pygame.sprite import Group
import game_func
from settings import Settings

def run_game():
    pygame.init()
    pygame.mixer.init()

    os.environ['SDL_VIDEO_WINDOW_POS'] = '50,70'
    pygame.mouse.set_visible(False)

    settings = Settings()
    screen = settings.screen
    pygame.display.set_caption('Battle Chess')

    chesses = []
    dead_chesses = []
    game_func.create_whole_chess(settings,chesses,screen)
    settings.chesses = chesses[:]

    while True:
        game_func.check_event(chesses,settings,dead_chesses,screen)
        game_func.update_screen(settings,screen,chesses,dead_chesses)

run_game()