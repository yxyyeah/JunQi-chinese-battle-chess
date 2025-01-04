import pygame

class Board():
    def __init__(self,settings,screen):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.rect = pygame.Rect(0,0,settings.board_width,settings.board_height)
        self.rect.center = self.screen_rect.center
        self.rect_color = settings.board_color
        self.text_color = settings.notice_color
        self.font = settings.board_font
        self.notice = ''
        
        self.lining_1 = pygame.Rect(0,0,settings.yesorno_lining_width,
                                                settings.yesorno_lining_height)     #no_rect
        self.lining_2 = pygame.Rect(0,0,settings.yesorno_lining_width,
                                                settings.yesorno_lining_height)     #yes_rect
        self.yes_rect = pygame.Rect(0,0,settings.yesorno_width,
                                                    settings.yesorno_height)
        self.no_rect = pygame.Rect(0,0,settings.yesorno_width,
                                                    settings.yesorno_height)
        self.yes_text = 'Yes'
        self.no_text = 'Cancel'
        self.yes_color = settings.yesorno_color
        self.no_color = settings.yesorno_color
        self.yesorno_color = settings.yesorno_color
        self.yesorno_colort = settings.yesorno_colort
        self.yesorno_lining_color = settings.yesorno_lining_color
        
        self.position(settings)

    def position(self,settings):
        '''arrange the position of the rects'''
        self.lining_1.bottomright = self.rect.bottomright
        self.lining_2.right = self.lining_1.left - settings.yesno_spacing
        self.lining_2.bottom = self.rect.bottom
        self.yes_rect.center = self.lining_2.center
        self.no_rect.center = self.lining_1.center

    def prep_text(self,msg):
        self.msg_image = self.font.render(msg,True,self.text_color,
                                                        self.rect_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

        self.yes_image = self.font.render(self.yes_text,True,self.text_color,
                                                        self.yes_color)
        self.yes_image_rect = self.yes_image.get_rect()
        self.yes_image_rect.center = self.yes_rect.center

        self.no_image = self.font.render(self.no_text,True,self.text_color,
                                                        self.no_color)
        self.no_image_rect = self.no_image.get_rect()
        self.no_image_rect.center = self.no_rect.center

    def draw_board(self):
        self.screen.fill(self.rect_color,self.rect)
        self.screen.fill(self.yesorno_lining_color,self.lining_1)
        self.screen.fill(self.yesorno_lining_color,self.lining_2)
        self.screen.fill(self.yes_color,self.yes_rect)
        self.screen.fill(self.no_color,self.no_rect)
        self.screen.blit(self.msg_image,self.msg_image_rect)
        self.screen.blit(self.yes_image,self.yes_image_rect)
        self.screen.blit(self.no_image,self.no_image_rect)

    def touched_yes(self):
        self.yes_color = self.yesorno_colort

        self.yes_image = self.font.render(self.yes_text,True,self.text_color,
                                                        self.yes_color)
        self.yes_image_rect = self.yes_image.get_rect()
        self.yes_image_rect.center = self.yes_rect.center

    def normal_yes(self):
        self.yes_color = self.yesorno_color

        self.yes_image = self.font.render(self.yes_text,True,self.text_color,
                                                        self.yes_color)
        self.yes_image_rect = self.yes_image.get_rect()
        self.yes_image_rect.center = self.yes_rect.center

    def touched_no(self):
        self.no_color = self.yesorno_colort
        
        self.no_image = self.font.render(self.no_text,True,self.text_color,
                                                        self.no_color)
        self.no_image_rect = self.no_image.get_rect()
        self.no_image_rect.center = self.no_rect.center
    
    def normal_no(self):
        self.no_color = self.yesorno_color
        
        self.no_image = self.font.render(self.no_text,True,self.text_color,
                                                        self.no_color)
        self.no_image_rect = self.no_image.get_rect()
        self.no_image_rect.center = self.no_rect.center
          