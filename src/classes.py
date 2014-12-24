# For now, the classes are in a file apart. It does not mean they will stay organized this way.
import pygame, sys, os
from pygame.locals import *
from operator import add
#import numpy
import math

screen = None

FRAMES_PER_SECOND = 500
JUMP_SPEED = 1.5

class OnScreenImage(object):
    def __init__(self):
        pass
    def draw(self):
        pass
    def tick(self):
        self.frame = (self.frame+1)%self.FRAME_NUMBERS
        return

class OnScreenImageGui(object):
    pass

class Gui(object):
    # should this be am on_screen_image or should it just be an `object` that contains on_screen_image things?
    def __init__(self):
        pass

class GuiItem(OnScreenImage):
    def __init__(self):
        pass

class Menu(object):
    def __init__(self):
        pass

    def key_event(self, event):
        if event.type == KEYDOWN:
            pass
            # manage the key
        pass

class ContainerOnMenu(OnScreenImage):
    def __init__(self):
        pass

class OptionInContainer(OnScreenImage):
    def __init__(self):
        pass

class OnField(OnScreenImage):
    def __init__(self):
        pass

class Item(OnField):
    def __init__(self):
        pass

class Being(OnScreenImage):
    # Being as in something that moves by itself.
    def __init__(self):
        pass
    def tick(self):
        pass
        return
        super(self.__class__, self).tick()

def translate(x,y,z):
    return [
        [1.0,0,0,x],
        [0,1.0,0,y],
        [0,0,1.0,z],
        [0,0,0,1.0]
    ]

#def rotate(x,y):
 #   rot_x = [
  #      [1.0,0,0,0],
   #    [0,math.sin(x),math.cos(x),0],
    #    [0,0,0,1.0]
    #]
    #rot_y = [
     #   [math.cos(y),0,math.sin(y),0],
      #  [0,1.0,0,0],
       # [-math.sin(y),0,math.cos(y),0],
        #[0,0,0,1.0]
    #]
    #return numpy.dot(rot_x, rot_y)


fzNear = 0.5
fzFar = 30.0
frustumScale = 1.0

perspectiveMatrix = [
    [frustumScale,  0,              0,                                  0],
    [0,             frustumScale,   0,                                  0],
    [0,             0,              (fzFar + fzNear) / (fzNear-fzFar),  (2*fzFar * fzNear) / (fzNear - fzFar)],
    [0,             0,              -1.0,                               0.0]
]

def pos_to_2d(position):
    #print position+(1,)
    f = translate(0.0,10.0,0.0)
    f = numpy.dot(rotate(1.0, 0), f)
    f = numpy.dot(perspectiveMatrix, f)
    out = numpy.dot(f, list(position+(1,)) )
    #print out
    out2 = (out[0], out[2])
    return out2

class Player(Being):
    def __init__(self):
        self.position = (50,50,-50)
        self.velocity = (0,0,0)
        self.pressed_keys = []
        self.keys = {
            K_w: (0,0,1),
            K_a: (-1,0,0),
            K_s: (0,0,-1),
            K_d: (1,0,0)
        }
        self.player_image = pygame.image.load(os.path.join('.', 'data', 'player.png'))
        self.player_shadow = pygame.image.load(os.path.join('.', 'data', 'shadow.png'))
        self.jumping = False
        self.velocity_up = 0

    def draw(self):
        screen.blit(self.player_image, pos_to_2d(self.position) )
        screen.blit(self.player_shadow, pos_to_2d( (self.position[0], 0, self.position[2]) ) )

    def move(self):
        self.position = tuple(map(add, self.position, self.velocity)) # Add movement to position

    def key_event(self, event):
        if event.type == KEYDOWN:
            self.pressed_keys.append(event.key)
        elif event.type == KEYUP:
            if event.key in self.pressed_keys:
                self.pressed_keys.remove(event.key)


    def tick(self):
        super(self.__class__, self).tick()
        self.draw()


        # Handle keys
        for key in self.pressed_keys:
            if key == K_SPACE:
                if not self.jumping:
                    self.jumping = True
                    self.velocity_up = JUMP_SPEED
            try:
                self.position = tuple(map(add, self.position, self.keys[key]))
            except Exception:
                pass

        if self.jumping:
            z = self.velocity_up*1 + 1.0/2*(-9.8)*((1/FRAMES_PER_SECOND)**2)
            self.velocity_up = self.velocity_up -9.8*1/FRAMES_PER_SECOND
            self.position = tuple(map(add, self.position, (0,z,0)))
        if JUMP_SPEED + self.velocity_up <= 0.0 and self.velocity_up < 0:
            # Here we assume that the only possible height at which the player
            # can be is 0. Later on, I think we might have some platforms, so we
            # will need to work out other abstractions
            self.jumping = False
            self.velocity_up = 0


class Enemy(Being):
    def __init__(self):
        pass

class Manager(object):
    def __init__(self):
        pass
