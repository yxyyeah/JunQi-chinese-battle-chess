import pygame
import win32api,win32con
class Settings():
    
    def __init__(self):

    #screen
        self.screen_width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        self.screen_height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        self.bg_color = (0,0,0)
        self.fullscreen = True
        self.screen = pygame.display.set_mode(
                    (self.screen_width,self.screen_height),pygame.FULLSCREEN)
        self.screen_rect = self.screen.get_rect()
    
    #red half bg - used to indicate who goes first
        self.half_red_bg = pygame.Rect(0,0,int(self.screen_width/2),
                                                    self.screen_height)
        self.color_red = (255,0,0)

    #bg image
        f=r'images\1536_864.jpg'
        try:
            bg_image = pygame.image.load(f)
        except FileNotFoundError:
            f=r'C:\Users\AAAAA\Desktop\python_work\battle_chess\images\1536_864.jpg'
            bg_image = pygame.image.load(f)
        self.bg_image_width = int(self.screen_width/1.32)
        self.bg_image_height = int(1147*self.bg_image_width/1749)
        bg_image_size = (self.bg_image_width,self.bg_image_height)
        self.bg_image = pygame.transform.scale(bg_image,bg_image_size)
        self.bg_image_rect = self.bg_image.get_rect()
        self.bg_image_rect.center = self.screen_rect.center

    #mouse image
    #palm image
        f = r'images\palm.png'
        try:
            palm_image = pygame.image.load(f)
        except FileNotFoundError:
            f=r'C:\Users\AAAAA\Desktop\python_work\battle_chess\images\palm.png'
            palm_image = pygame.image.load(f)
        self.palm_image_width = int(self.screen_width/1280*25)
        self.palm_image_height = self.palm_image_width
        palm_image_size = (self.palm_image_width,self.palm_image_height)
        self.palm_image = pygame.transform.scale(palm_image,palm_image_size)
        self.palm_image_rect = self.palm_image.get_rect()
    #fist image
        f = r'images\fist.png'
        try:
            fist_image = pygame.image.load(f)
        except FileNotFoundError:
            f=r'C:\Users\AAAAA\Desktop\python_work\battle_chess\images\fist.png'
            fist_image = pygame.image.load(f)
        self.fist_image_width = int(self.screen_width/1280*25*1.2)
        self.fist_image_height = self.fist_image_width
        fist_image_size = (self.fist_image_width,self.fist_image_height)
        self.fist_image = pygame.transform.scale(fist_image,fist_image_size)
        self.fist_image_rect = self.fist_image.get_rect()
    #mouse image
        self.mouse_image = self.palm_image
        self.mouse_image_rect = self.mouse_image.get_rect()

    #mouse enter pygame display
        self.mouse_enter = False

    #win_image
        f = r'images\victory.jpg'
        try:
            self.win_image = pygame.image.load(f).convert()
        except FileNotFoundError:
            f=r'C:\Users\AAAAA\Desktop\python_work\battle_chess\images\victory.jpg'
            self.win_image = pygame.image.load(f).convert()
        self.alpha_value = 0
        self.win_image_width = int(self.screen_width/1280*774)
        self.win_image_height = int(self.win_image_width/774*215)
        win_image_size = (self.win_image_width,self.win_image_height)
        self.win_image = pygame.transform.scale(self.win_image,win_image_size)

    #tie image
    #normal
        f = r'images\tie_flag.png'
        try:
            self.tie_image = pygame.image.load(f)
        except FileNotFoundError:
            f=r'C:\Users\AAAAA\Desktop\python_work\battle_chess\images\tie_flag.png'
            self.tie_image = pygame.image.load(f)
        self.tie_image_width = int(5*self.screen_width/128)
        self.tie_image_height = self.tie_image_width
        tie_image_size = (self.tie_image_width,self.tie_image_height)
        self.tie_image = pygame.transform.scale(self.tie_image,tie_image_size)
        self.tie_image_rect = self.tie_image.get_rect()
        self.tie_image_rect.bottom = self.screen_rect.bottom
        self.tie_image_rect.left=self.screen_rect.left+self.screen_width/64
    #big
        self.tie_imageb = pygame.image.load(f)
        self.tie_imageb_width = int(60*self.screen_width/128)
        self.tie_imageb_height = self.tie_imageb_width
        tie_imageb_size = (self.tie_imageb_width,self.tie_imageb_height)
        self.tie_imageb=pygame.transform.scale(self.tie_imageb,tie_imageb_size)
        self.tie_imageb_rect = self.tie_imageb.get_rect()
        self.tie_imageb_rect.centerx = self.screen_rect.centerx
        self.tie_imageb_rect.centery = -self.tie_imageb_height/2
    #transparent
        f = r'images\tie_flagt.png'
        try:
            self.tie_imaget = pygame.image.load(f)
        except FileNotFoundError:
            f=r'C:\Users\AAAAA\Desktop\python_work\battle_chess\images\tie_flagt.png'
            self.tie_imaget = pygame.image.load(f)
        self.tie_imaget = pygame.transform.scale(self.tie_imaget,tie_image_size)
        self.tie_imaget_rect = self.tie_imaget.get_rect()
        self.tie_imaget_rect.bottom = self.screen_rect.bottom
        self.tie_imaget_rect.left=self.screen_rect.left+self.screen_width/64
    #tie flag
        self.tie_flag = self.tie_imaget
        self.tie_flag_rect = self.tie_imaget_rect

    #white flag image
    #normal
        f = r'images\wh_flag.png'
        try:
            self.wh_image = pygame.image.load(f)
        except FileNotFoundError:
            f=r'C:\Users\AAAAA\Desktop\python_work\battle_chess\images\wh_flag.png'
            self.wh_image = pygame.image.load(f)
        self.wh_image_width = self.tie_image_width
        wh_image_size = (self.wh_image_width,self.wh_image_width)
        self.wh_image = pygame.transform.scale(self.wh_image,wh_image_size)
        self.wh_image_rect = self.wh_image.get_rect()
        self.wh_image_rect.bottom = self.screen_rect.bottom
        self.wh_image_rect.left=self.tie_imaget_rect.right+3*self.screen_width/128
    #transparent
        f = r'images\wh_flagt.png'
        try:
            self.wht_image = pygame.image.load(f)
        except FileNotFoundError:
            f=r'C:\Users\AAAAA\Desktop\python_work\battle_chess\images\wh_flagt.png'
            self.wht_image = pygame.image.load(f)
        self.wht_image = pygame.transform.scale(self.wht_image,wh_image_size)
        self.wht_image_rect = self.wht_image.get_rect()
        self.wht_image_rect.bottom = self.screen_rect.bottom
        self.wht_image_rect.left=self.tie_imaget_rect.right+3*self.screen_width/128
    #white flag
        self.wh_flag = self.wht_image
        self.wh_flag_rect = self.wht_image_rect

    #detective image used for blit flag image
        self.detec_width = 250*self.screen_width/1280
        self.detec_height = 150*self.screen_width/1280
        self.detec_rect = pygame.Rect(0,0,self.detec_width,self.detec_height)
        self.detec_rect.bottomleft = self.screen_rect.bottomleft

        self.detec_active = False

    #notice board
        self.board_width = self.screen_width
        self.board_height = int(self.screen_width/12.8)
        self.board_color = (0,42,255)
        self.notice_color = (255,255,255)
        self.yesorno_lining_width = int(self.screen_width/12.8)
        self.yesorno_lining_height = int(self.yesorno_lining_width*3/10)
        self.yesorno_width = int(self.yesorno_lining_width*0.96)
        self.yesorno_height = int(self.yesorno_lining_height*0.9)
        self.yesorno_lining_color = (255,255,255)
        self.yesorno_color = (0,190,255)
        self.yesorno_colort = (0,160,255)
        self.yesno_spacing = int(self.yesorno_lining_width*3/10)
        self.board_font = pygame.font.SysFont('calibri',23)
        self.board_appear = False

        self.board = None
    
    #chess
        self.chess_width_out = self.screen_width/26.4
        self.chess_height_out = self.chess_width_out*1.6
        self.chess_width_in = self.chess_width_out*0.85
        self.chess_height_in = self.chess_height_out*0.85
        self.chess_color_back = (0,0,0)
        self.chess_color_front = (255,255,255)
        self.chess_color_selected = (0,255,0)
        self.text_color_red = (255,0,0)
        self.text_color_black = (0,0,0)
        #get proper font size
        active = True
        self.fontsize = 1
        while active:
            self.font = pygame.font.SysFont('华文楷体',self.fontsize,0)
            self.test_image = self.font.render('测试',True,(0,0,0))
            self.test_image = pygame.transform.rotate(self.test_image,90)
            self.test_image_rect = self.test_image.get_rect()
            if self.test_image_rect[2] <= self.chess_width_in:
                self.fontsize += 1
            else:
                active = False
        self.font = pygame.font.SysFont('华文楷体',self.fontsize-1,0)
        #distribute chess position
        self.pos_num = 0

    #play button
        self.play_width_out = int(self.screen_width*25/192)
        self.play_height_out = int(self.play_width_out*0.4)
        self.play_width_in = int(self.play_width_out*0.92)
        self.play_height_in = int(self.play_height_out*0.8)
        self.play_button_color_in_1 = (0,230,0)
        self.play_button_color_in_2 = (0,200,0)
        self.play_button_color_out = (0,255,0)
        self.play_text_color = (0,0,0)
        self.play_font = pygame.font.SysFont('calibri',self.fontsize-1)

    #chess lines and rows spacing
        self.line_1_pos_x = (self.screen_width-self.bg_image_width)/2
        self.line_1_pos_x += self.bg_image_width/23
        self.line_1_pos_y = (self.screen_height-self.bg_image_height)/2
        self.line_1_pos_y += self.bg_image_height*0.084976308
        self.line_norm_spac = self.bg_image_width*83/1150
        self.line_spac_spec_1 = self.line_norm_spac*6/5 
        self.line_spac_spec_2 = self.line_norm_spac*5.8/2.5
        self.row_spac = self.line_norm_spac*4.7/2.5

    #dead chess spacing
        self.dead_pos_x = self.chess_height_out/2
        self.dead_pos_y = 0

    #chess pool
        self.chess_pool = [
            ('军旗',-2,self.text_color_red),('地雷',-1,self.text_color_red),
            ('地雷',-1,self.text_color_red),('地雷',-1,self.text_color_red),
            ('军旗',-2,self.text_color_black),('地雷',-1,self.text_color_black),
            ('地雷',-1,self.text_color_black),('地雷',-1,self.text_color_black),
            ('炸弹',0,self.text_color_red),('炸弹',0,self.text_color_red),
            ('炸弹',0,self.text_color_black),('炸弹',0,self.text_color_black),
            ('工兵',1,self.text_color_red),('工兵',1,self.text_color_red),
            ('工兵',1,self.text_color_red),('工兵',1,self.text_color_black),
            ('工兵',1,self.text_color_black),('工兵',1,self.text_color_black),
            ('排长',2,self.text_color_red),('排长',2,self.text_color_red),
            ('排长',2,self.text_color_red),('排长',2,self.text_color_black),
            ('排长',2,self.text_color_black),('排长',2,self.text_color_black),
            ('连长',3,self.text_color_red),('连长',3,self.text_color_red),
            ('连长',3,self.text_color_red),('连长',3,self.text_color_black),
            ('连长',3,self.text_color_black),('连长',3,self.text_color_black),
            ('营长',4,self.text_color_red),('营长',4,self.text_color_red),
            ('营长',4,self.text_color_black),('营长',4,self.text_color_black),
            ('团长',5,self.text_color_red),('团长',5,self.text_color_red),
            ('团长',5,self.text_color_black),('团长',5,self.text_color_black),
            ('旅长',6,self.text_color_red),('旅长',6,self.text_color_red),
            ('旅长',6,self.text_color_black),('旅长',6,self.text_color_black),
            ('师长',7,self.text_color_red),('师长',7,self.text_color_red),
            ('师长',7,self.text_color_black),('师长',7,self.text_color_black),
            ('军长',8,self.text_color_red),('军长',8,self.text_color_black),
            ('司令',9,self.text_color_red),('司令',9,self.text_color_black)
            ]

    #game status
        self.red_mine = 3
        self.black_mine = 3

        self.second = False
        #the two selected chess to move
        self.chess_1 = None
        self.chess_2 = None
        #chess_1 index cache
        self.chess1index = None
        #create an unchangable chesses index, used for determine move position
        #b/c at that time the moved one is removed from chesses
        #why need this? b/c in the determine_mov_pos func, it will need the index to locate.
        self.chesses = None
        #chess_1 center position cache used for moving chess_1, does not effect undo
        self.a = None
        #chess_1 moves with mouse
        self.chess_move = False

        self.dead_pool = []
        self.dead_num = 0
        #used to undo
        self.allow_undo = False

        #used to determine who's red and who's black
        self.color_confirmed = False
        self.count = 0
        self.move_1 = None      #used for determine who's red or black in func color_confirmed

        #used to determine who's turn is it, players MUST take turns to go
        #the alter_move_control is placed in the check ingame event func
        self.move_control = 0

        #put game win and game tie in game result as strs.
        self.game_result = None
        #game end is true when before pushing the play button, or a round ends
        self.game_end = True
        #determine whether one can admit tie or lose
        self.game_allow_end = False
        #when notice board pop up, game will not be active
        self.game_active = True
        #control game rewind, used in func rewind
        self.game_rewind = False
        #used to control if one side has no pieces then game end
        self.red_no_pieces = True
        self.black_no_pieces = True
        #used to indicate who goes first
        self.red_bg = False
        #used to show the order of play, also control the duration-3seconds
        self.show_order = False
        #used to show play button at the beginning
        self.play_button_on = True
        self.play_button = None
        #moved chess cache used for undo
        self.move_cache = []

        #used to compare steps moved to the records; and calculate time duration only once
        self.calculating = True
        #store the stat image
        self.draw_stat = None
        
        #calculate game duration, the start_time is stored right after botton click detected
        #end_time is stored when game result is win or tie in func update_screen
        self.start_time = None
        self.end_time = None

    #game statistics, reset each round
        self.player_1 = 'yxy'
        self.player_2 = 'yyg'
        #default: left -> player 1
        self.first_move = None
        self.steps_before_c_confirmed = 0
        self.player_1_color = None
        self.move_start = 0
        self.move_end = 0
        self.p1_movtime = 0
        self.p2_movtime = 0
        self.p1_steps = 0
        self.p2_steps = 0
        self.p1_units_destroyed = 0
        self.p2_units_destroyed = 0
        self.winner = None
        self.total_time_lasted = None
        self.total_steps_moved = None
    #win music
        f = r'victory.ogg'
        try:
            self.win_music = pygame.mixer.Sound(f)
        except FileNotFoundError:
            f=r'C:\Users\AAAAA\Desktop\python_work\battle_chess\victory.ogg'
            self.win_music = pygame.mixer.Sound(f)
        self.win_music.set_volume(0.2)
        self.win_music_play = False

    #variables related to free fall
        self.time_count = 0
        self.v = 0
        self.v_0 = 0
        self.down = True
        self.up = False
        self.x_0 = -self.tie_imageb_height/2
        self.y = 0

        self.free_fall = True

    def init_set(self):
        #game status
        self.red_mine = 3
        self.black_mine = 3

        self.second = False
        #the two selected chess to move
        self.chess_1 = None
        self.chess_2 = None
        self.chess1index = None
        self.chesses = None
        #chess_1 center cache
        self.a = None
        #chess_1 moves with mouse
        self.chess_move = False

        self.dead_pool = []
        self.dead_num = 0
        #used to undo
        self.allow_undo = False

        #used to determine who's red and who's black
        self.color_confirmed = False
        self.count = 0
        self.move_1 = None 
        self.move_control = 0

        self.game_result = None
        self.game_end = True
        #determine whether one can admit tie or lose
        self.game_allow_end = False
        self.game_active = True
        self.game_rewind = False
        self.red_no_pieces = True
        self.black_no_pieces = True
        self.move_cache = []
        self.calculating = True
        self.draw_stat = None
        self.win_music_play = False
        self.red_bg = False
        self.show_order = False
        self.play_button_on = True
        self.play_button = None
        self.start_time = None
        self.end_time = None

    #game statistics, reset each round
        self.player_1 = 'yxy'
        self.player_2 = 'yyg'
        #default: left -> player 1
        self.first_move = None
        self.steps_before_c_confirmed = 0
        self.player_1_color = None
        self.move_start = 0
        self.move_end = 0
        self.p1_movtime = 0
        self.p2_movtime = 0
        self.p1_steps = 0
        self.p2_steps = 0
        self.p1_units_destroyed = 0
        self.p2_units_destroyed = 0
        self.winner = None
        self.total_time_lasted = None
        self.total_steps_moved = None
        
        #distribute position
        self.pos_num = 0
        #variables related to free fall
        self.time_count = 0
        self.v = 0
        self.v_0 = 0
        self.down = True
        self.up = False
        self.x_0 = -self.tie_imageb_height/2
        self.y = 0

        self.free_fall = True

        #chess pool
        self.chess_pool = [
            ('军旗',-2,self.text_color_red),('地雷',-1,self.text_color_red),
            ('地雷',-1,self.text_color_red),('地雷',-1,self.text_color_red),
            ('军旗',-2,self.text_color_black),('地雷',-1,self.text_color_black),
            ('地雷',-1,self.text_color_black),('地雷',-1,self.text_color_black),
            ('炸弹',0,self.text_color_red),('炸弹',0,self.text_color_red),
            ('炸弹',0,self.text_color_black),('炸弹',0,self.text_color_black),
            ('工兵',1,self.text_color_red),('工兵',1,self.text_color_red),
            ('工兵',1,self.text_color_red),('工兵',1,self.text_color_black),
            ('工兵',1,self.text_color_black),('工兵',1,self.text_color_black),
            ('排长',2,self.text_color_red),('排长',2,self.text_color_red),
            ('排长',2,self.text_color_red),('排长',2,self.text_color_black),
            ('排长',2,self.text_color_black),('排长',2,self.text_color_black),
            ('连长',3,self.text_color_red),('连长',3,self.text_color_red),
            ('连长',3,self.text_color_red),('连长',3,self.text_color_black),
            ('连长',3,self.text_color_black),('连长',3,self.text_color_black),
            ('营长',4,self.text_color_red),('营长',4,self.text_color_red),
            ('营长',4,self.text_color_black),('营长',4,self.text_color_black),
            ('团长',5,self.text_color_red),('团长',5,self.text_color_red),
            ('团长',5,self.text_color_black),('团长',5,self.text_color_black),
            ('旅长',6,self.text_color_red),('旅长',6,self.text_color_red),
            ('旅长',6,self.text_color_black),('旅长',6,self.text_color_black),
            ('师长',7,self.text_color_red),('师长',7,self.text_color_red),
            ('师长',7,self.text_color_black),('师长',7,self.text_color_black),
            ('军长',8,self.text_color_red),('军长',8,self.text_color_black),
            ('司令',9,self.text_color_red),('司令',9,self.text_color_black)
            ]