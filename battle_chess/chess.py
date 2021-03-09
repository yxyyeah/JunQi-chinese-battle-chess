import pygame
from pygame.sprite import Sprite
import pygame.font
import random

class Chess(Sprite):
    def __init__(self,screen,settings):
        super().__init__()
        self.screen = screen
        self.rect_out = pygame.Rect(0,0,settings.chess_width_out,
                                            settings.chess_height_out)
        self.rect_in = pygame.Rect(0,0,settings.chess_width_in,
                                                settings.chess_height_in)
        self.chess_color_out = settings.chess_color_back
        self.chess_color_in = settings.chess_color_back
        self.text_color = settings.text_color_red
        self.font = settings.font
        self.rect_out.x = 0
        self.rect_out.y = 0

        self.msg = ''

        self.covered = True
        self.dead = False
        self.move = True

        self.identity = ''
        self.rank = 0
#the position on the chess board
        self.pos = 0
#chess can only be moved if chess.move_control == settings.move_control
#red -> 1, black -> -1
        self.move_control = 0

        self.angle = self.random_angle()

    def update_msg(self,msg):
        '''let the text move when rect moves'''
        self.msg_image = self.font.render(msg,True,self.text_color,
                                                   self.chess_color_in)
        self.msg_image = pygame.transform.rotate(self.msg_image,self.angle)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect_out.center

    def update_layer(self):
        '''let the inside layer of chess move when the outside layer moves'''
        self.rect_in.center = self.rect_out.center
    
    def random_angle(self):
        '''decide if the rotation of the font is clockwise or anti'''
        n = random.randint(0,1)
        if n == 0:
            angle = 90
            return angle
        else:
            angle = -90
            return angle

    def draw_chess(self):
        pygame.draw.rect(self.screen,self.chess_color_out,self.rect_out)
        pygame.draw.rect(self.screen,self.chess_color_in,self.rect_in)        
        self.screen.blit(self.msg_image,self.msg_image_rect)
