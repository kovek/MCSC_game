import pygame, sys, os
from pygame.locals import *
from enum import Enum
import classes
from classes import animation_loop

# set up pygame
pygame.init()
is_online = False

# set up the window
screen = pygame.display.set_mode((1440, 900), 0, 32)
classes.screen = screen

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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

#this should be moved to some other class eventually
player = classes.Player()
square_position_x = [510,580,670,740,810,880]
hp_container = classes.GuiStatic('bar_container.png',20,830)
mana_container = classes.GuiStatic('bar_container.png',970,830)
enemy_bar_container = classes.GuiStatic('enemy_bar_container.png',470,20)
hp_bar = classes.GuiDynamic('hp_bar.png', 22, 832, 446, health_percentage)
mana_bar = classes.GuiDynamic('mana_bar.png', 972, 832, 446, mana_percentage)
enemy_bar = classes.GuiDynamic('enemy_bar.png', 472, 22, 496, enemy_hp_percentage)
#IS THERE NO WAY TO DO THIS WITH A LIST? /rant
square0 = classes.GuiStatic('square.png', square_position_x[0], 830)
square1 = classes.GuiStatic('square.png', square_position_x[1], 830)
square2 = classes.GuiStatic('square.png', square_position_x[2], 830)
square3 = classes.GuiStatic('square.png', square_position_x[3], 830)
square4 = classes.GuiStatic('square.png', square_position_x[4], 830)
square5 = classes.GuiStatic('square.png', square_position_x[5], 830)
hp_text = classes.GuiText('HP',20,810)
mana_text = classes.GuiText('MP', 970, 810)
lh_text = classes.GuiText('LH',510,810)
rh_text = classes.GuiText('RH',580,810)
s1_text = classes.GuiText('S1',670,810)
s2_text = classes.GuiText('S2',740,810)
s3_text = classes.GuiText('S3',810,810)
s4_text = classes.GuiText('S4',880,810)
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

