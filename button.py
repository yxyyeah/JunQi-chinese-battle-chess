import pygame

class Button():
    def __init__(self,screen,settings,msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings

        self.button_in = pygame.Rect(0,0,settings.play_width_in,settings.play_height_in)
        self.button_in.center = self.screen_rect.center
        self.button_out = pygame.Rect(0,0,settings.play_width_out,settings.play_height_out)
        self.button_out.center = self.screen_rect.center
        self.color_in = settings.play_button_color_in_1
        self.prep_msg(msg)

    def prep_msg(self,msg):
        self.msg_image = self.settings.play_font.render(msg,True,
                self.settings.play_text_color,self.color_in)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.button_in.center
    
    def draw_button(self):
        pygame.draw.rect(self.screen,self.settings.play_button_color_out,
                                                                self.button_out)
        pygame.draw.rect(self.screen,self.color_in,self.button_in)     
        self.screen.blit(self.msg_image,self.msg_image_rect)

    def normal_button(self,msg):
        self.color_in = self.settings.play_button_color_in_1
        self.msg_image = self.settings.play_font.render(msg,True,
                self.settings.play_text_color,self.color_in)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.button_in.center
    
    def touched_button(self,msg):
        self.color_in = self.settings.play_button_color_in_2
        self.msg_image = self.settings.play_font.render(msg,True,
                self.settings.play_text_color,self.color_in)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.button_in.center