import pygame, sys, os
from pygame.locals import *
from enum import Enum
import classes
from classes import animation_loop

# set up pygame
pygame.init()

window_size_h = 0
window_size_v = 0
print "Sup m8 this game runs only at resolutions above 1440x900, umad ppl stuck in 2010? XD"
# get input for horizontal size, get new one if below 1440 px
print "Gimme window horizontal size in pixels:"
window_size_h = input()
while window_size_h < 1440:
    print "U 'avin a giggle m8? Gimme horizontal size at least 1440"
    window_size_h = input()
# get input for vertical size, get new one if below 900 px
print "Gimme window vertical size in pixels:"
window_size_v = input()
while window_size_v < 900:
    print "U 'avin a giggle m8? Gimme vertical size at least 900"
    window_size_v = input()
# offsets for gui items to remain at the same relative place regardless of screen size
offset_h = (window_size_h-1440)/2
offset_v = (window_size_v-900)

is_online = False

# set up the window
screen = pygame.display.set_mode((window_size_h, window_size_v), 0, 32)
classes.screen = screen

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# give the size of window to classes.py
classes.window_size_h = window_size_h
classes.window_size_v = window_size_v

max_health_value = 750.0
max_mana_value = 500.0
max_enemy_hp_value = 15000.0
health_value = 750.0
mana_value = 500.0
enemy_hp_value = 15000.0
health_percentage = health_value/max_health_value
mana_percentage = mana_value/max_mana_value
enemy_hp_percentage = enemy_hp_value/max_enemy_hp_value


# draw the black background onto the surface
screen.fill(BLACK)

# draw the window onto the screen
pygame.display.update()

# initialization of every element of the game (player, enemies, gui items)
###this should be moved to some other class eventually
player = classes.Player()
square_position_x = [510+offset_h,580+offset_h,670+offset_h,740+offset_h,810+offset_h,880+offset_h]
hp_container = classes.GuiStatic('bar_container.png',20+offset_h,830+offset_v)
mana_container = classes.GuiStatic('bar_container.png',970+offset_h,830+offset_v)
enemy_bar_container = classes.GuiStatic('enemy_bar_container.png',470+offset_h,20)
hp_bar = classes.GuiDynamic('hp_bar.png', 22+offset_h, 832+offset_v, 446, health_percentage)
mana_bar = classes.GuiDynamic('mana_bar.png', 972+offset_h, 832+offset_v, 446, mana_percentage)
enemy_bar = classes.GuiDynamic('enemy_bar.png', 472+offset_h, 22, 496, enemy_hp_percentage)
###IS THERE NO WAY TO DO THIS WITH A LIST? /rant
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
boss = classes.Enemy()


focus = player

pos = (50,50,50)

State = Enum('State', 'playing menu paused')
state = State.playing
things_on_screen = [player, hp_container, mana_container, enemy_bar_container,square0,square1,square2,square3,square4,square5,hp_bar,mana_bar,enemy_bar,hp_text,mana_text,lh_text,rh_text,s1_text,s2_text,s3_text,s4_text,boss]


paused = False

# run the game loop
while True:
    screen.fill(BLACK)
    if paused:
        pass
        # don't move anything
    else:
        for thing in things_on_screen:
            thing.tick()

    # Handle events
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
                        paused = True

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

