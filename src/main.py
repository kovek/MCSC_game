import pygame, sys, os
from pygame.locals import *
from enum import Enum
import classes
import yaml
import guiclasses

configs = yaml.load( file('../local/config.yaml') )

# set up pygame and init
pygame.init()
is_online = False

# this bypasses the resolution selection and makes it 1080p by default, get rekt peasants
bypass = True
window_size_h = 0
window_size_v = 0
sun_degree = 0

window_size_h = configs['options']['resolution'][0]
window_size_v = configs['options']['resolution'][1]

# offsets for gui items to remain at the same relative place regardless of screen size
offset_h = (window_size_h-1440)/2
offset_v = (window_size_v-900)

# Set up the window
screen = pygame.display.set_mode((window_size_h, window_size_v), 0, 32)
pygame.display.toggle_fullscreen
classes.screen = screen
guiclasses.screen = screen

BLACK = (0, 0, 0)

# initialization of every element of the game (player, enemies, gui items)
###this should be moved to some other class eventually
player = classes.Warrior()
player.components['controls'].pygame = pygame

sun = classes.Star()

boss = classes.RagdollBoss()

import random
for i in range(10):
    bossi = classes.RagdollBoss()
    x = random.random()*200.0
    y = random.random()*200.0
    z = random.random()*200.0
    bossi.components['physics'].position = [x,y,z]


health_bar = guiclasses.GUIItem('health')
mana_bar = guiclasses.GUIItem('mana')
guiclasses.PlayingGUI.components['health_bar'].components['content'].linked_entity = player
guiclasses.PlayingGUI.components['boss_health'].components['content'].linked_entity = boss

# Use this to know what state the game is at
State = Enum('State', 'playing menu paused')
state = State.playing

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
        classes.TimeoutManager.tick()

        guiclasses.PlayingGUI.tick()

    pygame.display.update()
