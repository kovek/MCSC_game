import pygame, sys, os
from pygame.locals import *
from enum import Enum
import classes
import yaml
import guiclasses

configs = yaml.load( file('../local/config.yaml') )

# set up pygame
pygame.init()
# this bypasses the resolution selection and makes it 1080p by default, get rekt peasants
bypass = 1
window_size_h = 0
window_size_v = 0
sun_degree = 0
if bypass == 0:
    print "Sup m8 this game runs only at resolutions above 1440x900, umad ppl stuck in 2010? XD"
    # get input for horizontal size, get new one if below 1440 px or not an int
    print "Gimme window horizontal size in pixels:"
    while True:
        try:
            window_size_h = input()
        except:
            print "U 'avin a giggle m8? Gimme horizontal size as an int, at least 1440"
        else:
            if window_size_h >= 1440:
                break
            else:
                print "U 'avin a giggle m80? Gimme horizontal size at least 1440"
                pass
    print "Gimme window vertical size in pixels:"
    # get input for vertical size, get new one if below 900 px or not an int
    while True:
        try:
            window_size_v = input()
        except:
            print "U 'avin a giggle m8? Gimme vertical size as an int, at least 900"
        else:
            if window_size_v >= 900:
                break
            else:
                print "U 'avin a giggle m80? Gimme vertical size at least 900"
                pass
elif bypass == 1:
    window_size_h = configs['options']['resolution'][0]
    window_size_v = configs['options']['resolution'][1]
# offsets for gui items to remain at the same relative place regardless of screen size
offset_h = (window_size_h-1440)/2
offset_v = (window_size_v-900)
is_online = False

# set up the window
screen = pygame.display.set_mode((window_size_h, window_size_v), 0, 32)
pygame.display.toggle_fullscreen
classes.screen = screen
guiclasses.screen = screen

# Set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

classes.window_size_h = window_size_h
classes.window_size_v = window_size_v

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


# draw the black background onto the surface
screen.fill(BLACK)

# draw the window onto the screen
pygame.display.update()
#pygame.display.toggle_fullscreen()

# initialization of every element of the game (player, enemies, gui items)
###this should be moved to some other class eventually
player = classes.Warrior()
player.components['controls'].pygame = pygame
"""
walls = [
	classes.Wall([250,0,0], [-1,0,0]),
	classes.Wall([-250,0,0], [1,0,0]),
	classes.Wall([0,0,250], [0,0-1]),
	classes.Wall([0,0,-250], [0,0,1]),
	classes.Wall([0,0,0], [0,1,0]) ]
	"""
health_bar = guiclasses.GUIItem('health')
mana_bar = guiclasses.GUIItem('mana')

"""
square_position_x = [510+offset_h,580+offset_h,670+offset_h,740+offset_h,810+offset_h,880+offset_h]
hp_container = classes.GuiStatic('bar_container.png',20+offset_h,830+offset_v)
mana_container = classes.GuiStatic('bar_container.png',970+offset_h,830+offset_v)
enemy_bar_container = classes.GuiStatic('enemy_bar_container.png',470+offset_h,20)
hp_bar = classes.GuiDynamic('hp_bar.png', 22+offset_h, 832+offset_v, 446, health_percentage)
#mana_bar = classes.GuiDynamic('mana_bar.png', 972+offset_h, 832+offset_v, 446, mana_percentage)
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
#player_shadow = classes.Shadow(player,'player',sun)
#boss_shadow = classes.Shadow(boss,'boss',sun)
"""

sun = classes.Star()

focus = player

# Use this to know what state the game is at
State = Enum('State', 'playing menu paused')
state = State.playing

# things_on_screen contains everything that must be drawn by pygame.
things_on_screen = [classes.Battlefield(), classes.RagdollBoss(), player, sun, mana_bar, health_bar]
classes.PhysicsEngine.things_on_field = things_on_screen

# run the game loop
while True:
    screen.fill(BLACK)
    if state == State.paused:
        pass
        # don't move anything
    else:
        for thing in things_on_screen:
            thing.tick()

    # Handle events (keys)
    pygame.display.update()

