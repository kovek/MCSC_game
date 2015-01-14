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
bypass = True
window_size_h = 0
window_size_v = 0
sun_degree = 0

if not bypass:
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
elif bypass:
    window_size_h = configs['options']['resolution'][0]
    window_size_v = configs['options']['resolution'][1]

# offsets for gui items to remain at the same relative place regardless of screen size
offset_h = (window_size_h-1440)/2
offset_v = (window_size_v-900)
is_online = False

# Set up the window
screen = pygame.display.set_mode((window_size_h, window_size_v), 0, 32)
pygame.display.toggle_fullscreen
classes.screen = screen
guiclasses.screen = screen

classes.window_size_h = window_size_h
classes.window_size_v = window_size_v

BLACK = (0, 0, 0)

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
player = classes.Warrior()
player.components['controls'].pygame = pygame

health_bar = guiclasses.GUIItem('health')
mana_bar = guiclasses.GUIItem('mana')

sun = classes.Star()

boss = classes.RagdollBoss()

# Use this to know what state the game is at
State = Enum('State', 'playing menu paused')
state = State.playing

guiclasses.PlayingGUI.components['health_bar'].components['content'].linked_entity = player

# things_on_screen contains everything that must be drawn by pygame.

# run the game loop
while True:
    screen.fill(BLACK)
    if state == State.paused:
        # don't move anything
        pass
    else:
        classes.PhysicsManager.tick()
        classes.ControlsManager.tick()
        classes.StarManager.tick()

        # Draw things
        classes.Battlefield.tick()
        classes.ShadowManager.tick()
        classes.RenderManager.tick()

        classes.CollisionsManager.tick()

        guiclasses.PlayingGUI.tick()

    pygame.display.update()
