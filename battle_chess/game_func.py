import pygame
import sys
import random
import time
from chess import Chess
from board import Board
import subboard
from settings import Settings

def update_screen(settings,screen,chesses,dead_chesses):
    '''draw order: screen -> corner_flag -> chess -> dead_chess -> win/tie_sign  
    -> notice_board -> moving_chess -> mouse'''
    screen.fill(settings.bg_color)
    screen.blit(settings.bg_image,settings.bg_image_rect)
    #draw tie and white flag on corner
    if settings.detec_active:
        screen.blit(settings.tie_flag,settings.tie_flag_rect)
        screen.blit(settings.wh_flag,settings.wh_flag_rect)
    
    #game allow end controls whether chess has been uncovered
    settings.game_allow_end = True
    settings.red_no_pieces = True
    settings.black_no_pieces = True
    #draw chess
    for chess in chesses:
        if not chess.dead:
            chess.draw_chess()
        if chess.covered and settings.game_allow_end:
            settings.game_allow_end = False
        check_pieces(chess,settings)

    for chess in dead_chesses:
        chess.screen.fill(chess.chess_color_out,chess.rect_out)
        chess.screen.blit(chess.msg_image,chess.msg_image_rect)
    
    #game tie
    if settings.red_no_pieces and settings.black_no_pieces:
        settings.game_tie = True
    #game win
    elif settings.red_no_pieces or settings.black_no_pieces:
        if not settings.chess_move and not settings.game_end:                     #b\c if chess is moving it is removed from the chesses list
            settings.game_win = True
            settings.win_music_play = True
            settings.game_end = True

    #draw the main win or tie sign
    if settings.game_win or settings.game_lose:
        blit_win(settings,screen)
        #play music once
        if settings.win_music_play:
            settings.win_music_play = False
            settings.win_music.play()
    elif settings.game_tie:
        if settings.free_fall:
            free_fall(settings.tie_imageb_rect,settings)
        screen.blit(settings.tie_imageb,settings.tie_imageb_rect)
    #draw notice board
    if settings.board_appear:
        settings.board.draw_board()
    #draw moving chess
    if settings.chess_move:
        chess_on_mouse(settings)
    #draw mouse image
    if settings.mouse_enter:
        mouse_pos(settings,screen)

    pygame.display.update()

def mouse_pos(settings,screen):
    '''let the image be on the mouse position'''
    pos = pygame.mouse.get_pos()
    settings.mouse_image_rect.center = pos
    screen.blit(settings.mouse_image,settings.mouse_image_rect)

def check_pieces(chess,settings):
    '''feedback to settings.red/black no pieces'''
    if settings.red_no_pieces:
        if chess.text_color == settings.text_color_red and not chess.dead:
            if chess.rank >= 0:
                settings.red_no_pieces = False
    if settings.black_no_pieces:    
        if chess.text_color == settings.text_color_black and not chess.dead:
            if chess.rank >= 0:
                settings.black_no_pieces = False

def chess_on_mouse(settings):
    settings.chess_1.rect_out.center = settings.mouse_image_rect.center
    settings.chess_1.update_msg(settings.chess_1.msg)
    settings.chess_1.update_layer()
    settings.chess_1.draw_chess()

def win_center(screen,settings):
    '''putting the win image on the center of the screen'''
    screen_rect = screen.get_rect()
    win_image_rect = settings.win_image.get_rect()
    win_image_rect.center = screen_rect.center
    return win_image_rect

def blit_win(settings,screen):
    '''win image'''
    #increase alpha value
    n = settings.alpha_value
    if n <= 255:
        settings.alpha_value += 1
    settings.win_image.set_alpha(settings.alpha_value)

    win_rect = win_center(screen,settings)
    screen.blit(settings.win_image,win_rect)

def check_event(chesses,settings,dead_chesses,screen):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            chesses.clear()
            dead_chesses.clear()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                chesses.clear()
                dead_chesses.clear()
                sys.exit()
            if event.key == pygame.K_f:
                undo(settings,chesses,dead_chesses)
            if event.key == pygame.K_RETURN:
                switch_screen(settings)
            if event.key == pygame.K_r:
                if settings.game_end:
                    replay(settings,chesses,dead_chesses,screen)

        if event.type == pygame.MOUSEBUTTONDOWN and not settings.game_end:
            if event.button == 1 or event.button == 5:
                #the mouse image will not immediately change, but will wait 
                # until next screen update. but it does not matter, because the 
                # following judgements are quick
                settings.mouse_image = settings.fist_image
                pos = event.pos
                for chess in chesses:
                    if (chess.rect_out.collidepoint(pos) and
                                                    settings.game_active):
                        #undo is only allowed right after you move, and will be 
                        #invalid once you click on another chess
                        if not chess.dead:
                            settings.allow_undo = False

                        if not settings.second:
                            #show the identity of the chess
                            if chess.covered == True:
                                chess.msg = chess.identity
                                chess.chess_color_in=settings.chess_color_front
                                chess.update_msg(chess.msg)
                                chess.covered = False
                                break
                            
                            elif not chess.dead and chess.move:
                                #make a green mark on selected chess
                                a = settings.chess_color_selected
                                chess.chess_color_out = a
                                #a is just a tuple, not affiliated with the 
                                #chess. but settings.chess_1 has the same 
                                # qualities as chess. settings.chess_1 is in the
                                # sprites
                                settings.a = chess.rect_out.center
                                settings.chess1index = chesses.index(chess)
                                chesses.remove(chess)
                                settings.chess_1 = chess
                                settings.second = True
                                settings.chess_move = True
                                break

                        elif settings.second:
                            settings.second = False
                            settings.chess_2 = chess
                            det = determine(settings.chess_1,settings.chess_2,
                                settings,chesses,screen,dead_chesses)
                            if det:
                                chesses.insert(settings.chess1index,settings.chess_1)
                                move_chess(settings.chess_1,settings,
                                                    chesses,settings.chess_2)
                                
                                settings.chess_move = False
                                break
                            elif not det:
                                #let chess1 be where it used to be
                                color=settings.chess_color_back
                                chess = settings.chess_1
                                chess.chess_color_out=color
                                chess.rect_out.center = settings.a
                                chess.update_msg(chess.msg)
                                chess.update_layer()
                                chesses.insert(settings.chess1index,chess)
                                settings.chess_move = False
                                break

            if event.button == 3 and settings.chess_move:
                #let chess1 be where it used to be. cancel the move.
                color=settings.chess_color_back
                settings.chess_1.chess_color_out=color
                settings.chess_1.rect_out.center = settings.a
                settings.chess_1.update_msg(settings.chess_1.msg)
                settings.chess_1.update_layer()
                chesses.insert(settings.chess1index,settings.chess_1)
                settings.chess_move = False
                settings.second = False

            #check mouse click on tie flag or white flag
            if (settings.tie_flag_rect.collidepoint(event.pos) and 
                                                    not settings.chess_move):
                if settings.game_allow_end and settings.game_active:
                    settings.board = subboard.TieBoard(settings,screen)
                    settings.board_appear = True
                    settings.game_active = False

            if (settings.wh_flag_rect.collidepoint(event.pos) and 
                                                not settings.chess_move):
                if settings.game_allow_end and settings.game_active:
                    settings.game_lose = True
                    settings.win_music_play = True
                    settings.game_end = True
                elif settings.game_active:
                    settings.board = subboard.LoseBoard(settings,screen)
                    settings.board_appear = True
                    settings.game_active = False
            
            if settings.board_appear:
                if settings.board.yes_rect.collidepoint(event.pos):     #yes_rect
                    settings.board.action()
                    settings.board_appear = False
                    settings.game_active = True
                elif settings.board.no_rect.collidepoint(event.pos):   #no_rect
                    settings.board_appear = False
                    settings.game_active = True

        if event.type == pygame.MOUSEBUTTONUP and not settings.chess_move:
            settings.mouse_image = settings.palm_image

        if event.type == pygame.ACTIVEEVENT:
            if event.gain == 1:
                settings.mouse_enter = True
            else:
                settings.mouse_enter = False

        if event.type == pygame.MOUSEMOTION:
            #detect if mouse moves over those flags
            if settings.detec_rect.collidepoint(event.pos):
                settings.detec_active = True
            else:
                settings.detec_active = False

            if settings.tie_imaget_rect.collidepoint(event.pos):
                settings.tie_flag = settings.tie_image
            else:
                settings.tie_flag = settings.tie_imaget
            
            if settings.wh_image_rect.collidepoint(event.pos):
                settings.wh_flag = settings.wh_image
            else:
                settings.wh_flag = settings.wht_image

            if settings.board_appear:
                if settings.board.yes_rect.collidepoint(event.pos):
                    settings.board.touched_yes()
                else:
                    settings.board.normal_yes()
                if settings.board.no_rect.collidepoint(event.pos):
                    settings.board.touched_no()
                else:
                    settings.board.normal_no()

def highlight_chess(chess,settings):
    '''highlight chess when uncover the chess'''
    '''currently not used'''
    chess.chess_color_in = settings.chess_color_selected
    chess.update_msg(chess.msg)
    chess.draw_chess()
    pygame.display.update()
    time.sleep(0.1)
    chess.chess_color_in = settings.chess_color_front
    chess.update_msg(chess.msg)
    chess.draw_chess()
    pygame.display.update()
    time.sleep(0.1)
    chess.chess_color_in = settings.chess_color_selected
    chess.update_msg(chess.msg)
    chess.draw_chess()
    pygame.display.update()
    time.sleep(0.1)
    chess.chess_color_in = settings.chess_color_front
    chess.update_msg(chess.msg)

def create_chess(settings,chesses,screen,a,b,chess):
    chess.rect_out.center = (a,b)
    chess.update_msg(chess.msg)
    chess.update_layer()
    chesses.append(chess)

def update_dead(screen,settings,dead_chesses):
    chess = Chess(screen,settings)
    group = settings.dead_pool[-1]
    msg,color = group
    chess.rect_out = pygame.Rect(0,0,settings.chess_height_out,
                                            settings.chess_width_out)
    #split rows to display dead chesses
    l = len(settings.dead_pool)
    if l <= 12:
        a = settings.dead_pos_x
        settings.dead_pos_y = -settings.chess_width_out/2
        settings.dead_pos_y += (settings.chess_width_out+5)*l
        b = settings.dead_pos_y
    elif l <= 24:
        a = settings.dead_pos_x + settings.chess_height_out
        settings.dead_pos_y = -settings.chess_width_out/2
        settings.dead_pos_y += (settings.chess_width_out+5)*(l-12)
        b = settings.dead_pos_y
    elif l <= 37:
        a = settings.dead_pos_x + settings.chess_height_out*2
        a += settings.bg_image_width
        settings.dead_pos_y = -settings.chess_width_out/2
        settings.dead_pos_y += (settings.chess_width_out+5)*(l-24)
        b = settings.dead_pos_y
    else:
        a = settings.dead_pos_x + settings.chess_height_out*3
        a += settings.bg_image_width
        settings.dead_pos_y = -settings.chess_width_out/2
        settings.dead_pos_y += (settings.chess_width_out+5)*(l-37)
        b = settings.dead_pos_y

    chess.rect_out.center = (a,b)
    chess.text_color = color
    chess.chess_color_in = settings.chess_color_front
    chess.move = False
    chess.covered = False
    chess.angle = 0
    chess.update_msg(msg)
    dead_chesses.append(chess)

def create_whole_chess(settings,chesses,screen):
    a = settings.line_1_pos_x
    b = settings.line_1_pos_y
    for n in range(5):
        if n == 1 or n == 3:
            for i in range(12):
                chess = Chess(screen,settings)
                if i == 0:
                    create_chess(settings,chesses,screen,a,b,chess)
                    distribute_id(settings,chess)
                    distribute_pos(settings,chess)
                elif i == 1 or i == 11:
                    a += settings.line_spac_spec_1
                    create_chess(settings,chesses,screen,a,b,chess)
                    distribute_id(settings,chess)
                    distribute_pos(settings,chess)
                elif i == 6:
                    a += settings.line_spac_spec_2
                    create_chess(settings,chesses,screen,a,b,chess)
                    distribute_id(settings,chess)
                    distribute_pos(settings,chess)
                else:
                    a += settings.line_norm_spac
                    create_chess(settings,chesses,screen,a,b,chess)
                    if i == 2 or i == 4:
                        chess.dead = True
                        chess.covered = False
                        distribute_pos(settings,chess)
                    elif i == 7 or i == 9:
                        chess.dead = True
                        chess.covered = False
                        distribute_pos(settings,chess)
                    else:
                        distribute_id(settings,chess)
                        distribute_pos(settings,chess)

            a = settings.line_1_pos_x
            b += settings.row_spac   

        elif n == 2:
            for i in range(12):
                chess = Chess(screen,settings)
                if i == 0:
                    create_chess(settings,chesses,screen,a,b,chess)
                    distribute_id(settings,chess)
                    distribute_pos(settings,chess)
                elif i == 1 or i == 11:
                    a += settings.line_spac_spec_1
                    create_chess(settings,chesses,screen,a,b,chess)
                    distribute_id(settings,chess)
                    distribute_pos(settings,chess)
                elif i == 6:
                    a += settings.line_spac_spec_2
                    create_chess(settings,chesses,screen,a,b,chess)
                    distribute_id(settings,chess)
                    distribute_pos(settings,chess)
                else:
                    a += settings.line_norm_spac
                    create_chess(settings,chesses,screen,a,b,chess)
                    if i == 3 or i == 8:
                        chess.dead = True
                        chess.covered = False
                        distribute_pos(settings,chess)
                    else:
                        distribute_id(settings,chess)
                        distribute_pos(settings,chess)

            a = settings.line_1_pos_x
            b += settings.row_spac

        else:
            for i in range(12):
                chess = Chess(screen,settings)
                if i == 0:
                    create_chess(settings,chesses,screen,a,b,chess)
                    distribute_id(settings,chess)
                    distribute_pos(settings,chess)
                elif i == 1 or i == 11:
                    a += settings.line_spac_spec_1
                    create_chess(settings,chesses,screen,a,b,chess)
                    distribute_id(settings,chess)
                    distribute_pos(settings,chess)
                elif i == 6:
                    a += settings.line_spac_spec_2
                    create_chess(settings,chesses,screen,a,b,chess)
                    distribute_id(settings,chess)
                    distribute_pos(settings,chess)
                else:
                    a += settings.line_norm_spac
                    create_chess(settings,chesses,screen,a,b,chess)
                    distribute_id(settings,chess)
                    distribute_pos(settings,chess)

            a = settings.line_1_pos_x
            b += settings.row_spac                

def move_chess(chess,settings,chesses,chess_2):
    '''exchange the position of the two chess_spaces'''

    #exchange pos number first and the index in the list
    chess.pos,chess_2.pos = chess_2.pos,chess.pos
    a = chesses.index(chess)
    b = chesses.index(chess_2)
    chesses[a],chesses[b] = chesses[b],chesses[a]
    settings.chesses = chesses[:]

    b = chess_2.rect_out.center
    chess.rect_out.center = b
    #using settings a because a stores the original coordinates of chess_1
    chess_2.rect_out.center = settings.a

    color = settings.chess_color_back
    chess.chess_color_out = color
    chess.update_msg(chess.msg)
    chess.update_layer()
    chess_2.update_msg(chess_2.msg)
    chess_2.update_layer()
    selecting = False
    return selecting

def distribute_id(settings,chess):
    '''assign some qualities to a chess
    for later draw chess, battle, etc. use'''
    l = settings.chess_pool
    a = len(l)
    if a > 0:
        num = random.randint(0,a-1)
        b = l[num]
        x,y,z = b
        chess.identity = x
        chess.rank = y
        chess.text_color = z
        del settings.chess_pool[num]
        if z == settings.text_color_red:
            chess.color_control = 1
        elif z == settings.text_color_black:
            chess.color_control = -1

        if y < 0:
            chess.move = False

def distribute_pos(settings,chess):
    chess.pos = settings.pos_num
    settings.pos_num += 1

def determine(chess,chess_2,settings,chesses,screen,dead_chesses):
    '''determine what to do with the selected two chesses'''
    det_1 = determine_move_pos(chess,chess_2,settings.chesses)
    det_2 = determine_camp(chess_2)
    if det_1 != True or det_2 != True:
        return False

    if chess_2.dead:
        return True

    elif chess_2.covered:
        return False
    
    elif chess.text_color != chess_2.text_color:

        if chess.rank != 1 and chess_2.rank == -2 and settings.game_allow_end:
            if chess.text_color == settings.text_color_red:
                if settings.black_mine == 0:
                    indicator = True
                    for chess_x in chesses.sprites():
                        if not chess_x.dead:
                            if chess.text_color == chess_x.text_color:
                                if 0<chess_x.rank and chess_x.rank<chess.rank:
                                    indicator = False
                                    break
                    if indicator:
                        chess_2.dead = True
                        add_dead(chess_2,settings)
                        update_dead(screen,settings,dead_chesses)
                        settings.game_win = True
                        settings.win_music_play = True
                        settings.game_end = True
                        return True
            elif chess.text_color == settings.text_color_black:
                if settings.red_mine == 0:
                    indicator = True
                    for chess_x in chesses.sprites():
                        if not chess_x.dead:
                            if chess.text_color == chess_x.text_color:
                                if 0<chess_x.rank and chess_x.rank<chess.rank:
                                    indicator = False
                                    break
                    if indicator:
                        chess_2.dead = True
                        add_dead(chess_2,settings)
                        update_dead(screen,settings,dead_chesses)
                        settings.game_win = True
                        settings.win_music_play = True
                        settings.game_end = True
                        return True
        
        elif chess.rank == 1 and chess_2.rank == -2 and settings.game_allow_end:
            if chess.text_color == settings.text_color_red:
                if settings.black_mine == 0:
                    chess_2.dead = True
                    add_dead(chess_2,settings)
                    update_dead(screen,settings,dead_chesses)
                    settings.game_win = True
                    settings.win_music_play = True
                    settings.game_end = True
                    return True
            elif chess.text_color == settings.text_color_black:
                if settings.red_mine == 0:
                    chess_2.dead = True
                    add_dead(chess_2,settings)
                    update_dead(screen,settings,dead_chesses)
                    settings.game_win = True
                    settings.win_music_play = True
                    settings.game_end = True
                    return True
        
        elif chess.rank == 1 and chess_2.rank == -1:
            if chess.text_color == settings.text_color_red:
                chess_2.dead = True
                settings.black_mine -= 1
                dead_num = 1
                add_dead(chess_2,settings,dead_num)
                update_dead(screen,settings,dead_chesses)
                settings.allow_undo = True
                return True
            elif chess.text_color == settings.text_color_black:
                chess_2.dead = True
                settings.red_mine -= 1
                dead_num = 1
                add_dead(chess_2,settings,dead_num)
                update_dead(screen,settings,dead_chesses)
                settings.allow_undo = True
                return True
        
        elif chess.rank == 0 and chess_2.rank != -2:
            chess.dead = True
            chess_2.dead = True
            dead_num = 2
            add_dead(chess,settings,dead_num)
            update_dead(screen,settings,dead_chesses)
            add_dead(chess_2,settings,dead_num)
            update_dead(screen,settings,dead_chesses)
            settings.allow_undo = True
            if chess_2.rank == -1:
                if chess.text_color == settings.text_color_red:
                    settings.black_mine -= 1
                elif chess.text_color == settings.text_color_black:
                    settings.red_mine -= 1
            return True
        
        elif chess_2.rank == 0:
            chess.dead = True
            chess_2.dead = True
            dead_num = 2
            add_dead(chess,settings,dead_num)
            update_dead(screen,settings,dead_chesses)
            add_dead(chess_2,settings,dead_num)
            update_dead(screen,settings,dead_chesses)
            settings.allow_undo = True
            return True

        elif chess.rank == chess_2.rank and chess.rank >= 0:
            chess.dead = True
            chess_2.dead = True
            dead_num = 2
            add_dead(chess,settings,dead_num)
            update_dead(screen,settings,dead_chesses)
            add_dead(chess_2,settings,dead_num)
            update_dead(screen,settings,dead_chesses)
            settings.allow_undo = True
            return True
        
        elif chess.rank > chess_2.rank and chess_2.rank > 0:
            chess_2.dead = True
            dead_num = 1
            add_dead(chess_2,settings,dead_num)
            update_dead(screen,settings,dead_chesses)
            settings.allow_undo = True
            return True

    #if the move is illegal, cancel the green mark 
    return False

def add_dead(chess,settings,dead_num=0):
    a = (chess.identity,chess.text_color)
    settings.dead_pool.append(a)
    settings.dead_num = dead_num

def undo(settings,chesses,dead_chesses):
    '''saving the qualities of two chesses in settings, if need to undo,
    exchange back their qualities. the two chesses in settings are in chesses
    sprites!!!    Note: if change sth in the move_chess function, you probably
    need to change it in the undo function!''' 
    if settings.allow_undo:
        settings.allow_undo = False

        chess_1 = settings.chess_1
        chess_2 = settings.chess_2

    #whether the chess is mine
        if (settings.chess_2.text_color == settings.text_color_red and 
            settings.chess_2.rank == -1):
            settings.red_mine += 1
        elif (settings.chess_2.text_color == settings.text_color_black and 
            settings.chess_2.rank == -1):
            settings.black_mine += 1

    #exchange their position number and list index back first
        chess_1.pos,chess_2.pos = chess_2.pos,chess_1.pos
        a = chesses.index(chess_1)
        b = chesses.index(chess_2)
        chesses[a],chesses[b] = chesses[b],chesses[a]

        a = chess_1.rect_out.center
        b = chess_2.rect_out.center
        chess_1.rect_out.center = b
        chess_2.rect_out.center = a

        chess_1.update_msg(chess_1.msg)
        chess_1.update_layer()
        chess_2.update_msg(chess_2.msg)
        chess_2.update_layer()

        chess_1.dead = False
        chess_2.dead = False

    #have the settings.chesses updated
        settings.chesses = chesses[:]

        if settings.dead_num == 1:
            del settings.dead_pool[-1]
            del dead_chesses[-1]
        elif settings.dead_num == 2:
            del settings.dead_pool[-1]
            del settings.dead_pool[-1]
            del dead_chesses[-1]
            del dead_chesses[-1]

def switch_screen(settings):
    '''let the displat switch between fullscreen and resizable'''
    if settings.full:
        pygame.display.set_mode(
            (settings.screen_width,settings.screen_height),pygame.RESIZABLE)
        settings.full = False
    else:
        pygame.display.set_mode(
            (settings.screen_width,settings.screen_height),pygame.FULLSCREEN)
        settings.full = True

def free_fall(rect,settings):
    a = 0.1
    if settings.y > settings.screen_rect.centery:
        settings.down = False
        settings.up = True
        settings.time_count = 0
    if settings.v < 0:
        settings.up = False
        settings.down = True
        settings.time_count = 0
    if settings.down:
        t = settings.time_count+1
        settings.y = 0.5*a*t**2 + settings.x_0
        rect.centery = settings.y
        settings.time_count = t
        settings.v = a*t
        settings.v_0 = 0.6*settings.v
    elif settings.up:
        t = settings.time_count+1
        #using y because y can be a float
        settings.y=settings.screen_rect.centery-(settings.v_0*t-0.5*a*t**2)
        settings.time_count = t
        settings.v = settings.v_0 - a*t
        rect.centery = settings.y
        settings.x_0 = settings.y
        
    if abs(settings.x_0-settings.screen_rect.centery) < a:
        settings.free_fall = False
    
def replay(settings,chesses,dead_chesses,screen):
    settings.init_set()
    chesses.clear()
    dead_chesses.clear()
    create_whole_chess(settings,chesses,screen)
    settings.chesses = chesses[:]

def determine_camp(chess_2):
    if chess_2.pos in [14,16,19,21,27,32,38,40,43,45]:
        if chess_2.dead:
            return True
        return False
    return True

def determine_move_pos(chess,chess_2,chesses):
    if chess.pos in [0,11,12,23,24,35,36,47,48,59]:
        if chess_2.pos in [chess.pos+1,chess.pos-1,chess.pos+12,chess.pos-12]:
            return True
        return False
    if chess.pos in [14,16,19,21,27,32,38,40,43,45]:
        a = chess.pos
        if chess_2.pos in [a-13,a-12,a-11,a-1,a+1,a+11,a+12,a+13]:
            return True
        return False
    if chess.pos in [15,20,26,28,31,33,39,44]:
        a = chess.pos
        if chess_2.pos in [a-12,a-1,a+1,a+12]:
            return True
        return False
    if chess.pos in [2,4,7,9]:
        if chess_2.pos in list(range(1,11)):
            n = min(chess.pos,chess_2.pos)+1
            m = max(chess.pos,chess_2.pos)
            while n < m:
                if not chesses[n].dead:
                    return False
                n += 1
            return True
        if chess_2.pos == chess.pos+12:
            return True
        return False
    if chess.pos in [50,52,55,57]:
        if chess_2.pos in list(range(49,59)):
            n = min(chess.pos,chess_2.pos)+1
            m = max(chess.pos,chess_2.pos)
            while n < m:
                if not chesses[n].dead:
                    return False
                n += 1
            return True
        if chess_2.pos == chess.pos-12:
            return True
        return False
    if chess.pos in [3,8]:
        if chess_2.pos in list(range(1,11)):
            n = min(chess.pos,chess_2.pos)+1
            m = max(chess.pos,chess_2.pos)
            while n < m:
                if not chesses[n].dead:
                    return False
                n += 1
            return True
        if chess_2.pos in [chess.pos+11,chess.pos+12,chess.pos+13]:
            return True
        return False          
    if chess.pos in [51,56]:
        if chess_2.pos in list(range(49,59)):
            n = min(chess.pos,chess_2.pos)+1
            m = max(chess.pos,chess_2.pos)
            while n < m:
                if not chesses[n].dead:
                    return False
                n += 1
            return True
        if chess_2.pos in [chess.pos-11,chess.pos-12,chess.pos-13]:
            return True
        return False  
    if chess.pos in [1,5,6,10]:
        if chess_2.pos in list(range(1,11)):
            n = min(chess.pos,chess_2.pos)+1
            m = max(chess.pos,chess_2.pos)
            while n < m:
                if not chesses[n].dead:
                    return False
                n += 1
            return True
        if chess.pos == 1:
            if chess_2.pos in [13,25,37,49]:
                n = 13
                while n < chess_2.pos:
                    if not chesses[n].dead:
                        return False
                    n += 12
                return True
            if chess_2.pos == 14:
                return True
            if chess_2.pos == 0:
                return True
            return False
        if chess.pos == 5:
            if chess_2.pos in [17,29,41,53]:
                n = 17
                while n < chess_2.pos:
                    if not chesses[n].dead:
                        return False
                    n += 12
                return True
            if chess_2.pos == 16:
                return True
        if chess.pos == 6:
            if chess_2.pos in [18,30,42,54]:
                n = 18
                while n < chess_2.pos:
                    if not chesses[n].dead:
                        return False
                    n += 12
                return True
            if chess_2.pos == 19:
                return True
        if chess.pos == 10:
            if chess_2.pos in [22,34,46,58]:
                n = 22
                while n < chess_2.pos:
                    if not chesses[n].dead:
                        return False
                    n += 12
                return True
            if chess_2.pos == 21:
                return True
            if chess_2.pos == 11:
                return True
            return False
    if chess.pos in [49,53,54,58]:
        if chess_2.pos in list(range(49,59)):
            n = min(chess.pos,chess_2.pos)+1
            m = max(chess.pos,chess_2.pos)
            while n < m:
                if not chesses[n].dead:
                    return False
                n += 1
            return True
        if chess.pos == 49:
            if chess_2.pos in [1,13,25,37]:
                n = chess_2.pos + 12
                while n < chess.pos:
                    if not chesses[n].dead:
                        return False
                    n += 12
                return True
            if chess_2.pos == 38:
                return True
            if chess_2.pos == 48:
                return True
            return False
        if chess.pos == 53:
            if chess_2.pos in [5,17,29,41]:
                n = chess_2.pos +12
                while n < chess.pos:
                    if not chesses[n].dead:
                        return False
                    n += 12
                return True
            if chess_2.pos == 40:
                return True
        if chess.pos == 54:
            if chess_2.pos in [6,18,30,42]:
                n = chess_2.pos +12
                while n < chess.pos:
                    if not chesses[n].dead:
                        return False
                    n += 12
                return True
            if chess_2.pos == 43:
               return True
        if chess.pos == 58:
            if chess_2.pos in [10,22,34,46]:
                n = chess_2.pos + 12
                while n < chess.pos:
                    if not chesses[n].dead:
                        return False
                    n += 12
                return True
            if chess_2.pos == 45:
                return True
            if chess_2.pos == 59:
                return True
            return False
    if chess.pos in [13,25,37]:
        if chess_2.pos in [1,13,25,37,49]:
            n = min(chess.pos,chess_2.pos)+12
            m = max(chess.pos,chess_2.pos)
            while n < m:
                if not chesses[n].dead:
                    return False
                n += 12
            return True
        if chess.pos == 25:
            if chess_2.pos in [14,24,26,38]:
                return True
        elif chess_2.pos in [chess.pos-1,chess.pos+1]:
            return True
        return False
    if chess.pos in [17,29,41]:
        if chess_2.pos in [5,17,29,41,53]:
            n = min(chess.pos,chess_2.pos)+12
            m = max(chess.pos,chess_2.pos)
            while n < m:
                if not chesses[n].dead:
                    return False
                n += 12
            return True
        if chess.pos == 29:
            if chess_2.pos in [16,28,30,40]:
                return True
        elif chess_2.pos == chess.pos-1:
            return True
        return False
    if chess.pos in [18,30,42]:
        if chess_2.pos in [6,18,30,42,54]:
            n = min(chess.pos,chess_2.pos)+12
            m = max(chess.pos,chess_2.pos)
            while n < m:
                if not chesses[n].dead:
                    return False
                n += 12
            return True
        if chess.pos == 30:
            if chess_2.pos in [19,29,31,43]:
                return True
        elif chess_2.pos == chess.pos+1:
            return True
        return False
    if chess.pos in [22,34,46]:
        if chess_2.pos in [10,22,34,46,58]:
            n = min(chess.pos,chess_2.pos)+12
            m = max(chess.pos,chess_2.pos)
            while n < m:
                if not chesses[n].dead:
                    return False
                n += 12
            return True
        if chess.pos == 34:
            if chess_2.pos in [21,33,35,45]:
                return True
        elif chess_2.pos in [chess.pos-1,chess.pos+1]:
            return True
        return False

def test(settings,screen):
    '''this test proves that the chess distribution process is fair!'''
    n = 0
    m = 0
    while n<=10000:
        chesses = []
        settings.init_set()
        create_whole_chess(settings,chesses,screen)
        for chess in chesses:
            if chess.identity=='军长' and chess.text_color==settings.text_color_black:
                if chess.pos == 51:
                    m += 1
        n += 1
    print(m)



