# For now, the classes are in a file apart. It does not mean they will stay organized this way.
import pygame, sys, os
from pygame.locals import *
from operator import add
import numpy
import math
import random

# set up pygame, random number generator, font and colors
pygame.init()
pygame.font.init()
random.seed()
screen = None
COMIC_SANS = os.path.join('..','data', 'comic.ttf')
myfont = pygame.font.Font(COMIC_SANS, 15)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# variables for target framerate, milliseconds per animation frame and jump speed of character
FRAMES_PER_SECOND = 500
MS_PER_FRAME = 200
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

class Menu(object):
    def __init__(self):
        pass

    def key_event(self, event):
        if event.type == KEYDOWN:
            pass
            # manage the key
        pass

class PauseMenu(Menu):
    # The menu tree must be a stack

    def __init__(self):
        # level in the options tree
        self.level = 0
        pass

    @classmethod
    def show(cls):

        pass

    @classmethod
    def key_event(cls, event):
        pass

    @classmethod
    def escape_pressed(cls):
        if self.level == 0:
            return "close_menu"
        else:
            # Go back the menu tree.
            return

class ContainerOnMenu(OnScreenImage):
    def __init__(self):
        pass

class OptionInContainer(OnScreenImage):
    def __init__(self):
        self.image = 'somefile'
        self.corners = [1,2,3,4]
        self.borders = [1,2,3,4]
        self.filler = 0
        self.height = None # Place height of option here. The parent Menu will need to know it.

    def draw(self, x, y, width):
        for i in xrange(4):
            screen.blit(self.corners[i], (x,y) )
        for i in xrange(4):
            screen.blit(self.borders[i], (x,y) )
        #figure_out_height_given_font(font, text, width)
        screen.blit(self.filler, (x+size_of_corner,y+size_of_corner) )

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

class GuiItem(OnScreenImage):
    # GuiItem as in something that is part of the GUI
    def __init__(self):
        pass
    def tick(self):
        pass
        return
        super(self.__class__, self).tick()

# this function increments a value everytime the time specified in MS_PER_FRAME passes, this is used for animating objects
def animation_loop(animation_counter):
        if (pygame.time.get_ticks()//MS_PER_FRAME )-animation_counter > 0:
            animation_counter += 1
        return animation_counter

def translate(x,y,z):
    return [
        [1.0,0,0,x],
        [0,1.0,0,y],
        [0,0,1.0,z],
        [0,0,0,1.0]
    ]

def rotate(x,y):
    rot_x = [
        [1.0,0,0,0],
        [0,math.cos(x),-math.sin(x),0],
        [0,math.sin(x),math.cos(x),0],
        [0,0,0,1.0]
    ]
    rot_y = [
        [math.cos(y),0,math.sin(y),0],
        [0,1.0,0,0],
        [-math.sin(y),0,math.cos(y),0],
        [0,0,0,1.0]
    ]
    return numpy.dot(rot_x, rot_y)

def scale(x, y, z):
    return [
        [x,0,0,0],
        [0,y,0,0],
        [0,0,z,0],
        [0,0,0,1.0]
    ]

fzNear = 10.0
fzFar = 510.0
frustumScale = 0.9 # Gots to be just enough to englobe the whole field

length_of_field = 500
width_of_field = 200
elevation_of_camera = 50
push_back_of_camera_from_field = 10
push_back_of_camera = length_of_field/2 + push_back_of_camera_from_field
angle_of_camera = math.atan( float(elevation_of_camera)/float(push_back_of_camera))

perspectiveMatrix = [
    [frustumScale/(1440.0/900.0),  0,              0,                                  0],
    [0,             -frustumScale,   0,                                  0],
    [0,             0,              (fzFar + fzNear) / (fzNear-fzFar),  (2*fzFar * fzNear) / (fzNear - fzFar)],
    [0,             0,              -1.0,                               0.0]
]

translation_of_camera =  translate(0.0, -elevation_of_camera, -push_back_of_camera)
rotation_of_camera = rotate(0, 0)
camera_matrix = numpy.dot(rotation_of_camera, translation_of_camera)
camera_matrix = numpy.dot(perspectiveMatrix, camera_matrix)


def pos_to_2d(position):
    out = numpy.dot(camera_matrix, list(position+(1,)) )
    for i in range(len(out)):
        out[i] /= out[3]
    out[0] *= window_size_h
    out[1] *= window_size_v
    out[0] += window_size_h/2
    out[1] += window_size_v/2
    out2 = ( int(out[0]), int(out[1]) )
    return out2

class Player(Being):
    def __init__(self):
        self.time_anim = 0
        self.time_anim_temp = 0
        self.framepos = 0
        self.frameposjump = 0
        self.position = (0,0,0)
        self.velocity = (0,0,0)
        self.pressed_keys = []
        self.keys = {
            K_w: (0,0,-1),
            K_a: (-1,0,0),
            K_s: (0,0,1),
            K_d: (1,0,0)
        }
        self.player_image = pygame.image.load(os.path.join('..', 'data', 'sprites', 'classes', 'anim.png'))
        self.player_shadow = pygame.image.load(os.path.join('..', 'data', 'sprites', 'shadow.png'))

        self.jumping = False
        self.velocity_up = 0

    def draw(self):
        # this resets the 3D velocity tuple
        self.velocity = (0,0,0)
        # this looks for any key that has been pressed that is used for 2D movement and adds its tuple to the velocity to get the sum of the velocities
        for key in self.pressed_keys:
            if key is not K_SPACE:
                self.velocity = tuple(map(add,self.velocity,self.keys[key]))

        edges = [list(pos_to_2d( (-250,0,-250) )), list(pos_to_2d( (250,0,-250) )), list(pos_to_2d( (250,0,250) )), list(pos_to_2d( (-250,0,250) )) ]
        pygame.draw.polygon(screen, (0,0,255), edges )

        # this gets a temporary value for animation purposes and compares it to the existing value to see if it is greater (i.e. the required time MS_PER_FRAME has passed)
        # if the value is greater, the horizontal position of the part of the spritesheet that serves for the character's sprite is modified to animate it) <- if you do not understand this it's ok
        self.time_anim_temp=animation_loop(self.time_anim)
        if self.time_anim_temp > self.time_anim:
            if self.framepos == 180:
                self.framepos = 0
                self.frameposjump = 0
            else:
                self.framepos = self.framepos+20
                self.frameposjump = self.frameposjump+20
        else:
            pass
        # dictionary to know which velocity tuple corresponds to which vertical position on the sprite sheet that will be used for the character's sprite <- if you do not understand this it's ok
        self.character_sprites = {
            (-1,0,1): 0,
            (1,0,1): 1,
            (-1,0,-1): 2,
            (1,0,-1): 3,
            (0,0,1): 4,
            (0,0,-1): 5,
            (-1,0,0): 6,
            (1,0,0): 7,
            (0,0,0): 8
            }
        # sets the character's sprite to the default non-moving player sprite if velocity is 0
        if self.velocity == (0,0,0):
            screen.blit(self.player_image, pos_to_2d(self.position), (0,50*self.character_sprites[self.velocity],20,50) )
        # if it is not, sets the character's sprite to the corresponding animation sprite
        else:
            screen.blit(self.player_image, pos_to_2d(self.position), (self.framepos,50*self.character_sprites[self.velocity],20,50) )
        # if jumping, sets the character's sprite to the corresponding jumping animation sprite
        if self.jumping == False:
            self.frameposjump = 0
        # copies the temporary value to the actual value for animation purposes, so they are equal again for the time specified in MS_PER_FRAME and the frames don't change
        elif self.jumping == True:
            screen.blit(self.player_image, pos_to_2d(self.position), (self.frameposjump,50*9,20,50) )

        screen.blit(self.player_shadow, pos_to_2d( (self.position[0], 0, self.position[2]) ) )
        self.time_anim = self.time_anim_temp


    def move(self):
            self.position = tuple(map(add, self.position, self.velocity)) # Add movement to position

    def key_event(self, event):
        if event.type == KEYDOWN and event.key in self.keys:
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
            z = self.velocity_up*1 + 1.0/2*(-6.8)*((1/FRAMES_PER_SECOND)**2)
            self.velocity_up = self.velocity_up -6.8*1/FRAMES_PER_SECOND
            self.position = tuple(map(add, self.position, (0,z,0)))
        if JUMP_SPEED + self.velocity_up <= 0.0 and self.velocity_up < 0:
            # Here we assume that the only possible height at which the player
            # can be is 0. Later on, I think we might have some platforms, so we
            # will need to work out other abstractions
            self.jumping = False
            self.velocity_up = 0

# enemy class
class Enemy(Being):
    # self
    def __init__(self):
        # initializes enemy sprite from file
        self.gui_item = pygame.image.load(os.path.join('..', 'data', 'sprites', 'bosses', 'boss.png'))
        # sets x and y position for enemy to random values within the window
        self.position_x = random.randint(0,1340)
        self.position_y = random.randint(0,700)
    # draws enemy at (x,y) coordinates
    def draw(self,position_x,position_y):
      screen.blit(self.gui_item, (self.position_x, self.position_y))

    def tick(self):
        super(self.__class__, self).tick()
        self.draw(self.position_x,self.position_y)

class GuiStatic(GuiItem):
    # self; image is the supplied image file, posx and posy are the supplied (x,y) coordinates 
    def __init__(self,image,posx,posy):
        # initializes static gui item from supplied image file
        self.gui_item = pygame.image.load(os.path.join('..', 'data', 'gui', image))
        # sets x and y position for gui item to supplied (x,y) coordinates
        self.position_x = posx
        self.position_y = posy
    # draws static gui item at (x,y) coordinates)
    def draw(self,position_x,position_y):
      screen.blit(self.gui_item, (self.position_x, self.position_y))

    def tick(self):
        super(self.__class__, self).tick()
        self.draw(self.position_x,self.position_y)

class GuiDynamic(GuiItem):
    # self; image is the supplied image file, posx and posy are the supplied (x,y) coordinates, size is the size of the dynamic gui item when it is full, percent is the amount of dynamic gui item to display (0<=percent<=1)
    def __init__(self,image,posx,posy,size,percent):
        # initializes dynamic gui item from supplied image file
        self.gui_item = pygame.image.load(os.path.join('..', 'data', 'gui', image))
        # sets x and y position for gui item to supplied (x,y) coordinates
        self.position_x = posx
        self.position_y = posy
        # sets size and percentage for gui item to supplied size and percent
        self.size = size
        self.percentage = percent
    # draws dynamic gui item at (x,y) coordinates, where its length is its size times the percentage of it being displayed
    def draw(self,position_x,position_y):
      screen.blit(self.gui_item, (self.position_x, self.position_y), (0,0,self.size*self.percentage,46))

    def tick(self):
        super(self.__class__, self).tick()
        self.draw(self.position_x,self.position_y)

class GuiText(GuiItem):
    # self; text is the supplied string, posx and posy are the supplied (x,y) coordinates
    def __init__(self,string,posx,posy):
        # draws text from the supplied is the supplied string with the myfont font in white
        self.gui_item = myfont.render(string, 1, WHITE)
        # sets x and y position for gui text to supplied (x,y) coordinates
        self.position_x = posx
        self.position_y = posy
        # draws gui text at (x,y) coordinates)
    def draw(self,position_x,position_y):
      screen.blit(self.gui_item, (self.position_x, self.position_y))

    def tick(self):
        super(self.__class__, self).tick()
        self.draw(self.position_x,self.position_y)

class Manager(object):
    def __init__(self):
        pass
