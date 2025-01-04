import sys
import random
import time
from datetime import datetime
from csv import writer
import threading
import pygame
from chess import Chess
from board import Board
import subboard
from button import Button
#the display size cannot resizable!

def wrapup(settings,dead_chesses):
    '''used to get data of steps moved, moving time and units destroyed'''
    #steps
    #first get the first move player's data
    n = 0
    while n <= len(settings.move_cache)-1:
        settings.p1_movtime += float(settings.move_cache[n][3])
        settings.p1_steps += 1
        n += 2
    settings.p1_movtime = round(settings.p1_movtime,2)
    n = 1
    while n <= len(settings.move_cache)-1:
        settings.p2_movtime += float(settings.move_cache[n][3])
        settings.p2_steps += 1
        n += 2
    settings.p2_movtime = round(settings.p2_movtime,2)
    if settings.first_move == settings.player_2:
        settings.p1_movtime, settings.p2_movtime = settings.p2_movtime, settings.p1_movtime
        settings.p1_steps, settings.p2_steps = settings.p2_steps, settings.p1_steps

    #units destroyed
    for chess in dead_chesses:
        if chess.text_color == settings.text_color_red:
            settings.p1_units_destroyed += 1
        elif chess.text_color == settings.text_color_black:
            settings.p2_units_destroyed += 1
    if settings.player_1_color == 'red':
        settings.p1_units_destroyed,settings.p2_units_destroyed=settings.p2_units_destroyed,settings.p1_units_destroyed

def writedown(settings):
    '''write all the game data into the csv file'''
    list_of_item = [settings.player_1,settings.player_2,settings.first_move,
        settings.steps_before_c_confirmed,settings.player_1_color,settings.total_time_lasted,
        settings.total_steps_moved,settings.p1_steps,settings.p1_movtime,settings.p2_steps,
        settings.p2_movtime,settings.p1_units_destroyed,settings.p2_units_destroyed,settings.winner]
    filename = r'all_games.csv'
    try:
        with open(filename,'a+',newline='') as f:
            csv_writer = writer(f)
            csv_writer.writerow(list_of_item)
    except FileNotFoundError:
        filename = r'C:\Users\AAAAA\Desktop\python_work\battle_chess\all_games.csv'
        with open(filename,'a+',newline='') as f:
            csv_writer = writer(f)
            csv_writer.writerow(list_of_item)

def update_screen(settings,screen,chesses,dead_chesses,play_button):
    '''draw order: red_bg -> bg_image -> corner_flag -> chess -> dead_chess -> 
    win/tie_sign -> statistics_board -> play_button -> notice_board -> 
    moving_chess -> mouse'''
    screen.fill(settings.bg_color)
    #draw play order (red bg)
    draw_play_order(settings,screen)
    #draw bg image
    screen.blit(settings.bg_image,settings.bg_image_rect)
    #draw tie and white flag on corner
    if settings.detec_active:
        screen.blit(settings.tie_flag,settings.tie_flag_rect)
        screen.blit(settings.wh_flag,settings.wh_flag_rect)
    
    #game allow end controls whether chess has been uncovered
    if settings.game_rewind:
        settings.game_allow_end = True
        settings.red_no_pieces = False
        settings.black_no_pieces = False
    else:
        settings.game_allow_end = True
        settings.red_no_pieces = True
        settings.black_no_pieces = True
    #draw chess (when drawing chess, check if game allow end)
    for chess in chesses:
        if not chess.dead:
            chess.draw_chess()
        if chess.covered:
            settings.game_allow_end = False
        if not settings.game_rewind:
            check_pieces(chess,settings)
    
    #draw dead chess
    for chess in dead_chesses:
        chess.screen.fill(chess.chess_color_out,chess.rect_out)
        chess.screen.blit(chess.msg_image,chess.msg_image_rect)    
    #game tie
    if settings.red_no_pieces and settings.black_no_pieces:
        settings.game_result = 'tie'
        settings.game_end = True
    #game win
    elif settings.red_no_pieces or settings.black_no_pieces:
        if not settings.chess_move and not settings.game_end:                     #b\c if chess is moving it is removed from the chesses list
            settings.game_result = 'win'
            if settings.red_no_pieces:      #write down winner in settings.winner
                if settings.player_1_color == 'black':
                    settings.winner = settings.player_1
                else:
                    settings.winner = settings.player_2
            if settings.black_no_pieces:
                if settings.player_1_color == 'red':
                    settings.winner = settings.player_1
                else:
                    settings.winner = settings.player_2
            settings.win_music_play = True
            settings.game_end = True

    #draw the main win or tie sign
    if settings.game_result == 'win':
        if settings.winner == None:    ##currently only when 1.one side has no pieces or 2.军旗 has been taken out will the winner be declared
            settings.winner = '--'
        if settings.calculating:
            settings.end_time = datetime.now().replace(microsecond=0)
            settings.draw_stat = game_record(settings,screen)
            #first calculate total time, then wrapup all the data and write to csv file
            wrapup(settings,dead_chesses)
            writedown(settings)
            print(settings.player_1,settings.player_2,settings.first_move,settings.steps_before_c_confirmed,
            settings.player_1_color,settings.total_time_lasted,settings.total_steps_moved,
            settings.p1_steps,settings.p1_movtime,settings.p2_steps,settings.p2_movtime,
            settings.p1_units_destroyed,settings.p2_units_destroyed,settings.winner)
        blit_win(settings,screen)
        #play music once
        if settings.win_music_play:
            settings.win_music_play = False
            settings.win_music.play()
        #draw msg - the msg is directly rendered on bg
        screen.blit(settings.draw_stat[0],settings.draw_stat[1])
        screen.blit(settings.draw_stat[2],settings.draw_stat[3])

    elif settings.game_result == 'tie':
        #a summary of winner = '--'
        settings.winner = '--'
        if settings.calculating:
            settings.end_time = datetime.now().replace(microsecond=0)
            settings.draw_stat = game_record(settings,screen)
            wrapup(settings,dead_chesses)
            writedown(settings)
            print(settings.player_1,settings.player_2,settings.first_move,settings.steps_before_c_confirmed,
            settings.player_1_color,settings.total_time_lasted,settings.total_steps_moved,
            settings.p1_steps,settings.p1_movtime,settings.p2_steps,settings.p2_movtime,
            settings.p1_units_destroyed,settings.p2_units_destroyed,settings.winner)
        if settings.free_fall:
            free_fall(settings.tie_imageb_rect,settings)
        screen.blit(settings.tie_imageb,settings.tie_imageb_rect)
        #draw msg - the msg is directly rendered on bg
        screen.blit(settings.draw_stat[0],settings.draw_stat[1])
        screen.blit(settings.draw_stat[2],settings.draw_stat[3])
    #draw play button
    if settings.play_button_on:
        settings.play_button.draw_button()
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

def randomize_play_order(settings,screen):
    settings.red_bg = True
    n = random.randint(0,1)
    if n == 0:
        settings.first_move = settings.player_1
        settings.half_red_bg.left = settings.screen_rect.left
        time.sleep(3)
    elif n == 1:
        settings.first_move = settings.player_2
        settings.half_red_bg.right = settings.screen_rect.right
        time.sleep(3)
    settings.red_bg = False

def draw_play_order(settings,screen):
    '''first randomize order, then draw it'''
    if settings.show_order:
        settings.show_order = False
        t = threading.Thread(target=randomize_play_order,args=(settings,screen))
        t.start()

    if settings.red_bg:
        pygame.draw.rect(screen,settings.color_red,settings.half_red_bg)

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

def color_confirm(chess,settings):
    '''used to determine if it has confirmed who's red and who's black'''
    if settings.count % 2 == 0:
        if settings.move_1 != chess.text_color:
            settings.color_confirmed = True
            settings.steps_before_c_confirmed = settings.count-1
            #interpret red or black
            #initiate move control
            if settings.move_1 == settings.text_color_red:
                if settings.first_move == settings.player_1:        #should pay attention to this red or black thing!
                    settings.player_1_color = 'red'
                else:
                    settings.player_1_color = 'black'
                settings.move_control = 1      #red -> 1
            elif settings.move_1 == settings.text_color_black:
                if settings.first_move == settings.player_1:
                    settings.player_1_color = 'black'
                else:
                    settings.player_1_color = 'red'
                settings.move_control = -1
    else:
        settings.move_1 = chess.text_color

def check_event(chesses,settings,dead_chesses,screen):
    '''storing all the funcs in case you'll need them in the future'''
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
                undo(settings,chesses,dead_chesses)     #check game active being put in undo function
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
                        if not settings.second:
                            #show the identity of the chess
                            if chess.covered == True:
                                chess.msg = chess.identity
                                chess.chess_color_in=settings.chess_color_front
                                chess.update_msg(chess.msg)
                                chess.covered = False
                                #save it to move cache
                                a=['uncover',chess,0]
                                settings.move_cache.append(a)
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
                            settings.dead_num = 0
                            det = determine(settings.chess_1,settings.chess_2,
                                settings,chesses,screen,dead_chesses)
                            if det:
                                chesses.insert(settings.chess1index,settings.chess_1)
                                move_chess(settings.chess_1,settings,
                                                    chesses,settings.chess_2)
                                a=[settings.chess_1,settings.chess_2,
                                                            settings.dead_num]
                                #if len(settings.move_cache) > 49:
                                #    settings.move_cache.pop(0)
                                settings.move_cache.append(a)
                                
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
                    settings.game_result = 'win'
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

            #push play button
            if settings.play_button != None:
                if settings.play_button.button_in.collidepoint(event.pos):
                    settings.play_button_on = False
                    settings.play_button = None
                    settings.show_order = True
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

            if settings.play_button_on:
                if settings.play_button.button_in.collidepoint(event.pos):
                    settings.play_button.touched_button('Play')
                else:
                    settings.play_button.normal_button('Play')

def check_event_gameend(chesses,settings,dead_chesses,screen,event):
    '''performing game_not_started functions'''
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            replay(settings,chesses,dead_chesses,screen)
            settings.start_time = datetime.now().replace(microsecond=0)
        if event.key == pygame.K_a and settings.game_result != None:  #only when it is literally game end, can game be rewinded
            rewind(settings)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1 or event.button == 5:
            #push play button
            if settings.play_button != None:
                if settings.play_button.button_in.collidepoint(event.pos):
                    settings.play_button_on = False
                    settings.play_button = None
                    settings.show_order = True
                    settings.game_end = False
                    settings.start_time = datetime.now().replace(microsecond=0)
                    settings.move_start = datetime.now()

    if event.type == pygame.MOUSEMOTION:
        if settings.play_button_on:
            if settings.play_button.button_in.collidepoint(event.pos):
                settings.play_button.touched_button('Play')
            else:
                settings.play_button.normal_button('Play')
                                    
def check_event_ingame(chesses,settings,dead_chesses,screen,event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_f:
            undo(settings,chesses,dead_chesses)     #check game active being put in undo function

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1 or event.button == 5:
            pos = event.pos
            for chess in chesses:
                if (chess.rect_out.collidepoint(pos) and
                                                settings.game_active):
                    if not settings.second:
                        #show the identity of the chess
                        if chess.covered == True:
                            #the former move ends here
                            settings.move_end = datetime.now()
                            #alter the move control, it will be other person's round
                            settings.move_control *= -1
                            if not settings.color_confirmed:
                                settings.count += 1
                                color_confirm(chess,settings)
                            chess.msg = chess.identity
                            chess.chess_color_in=settings.chess_color_front
                            chess.update_msg(chess.msg)
                            chess.covered = False
                            #save it to move cache
                            a=['uncover',chess,0,(settings.move_end-settings.move_start).total_seconds()]
                            settings.move_cache.append(a)
                            #the next move starts here
                            settings.move_start = datetime.now()
                            break
                        
                        elif not chess.dead and chess.move:
                            #first determine if it is the player's round
                            #delete two lines below to disable the function
                            if chess.move_control != settings.move_control:
                                print(chess.move_control,settings.move_control)
                                continue
                            else:
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
                        #the move ends here, but store the move_time only when it is legit aka if det
                        settings.move_end = datetime.now()
                        settings.second = False
                        settings.chess_2 = chess
                        settings.dead_num = 0
                        det = determine(settings.chess_1,settings.chess_2,
                            settings,chesses,screen,dead_chesses)
                        if det:
                            chesses.insert(settings.chess1index,settings.chess_1)
                            move_chess(settings.chess_1,settings,
                                                chesses,settings.chess_2)
                            #alter the move control, it will be other person's round
                            settings.move_control *= -1
                            a=[settings.chess_1,settings.chess_2,
                                settings.dead_num,(settings.move_end-settings.move_start).total_seconds()]
                            #if len(settings.move_cache) > 49:
                            #    settings.move_cache.pop(0)
                            settings.move_cache.append(a)
                            
                            settings.chess_move = False
                            #the next move starts here
                            settings.move_start = datetime.now()
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
            if settings.game_active:
                settings.board = subboard.TieBoard(settings,screen)
                settings.board_appear = True
                settings.game_active = False

        if (settings.wh_flag_rect.collidepoint(event.pos) and 
                                            not settings.chess_move):
            if settings.game_allow_end and settings.game_active:    #this game_active prevents already in a board appear status and you click the sign once more

                settings.game_result = 'win'
                settings.win_music_play = True
                settings.game_end = True
                settings.game_active = False
                settings.detec_active = False
            elif settings.game_active:
                settings.board = subboard.LoseBoard(settings,screen)
                settings.board_appear = True
                settings.game_active = False
        
        if settings.board_appear:
            if settings.board.yes_rect.collidepoint(event.pos):     #yes_rect
                settings.board.action()
                settings.board_appear = False
                settings.game_active = False
            elif settings.board.no_rect.collidepoint(event.pos):   #no_rect
                settings.board_appear = False
                settings.game_active = True

    if event.type == pygame.MOUSEMOTION:
        #detect if mouse moves over those flags
        if settings.detec_rect.collidepoint(event.pos):
            settings.detec_active = True        #pygame event get first captures mousemotion causing detec_active remain True after clicking it. the solution is set detec_active=false in clicking function.
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

        #detects if mouse move over the board
        if settings.board_appear:
            if settings.board.yes_rect.collidepoint(event.pos):
                settings.board.touched_yes()
            else:
                settings.board.normal_yes()
            if settings.board.no_rect.collidepoint(event.pos):
                settings.board.touched_no()
            else:
                settings.board.normal_no()

def check_event_display(chesses,settings,dead_chesses,screen,event):
    '''check events for display'''
    if event.type == pygame.QUIT:
        sys.exit()

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            sys.exit()
        if event.key == pygame.K_RETURN:
            switch_screen(settings)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1 or event.button == 5:
            #the mouse image will not immediately change, but will wait 
            #until next screen update. but it does not matter, because the 
            #following judgements are quick
            settings.mouse_image = settings.fist_image

    if event.type == pygame.MOUSEBUTTONUP and not settings.chess_move:
        settings.mouse_image = settings.palm_image

    if event.type == pygame.ACTIVEEVENT:
        if event.gain == 1:
            settings.mouse_enter = True
        else:
            settings.mouse_enter = False

def check_event_gamerewind(chesses,settings,dead_chesses,screen,event):
    '''funcs used during game rewind'''
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_f:
            undo(settings,chesses,dead_chesses)     #check game active being put in undo function
        if event.key == pygame.K_r:
            replay(settings,chesses,dead_chesses,screen)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1 or event.button == 5:
            pos = event.pos
            for chess in chesses:
                if (chess.rect_out.collidepoint(pos) and
                                                settings.game_active):
                    if not settings.second:
                        #show the identity of the chess
                        if chess.covered == True:
                            chess.msg = chess.identity
                            chess.chess_color_in=settings.chess_color_front
                            chess.update_msg(chess.msg)
                            chess.covered = False
                            #save it to move cache
                            a=['uncover',chess,0]
                            settings.move_cache.append(a)
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
                        settings.dead_num = 0
                        det = determine(settings.chess_1,settings.chess_2,
                            settings,chesses,screen,dead_chesses)
                        if det:
                            chesses.insert(settings.chess1index,settings.chess_1)
                            move_chess(settings.chess_1,settings,
                                                chesses,settings.chess_2)
                            a=[settings.chess_1,settings.chess_2,
                                                        settings.dead_num]
                            #if len(settings.move_cache) > 49:
                            #    settings.move_cache.pop(0)
                            settings.move_cache.append(a)
                            #the followings prevents triggering game win in rewind mode
                            settings.game_result = None
                            settings.win_music_play = False
                            settings.game_end = False

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
    '''moving the dead chess into right position on the screen'''
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
    '''exchange the position of the two chess_spaces, when editing this, you 
    probably need to change in undo function'''

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
    for later draw chess, battle, etc. in use'''
    l = settings.chess_pool
    a = len(l)
    if a > 0:
        num = random.randint(0,a-1)
        b = l[num]
        x,y,z = b
        chess.identity = x
        chess.rank = y
        chess.text_color = z
        if z == settings.text_color_red:
            chess.move_control = 1
        elif z == settings.text_color_black:
            chess.move_control = -1
        del settings.chess_pool[num]

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
                    for chess_x in chesses:
                        if not chess_x.dead:
                            if chess.text_color == chess_x.text_color:
                                if 0<chess_x.rank and chess_x.rank<chess.rank:
                                    indicator = False
                                    break
                    if indicator:
                        chess_2.dead = True
                        add_dead(chess_2,settings,dead_num=1)
                        update_dead(screen,settings,dead_chesses)
                        settings.game_result = 'win'
                        if settings.player_1_color == 'red':        #here the program will save the winner in settings
                            settings.winner = settings.player_1
                        else:
                            settings.winner = settings.player_2
                        settings.win_music_play = True
                        settings.game_end = True
                        return True
            elif chess.text_color == settings.text_color_black:
                if settings.red_mine == 0:
                    indicator = True
                    for chess_x in chesses:
                        if not chess_x.dead:
                            if chess.text_color == chess_x.text_color:
                                if 0<chess_x.rank and chess_x.rank<chess.rank:
                                    indicator = False
                                    break
                    if indicator:
                        chess_2.dead = True
                        add_dead(chess_2,settings,dead_num=1)
                        update_dead(screen,settings,dead_chesses)
                        settings.game_result = 'win'
                        if settings.player_1_color == 'black':
                            settings.winner = settings.player_1
                        else:
                            settings.winner = settings.player_2
                        settings.win_music_play = True
                        settings.game_end = True
                        return True
        
        elif chess.rank == 1 and chess_2.rank == -2 and settings.game_allow_end:
            if chess.text_color == settings.text_color_red:
                if settings.black_mine == 0:
                    chess_2.dead = True
                    add_dead(chess_2,settings,dead_num=1)
                    update_dead(screen,settings,dead_chesses)
                    settings.game_result = 'win'
                    if settings.player_1_color == 'red':
                        settings.winner = settings.player_1
                    else:
                        settings.winner = settings.player_2
                    settings.win_music_play = True
                    settings.game_end = True
                    return True
            elif chess.text_color == settings.text_color_black:
                if settings.red_mine == 0:
                    chess_2.dead = True
                    add_dead(chess_2,settings,dead_num=1)
                    update_dead(screen,settings,dead_chesses)
                    settings.game_result = 'win'
                    if settings.player_1_color == 'black':
                        settings.winner = settings.player_1
                    else:
                        settings.winner = settings.player_2
                    settings.win_music_play = True
                    settings.game_end = True
                    return True
        
        elif chess.rank == 1 and chess_2.rank == -1:
            if chess.text_color == settings.text_color_red:
                chess_2.dead = True
                settings.black_mine -= 1
                add_dead(chess_2,settings,dead_num=1)
                update_dead(screen,settings,dead_chesses)
                return True
            elif chess.text_color == settings.text_color_black:
                chess_2.dead = True
                settings.red_mine -= 1
                add_dead(chess_2,settings,dead_num=1)
                update_dead(screen,settings,dead_chesses)
                return True
        
        elif chess.rank == 0 and chess_2.rank != -2:
            chess.dead = True
            chess_2.dead = True
            add_dead(chess,settings,dead_num=2)
            update_dead(screen,settings,dead_chesses)
            add_dead(chess_2,settings,dead_num=2)
            update_dead(screen,settings,dead_chesses)
            if chess_2.rank == -1:
                if chess.text_color == settings.text_color_red:
                    settings.black_mine -= 1
                elif chess.text_color == settings.text_color_black:
                    settings.red_mine -= 1
            return True
        
        elif chess_2.rank == 0:
            chess.dead = True
            chess_2.dead = True
            add_dead(chess,settings,dead_num=2)
            update_dead(screen,settings,dead_chesses)
            add_dead(chess_2,settings,dead_num=2)
            update_dead(screen,settings,dead_chesses)
            return True

        elif chess.rank == chess_2.rank and chess.rank >= 0:
            chess.dead = True
            chess_2.dead = True
            add_dead(chess,settings,dead_num=2)
            update_dead(screen,settings,dead_chesses)
            add_dead(chess_2,settings,dead_num=2)
            update_dead(screen,settings,dead_chesses)
            return True
        
        elif chess.rank > chess_2.rank and chess_2.rank > 0:
            chess_2.dead = True
            add_dead(chess_2,settings,dead_num=1)
            update_dead(screen,settings,dead_chesses)
            return True

    #if the move is illegal, cancel the green mark 
    return False

def add_dead(chess,settings,dead_num=0):
    a = (chess.identity,chess.text_color)
    settings.dead_pool.append(a)
    settings.dead_num = dead_num

def undo(settings,chesses,dead_chesses):
    '''saving the qualities of one (or two) chesses in settings, if need to undo,
    exchange back their qualities. the two chesses in settings are in chesses
    sprites!!!    Note: if change sth in the move_chess function, you probably
    need to change it in the undo function!     also added to alter the move_control''' 
    if (not settings.game_end and settings.game_active 
                                        and not settings.chess_move):
        indicator = True
        uncover_ind = False
        try:
            chess_1,chess_2,dead_num,nothing = settings.move_cache[-1]      #nothing stands for the move_time, which is useless in this func
        except IndexError:
            indicator = False
        else:
            if chess_1 == 'uncover':
                uncover_ind = True
            #here alter the settings.move_control first
            settings.move_control *= -1
            settings.move_cache.pop()

        if uncover_ind:
            chess_2.covered = True
            chess_2.chess_color_in = settings.chess_color_back
            chess_2.msg = ''
            chess_2.update_msg(chess_2.msg)
            #have the settings.chesses updated
            settings.chesses = chesses[:]

        elif indicator:
            #whether the chess is mine
            if (chess_2.text_color == settings.text_color_red and 
                chess_2.rank == -1 and dead_num != 0):      #dead_num != 0 ensures only if 工兵eats 地雷,地雷 can be undo. if it is just moving one chess, then the already dead 地雷 should not count
                settings.red_mine += 1
            elif (chess_2.text_color == settings.text_color_black and 
                chess_2.rank == -1 and dead_num != 0):
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
            if dead_num == 0:
                chess_2.dead = True

            #have the settings.chesses updated
            settings.chesses = chesses[:]

            if dead_num == 1:
                del settings.dead_pool[-1]
                del dead_chesses[-1]
            elif dead_num == 2:
                del settings.dead_pool[-1]
                del settings.dead_pool[-1]
                del dead_chesses[-1]
                del dead_chesses[-1]

def switch_screen(settings):
    '''let the displat switch between (fullscreen) and resizable'''
    if settings.fullscreen:
        pygame.display.set_mode(
            (int(settings.screen_width/2),int(settings.screen_height/2)),pygame.RESIZABLE)
        settings.fullscreen = False
    else:
        pygame.display.set_mode(
            (settings.screen_width,settings.screen_height),pygame.FULLSCREEN)
        settings.fullscreen = True

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
    settings.play_button = Button(screen,settings,'Play')
    chesses.clear()
    dead_chesses.clear()
    create_whole_chess(settings,chesses,screen)
    settings.chesses = chesses[:]

def rewind(settings):
    settings.game_rewind = True
    settings.game_active = True
    settings.game_end = False
    settings.game_result = None

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

def calculate_duration(settings):
    '''interpret timedelta into a string containing day,hour,minute,second'''
    start = settings.start_time
    end = settings.end_time
    duration = end - start
    if duration.days == 0:
        message = ''
    elif duration.days == 1:
        message = '%s day ' % duration.days
    else:
        message = '%s days ' % duration.days
    if duration.seconds >= 3600:
        hour = duration.seconds // 3600
        if hour == 1:
            message += '%s hour ' % hour
        else:
            message += '%s hours ' % hour
        seconds = duration.seconds % 3600
        if seconds >= 60:
            minute = seconds // 60
            if minute == 1:
                message += '%s minute ' % minute
            else:
                message += '%s minutes ' % minute
            second = seconds % 60
            if second <= 1:
                message += '%s second' % second
            else:
                message += '%s seconds' % second
        else:
            if seconds <= 1:
                message += '%s second' % seconds
            else:
                message += '%s seconds' % seconds
    elif duration.seconds >= 60:
        minute = duration.seconds // 60
        if minute == 1:
            message += '%s minute ' % minute
        else:
            message += '%s minutes ' % minute
        second = duration.seconds % 60
        if second <= 1:
            message += '%s second' % second
        else:
            message += '%s seconds' % second
    else:
        if duration.seconds <= 1:
            message += '%s second' % duration.seconds
        else:
            message += '%s seconds' % duration.seconds
    settings.total_time_lasted = [message,str(duration.total_seconds())]
    return message, int(duration.total_seconds())

def game_record(settings,screen):
    '''check if moving steps are record high, also show it on the display
    also check if time duration is record high, show it on display'''
    #first determine if made record
    message_time, seconds = calculate_duration(settings)
    settings.total_steps_moved = len(settings.move_cache)
    record_step = False
    record_time = False
    filename=r'game_record.txt'
    try:
        with open(filename) as f:
            score = f.read()
            score = score.split()
    except FileNotFoundError:
        filename = r'C:\Users\AAAAA\Desktop\python_work\battle_chess\game_record.txt'
        with open(filename) as f:
            score = f.read()
            score = score.split()
    if int(score[0]) < len(settings.move_cache):
        record_step = True
        content = '%s %s' % (len(settings.move_cache),score[1])
    if int(score[1]) < seconds:
        record_time = True
        content = '%s %s' % (score[0],seconds)
    if record_step and record_time:
        content = '%s %s' % (len(settings.move_cache),seconds)
    #write record
    if record_time or record_step:
        filename=r'game_record.txt'
        try:
            with open(filename,'w') as f:
                f.write(content)
        except FileNotFoundError:
            filename = r'C:\Users\AAAAA\Desktop\python_work\battle_chess\game_record.txt'
            with open(filename,'w') as f:
                f.write(content)

    #prep step msg
    if record_step:
        msg='This round smashed past record with '+str(len(settings.move_cache))
        msg += ' steps moved!'
    else:
        msg = str(len(settings.move_cache))+' steps moved.'

    step_image = settings.board_font.render(msg,True,settings.notice_color,
                                                    settings.bg_color)
    step_image_rect = step_image.get_rect()
    step_image_rect.centerx = settings.screen_rect.centerx
    step_image_rect.bottom = settings.screen_rect.bottom

    #prep time msg
    if record_time:
        msg = 'The longest game of '+message_time+'!'
    else:
        msg = 'This round lasted '+message_time+'.'

    time_image = settings.board_font.render(msg,True,settings.notice_color,
                                                    settings.bg_color)
    time_image_rect = time_image.get_rect()
    time_image_rect.centerx = settings.screen_rect.centerx
    time_image_rect.bottom = step_image_rect.top

    settings.calculating = False

    return (step_image,step_image_rect,time_image,time_image_rect)