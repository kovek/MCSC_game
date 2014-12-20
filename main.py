import pygame, sys, os
from pygame.locals import *

# set up pygame
pygame.init()
pygame.font.init()
myfont = pygame.font.Font("/Users/macadmin/Library/Fonts/SourceCodePro-Black.ttf", 15)

# set up the window
screen = pygame.display.set_mode((1440, 900), 0, 32)

hp_container = pygame.image.load(os.path.join('.', 'bar_container.png'))
hp_bar = pygame.image.load(os.path.join('.', 'hp_bar.png'))
mana_bar = pygame.image.load(os.path.join('.', 'mana_bar.png'))
square = pygame.image.load(os.path.join('.', 'square.png'))
enemy_bar = pygame.image.load(os.path.join('.', 'enemy_bar.png'))
enemy_bar_fill = pygame.image.load(os.path.join('.', 'enemy_bar_fill.png'))
player = pygame.image.load(os.path.join('.', 'player.png'))
boss = pygame.image.load(os.path.join('.', 'boss.png'))

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
screen.blit(enemy_bar, (470,20) )
screen.blit(enemy_bar_fill, (470,20) )
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
screen.blit(player, (300, 600))
screen.blit(boss, (700, 300))

class player(object):
    def __init__(self):
        pass

    def draw(self):
        screen.blit(self.player, pos_to_2d(self.pos) )
        screen.blit(self.player_shadow, pos_to_2d(self.shadow_pos) ))

# draw the window onto the screen
pygame.display.update()

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
