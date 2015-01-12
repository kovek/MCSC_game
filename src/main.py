import pygame, sys, os
from pygame.locals import *
from enum import Enum
import classes

# set up pygame and init

pygame.init()
is_online = False

# this bypasses the resolution selection and makes it 1080p by default, get rekt peasants
bypass = 1
# the engine resolution at which everything is rendered, all computations are done with respect to this resolution
window_size_h_ren = 3840.0
window_size_v_ren = 2160.0
aspect_ratio = (16,9)
# querying for display resolution (and aspect ratio) at which everything is drawn
if bypass == 0:
    print "Sup m8 this game runs only at 16:9 or 16:10 aspect ratios with a max resolution of 3840x2400, umad ppl stuck in 2005 (4:3) or fat basement nerds (21:9)? XD"
    while True:
        print "Gimme aspect ratio: 16,10 or 16,9:"
        # get input for aspect ratio, get new one if not (16,9) or (16,10) or a tuple
        while True:
            try:
                aspect_ratio = tuple(input())
            except:
                print "U 'avin a giggle m8? Gimme aspect ratio in (x,y) format"
            else:
                if aspect_ratio == (16,10) or aspect_ratio == (16,9):
                    break
                else:            
                    print "U 'avin a giggle m8? Gimme aspect ratio 16,10 or 16,9"
                    pass
        print "Gimme window horizontal size in pixels or enter 0 to skip:"
        # get input for horizontal size, get new one if above 3840 px or not an int
        while True:
            try:
                window_size_h_res = input()
            except:
                print "U 'avin a giggle m8? Gimme horizontal size as an int"
            else:
                if window_size_h_res <=3840:  
                    window_size_h_res = float(window_size_h_res)
                    break
                    
                else:
                    print "U 'avin a giggle m80? Gimme horizontal size at most 3840"
                    pass
        print "Gimme window vertical size in pixels or enter 0 to skip:"
        # get input for vertical size, get new one if below 900 px or not an int
        while True:
            try:
                window_size_v_res = input()
            except:
                print "U 'avin a giggle m8? Gimme vertical size as an int"
            else:
                if window_size_v_res <=2400:
                    window_size_v_res = float(window_size_v_res)
                    break
                else:
                    print "U 'avin a giggle m80? Gimme vertical size at most 2400"
                    pass
        if window_size_h_res == 0 and window_size_v_res == 0:
            print "U 'avin a giggle m8? Horizontal and vertical size of 0? Get rekt scrub"
        elif window_size_h_res == 0 and window_size_v_res != 0:
            window_size_h_res = float(aspect_ratio[0])/float(aspect_ratio[1]) * window_size_v_res
            break
        elif window_size_h_res != 0 and window_size_v_res == 0:
            window_size_v_res = float(aspect_ratio[1])/float(aspect_ratio[0]) * window_size_h_res
            break
        else:
            if window_size_h_res/window_size_v_res != float(aspect_ratio[0])/float(aspect_ratio[1]):
                print "U 'avin a giggle m8? Horizontal and vertical size not matching aspect ratio? Get rekt scrub"
            elif window_size_h_res/window_size_v_res == float(aspect_ratio[0])/float(aspect_ratio[1]):
                break
# or default parameters
elif bypass == 1:
    window_size_h_res = 1920.0
    window_size_v_res = 1080.0
    aspect_ratio = (16,9)

# offsets for gui items to remain at the same relative place regardless of screen size
offset_h = (window_size_h_res-1440)/2
offset_v = (window_size_v_res-900)

# set up the different surfaces needed for drawing, screen is where GUI is drawn (it is not scaled and thus drawn directly on screen, maybe an option for small/medium/large will be added sometime); screen_render is where everything is rendered, screen_draw is the finished frame
screen = pygame.display.set_mode((int(window_size_h_res), int(window_size_v_res)), 0, 32)
classes.screen = screen
classes.screen_render = pygame.Surface((int(window_size_h_ren), int(window_size_v_ren)))
screen_draw = pygame.Surface((int(window_size_h_res), int(window_size_v_res)))

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

classes.window_size_h_ren = window_size_h_ren
classes.window_size_v_ren = window_size_v_ren
classes.window_size_h_res = window_size_h_res
classes.window_size_v_res = window_size_v_res

# Values for the GUI
max_health_value = 750.0
max_mana_value = 500.0
max_enemy_hp_value = 15000.0
health_value = 750.0
mana_value = 500.0
enemy_hp_value = 15000.0
health_percentage = health_value/max_health_value
mana_percentage = mana_value/max_mana_value
enemy_hp_percentage = enemy_hp_value/max_enemy_hp_value

# initialization of every element of the game (player, enemies, gui items)
###this should be moved to some other class eventually
player = classes.Player(20,50)
square_position_x = [510+offset_h,580+offset_h,670+offset_h,740+offset_h,810+offset_h,880+offset_h]
hp_container = classes.GuiStatic('bar_container.png',20+offset_h,830+offset_v)
mana_container = classes.GuiStatic('bar_container.png',970+offset_h,830+offset_v)
enemy_bar_container = classes.GuiStatic('enemy_bar_container.png',470+offset_h,20)
hp_bar = classes.GuiDynamic('hp_bar.png', 22+offset_h, 832+offset_v, 446, health_percentage)
mana_bar = classes.GuiDynamic('mana_bar.png', 972+offset_h, 832+offset_v, 446, mana_percentage)
enemy_bar = classes.GuiDynamic('enemy_bar.png', 472+offset_h, 22, 496, enemy_hp_percentage)
square0 = classes.GuiStatic('square.png', square_position_x[0], 830+offset_v)
square1 = classes.GuiStatic('square.png', square_position_x[1], 830+offset_v)
square2 = classes.GuiStatic('square.png', square_position_x[2], 830+offset_v)
square3 = classes.GuiStatic('square.png', square_position_x[3], 830+offset_v)
square4 = classes.GuiStatic('square.png', square_position_x[4], 830+offset_v)
square5 = classes.GuiStatic('square.png', square_position_x[5], 830+offset_v)
hp_text = classes.GuiText('HP',20+offset_h,810+offset_v)
mana_text = classes.GuiText('MP', 970+offset_h, 810+offset_v)
lh_text = classes.GuiText('LH',510+offset_h,810+offset_v)
rh_text = classes.GuiText('RH',580+offset_h,810+offset_v)
s1_text = classes.GuiText('S1',670+offset_h,810+offset_v)
s2_text = classes.GuiText('S2',740+offset_h,810+offset_v)
s3_text = classes.GuiText('S3',810+offset_h,810+offset_v)
s4_text = classes.GuiText('S4',880+offset_h,810+offset_v)
boss = classes.Enemy(100,200)
sun = classes.Star()
player_shadow = classes.Shadow(player,'player',sun)
boss_shadow = classes.Shadow(boss,'boss',sun)

focus = player

# Use this to know what state the game is at
State = Enum('State', 'playing menu paused')
state = State.playing

# things_objects are things that need to be rendered, things_gui are just gui items, things_other are things that have ticks but are not drawn
things_objects = [player_shadow, player, boss_shadow, boss]
things_gui = [hp_container, mana_container, enemy_bar_container,square0,square1,square2,square3,square4,square5,hp_bar,mana_bar,enemy_bar,hp_text,mana_text,lh_text,rh_text,s1_text,s2_text,s3_text,s4_text]
things_other = [sun]
things_on_screen = things_gui+things_objects+things_other
classes.things_on_screen = things_on_screen

# run the game loop
while True:
    screen.fill(BLACK)
    classes.screen_render.fill(BLACK)
    if state == State.paused:
        pass
        # don't move anything
    else:
        # tick for everything that is not gui items
        for thing in things_objects:
            thing.tick()
        for thing in things_other:
            thing.tick()
        # converting render surface into drawn surface, for now, for 16:10 it's simply stretched vertically, change that eventually
        screen_draw = pygame.transform.smoothscale(classes.screen_render, (int(window_size_h_res), int(window_size_v_res)))
        screen.blit(screen_draw, (0,0))
        # tick for gui items, that are drawn last
        for thing in things_gui:
            thing.tick()
    
    # Handle events (keys)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                # Depending of what is going on, we will do different things.
                if state == State.playing:
                    # If not online, stop game.
                    if not is_online:
                        state = State.paused

                    classes.PauseMenu.show()

                    # put pause menu to focus.
                    focus = classes.PauseMenu

                    state = State.paused
                elif state == State.menu or state == State.paused:
                    # send the escape event to menu. It will 'go back' if it can. If not, then it will remove the pause menu.
                    if focus.escape_pressed() == "close_menu":
                        pass

        focus.key_event(event)
    pygame.display.update()

