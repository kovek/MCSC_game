import pygame, sys, os
from pygame.locals import *
from enum import Enum
import classes

# set up pygame
pygame.init()
pygame.font.init()
myfont = pygame.font.Font("/Users/macadmin/Library/Fonts/SourceCodePro-Black.ttf", 15)

# set up the window
screen = pygame.display.set_mode((1440/2, 900), 0, 32)
classes.screen = screen

hp_container = pygame.image.load(os.path.join('.', 'data', 'bar_container.png'))
hp_bar = pygame.image.load(os.path.join('.', 'data', 'hp_bar.png'))
mana_bar = pygame.image.load(os.path.join('.', 'data', 'mana_bar.png'))
square = pygame.image.load(os.path.join('.', 'data', 'square.png'))
enemy_bar_container = pygame.image.load(os.path.join('.', 'data', 'enemy_bar_container.png'))
enemy_bar = pygame.image.load(os.path.join('.', 'data', 'enemy_bar_fill.png'))
player_image = pygame.image.load(os.path.join('.', 'data', 'player.png'))
boss = pygame.image.load(os.path.join('.', 'data', 'boss.png'))

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

HP = myfont.render("HP", 1, WHITE)
MP = myfont.render("MP", 1, WHITE)
LH = myfont.render("LH", 1, WHITE)
RH = myfont.render("RH", 1, WHITE)
S1 = myfont.render("1", 1, WHITE)
S2 = myfont.render("2", 1, WHITE)
S3 = myfont.render("3", 1, WHITE)
S4 = myfont.render("4", 1, WHITE)

health_value = 0.5 * 450
mana_value = 0.7 * 450

# draw the white background onto the surface
screen.fill(BLACK)
screen.blit(hp_bar, (20,830), (10,10,health_value,50) )
screen.blit(mana_bar, (970,830), (10,10,mana_value,50) )
screen.blit(hp_container, (20,830) )
screen.blit(hp_container, (970,830) )
screen.blit(enemy_bar_container, (470,20) )
screen.blit(enemy_bar, (470,20) )
screen.blit(square, (510,830) )
screen.blit(square, (580,830) )
screen.blit(square, (670,830) )
screen.blit(square, (740,830) )
screen.blit(square, (810,830) )
screen.blit(square, (880,830) )
screen.blit(HP, (20, 810))
screen.blit(MP, (970, 810))
screen.blit(LH, (510, 810))
screen.blit(RH, (580, 810))
screen.blit(S1, (670, 810))
screen.blit(S2, (740, 810))
screen.blit(S3, (810, 810))
screen.blit(S4, (880, 810))
screen.blit(player_image, (300, 600))
screen.blit(boss, (700, 300))


# draw the window onto the screen
pygame.display.update()

player = classes.Player()
focus = player

pos = (50,50,50)

State = Enum('State', 'playing menu paused')
state = State.playing
things_on_screen = [player]

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
                    pass
                    # If not online, stop game.
                        # paused = True

                    # bring up pause menu.
                        # PauseMenu.show()

                    # put pause menu to focus.
                        # focus = PauseMenu

                if state == State.menu or state == State.paused:
                    # send the escape event to menu. It will 'go back' if it can. If not, then it will remove the pause menu.
                    focus.escape_pressed()

        focus.key_event(event)
    pygame.display.update()

