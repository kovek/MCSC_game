# For now, the classes are in a file apart. It does not mean they will stay organized this way.
import pygame, sys, os
from pygame.locals import *
from operator import add
import numpy
import math
import random

# set up pygame, random number generator, font, colors and math constants
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
PI = 3.14159265

# variables for target framerate, milliseconds per animation frame,jump speed of character, and time for 1 day (in ms = 6 min)
FRAMES_PER_SECOND = 500
MS_PER_FRAME = 200
JUMP_SPEED = 1.5
DAY_TIME = 360000

class OnScreenImage(object):
    """ Anything that is on the screen and needs an image file to be drawn """

    def __init__(self):
        pass
    def draw(self):
        pass
    def tick(self):
        self.frame = (self.frame+1)%self.FRAME_NUMBERS
        return

    """def __init__(self, width, height, x, y):
		self.width = width
		self.height = height
		self.x = x
		self.y = y
	def __repr__(self):
		return "An image of" + str(self.width) + "by" + str(self.height) + "positioned at" + str(self.x) + "," + str(self.y )
	#The bodycenter is the coordinates fed into the pygame draw command.
	def low_body_center(self):
		u = self.x - self.width/2
		v = self.y + self.height
		return (u,v)
	def body_center(self):
		u = self.x - self.width/2
		v = self.y - self.height/2
		return (u,v)"""

class OnScreenImageGui(object):
    pass


class Gui(object):
    # should this be am on_screen_image or should it just be an `object` that contains on_screen_image things?
    """ The Gui class will contain everything that will be displayed as a
        Graphical interface around the game."""

    def __init__(self):
        pass


class Menu(object):
    """ Basically this was supposed to hold all the different menus before
    playing a game. We might replace it with our Gooeypy menu after all. """

    def __init__(self):
        pass

    def key_event(self, event):
        if event.type == KEYDOWN:
            pass
            # manage the key
        pass


class PauseMenu(Menu):
    """ PauseMenu will contain buttons like:
        - Continue Game
        - Options
        - Go to Menu """

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
    """ This thing was supposed to contain a list of buttons and text inputs.
        However, we might be going with Gooeypy so we might remove that soon. """

    def __init__(self):
        pass


class OptionInContainer(OnScreenImage):
    """ One of the buttons in the container that is in a menu. """

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
    """ Something on the battlefield. Like a fireball or a boss or a player.
        Naturally, that means it will have a .position, a .velocity and other
        members"""

    def __init__(self):
        pass


class Item(OnField):
    """ An item that you can pick up. A potion? A cookie. Whatever.
        Pretty much the thing we're adding in this class is just the ability
        for the player to pick it up. """
    def __init__(self):
        pass


class Being(OnField):
    """ Being as in something that moves by itself. An Entity. It could be a
        player or a boss. """
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

# this function is the angle at which the sun is, moves by 1 degree every second in 0.01 degree steps (polling every 10ms)
def sun_loop(sun_angle):
    if (pygame.time.get_ticks()//(DAY_TIME/36000) - sun_angle > 0):
        sun_angle +=1
    return sun_angle

def translate(x,y,z):
    """ Return a translation matrix. """
    return [
        [1.0,0,0,x],
        [0,1.0,0,y],
        [0,0,1.0,z],
        [0,0,0,1.0]
    ]

def rotate(x,y):
    """ Return a rotation matrix. It rotates around the x- and y- axes. """
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
    """ Return a scaling matrix. """
    return [
        [x,0,0,0],
        [0,y,0,0],
        [0,0,z,0],
        [0,0,0,1.0]
    ]


# Numbers needed for depth perception
fzNear = 10.0
fzFar = 510.0
frustumScale = 0.9 # Gots to be just enough to englobe the whole field

# Numbers about "camera"
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

# Our transformations applied by doing dot products.
translation_of_camera =  translate(0.0, -elevation_of_camera, -push_back_of_camera)
rotation_of_camera = rotate(0, 0)
camera_matrix = numpy.dot(rotation_of_camera, translation_of_camera)
camera_matrix = numpy.dot(perspectiveMatrix, camera_matrix)


def pos_to_2d(position):
    """ Transform the current <x,y,z> point to a <x,y> point that will appear
        on the screen. That means we apply transformations to the point. """
    out = numpy.dot(camera_matrix, list(position+(1,)) )
    for i in range(len(out)):
        out[i] /= out[3]
    out[0] *= window_size_h_res
    out[1] *= window_size_v_res
    out[0] += window_size_h_res/2
    out[1] += window_size_v_res/2
    out2 = ( int(out[0]), int(out[1]) )
    return out2


class Player(Being):
    """ """

    # self; width is the player's width, height is the player's height, scaled_size stores the player's size after scaling, time_anim and time_anim_temp are variables for creating the animation
    # all the framepos are for positioning the area for the cropping, position and velocity are self-explanatory, velocity_up is used for jumping, equipment is a list of all the equipment types available to the player
    # equipment_held is a list used to store tuples describing what hand holds what equipment type for cropping purposes, pressed_keys is for keys that are currently pressed, keys are the keys currently accepted for controlling player and their effect on position
    # pressed_mouse is for mouse buttons that are currently pressed, mouse is the buttons currently accepted for controlling the player and the weapon type each hand holds, player_image_temp and hand_image_temp are the spritesheets
    # jumping/lefthand/righthand are bools determining whether player is jumping/using left hand/using right hand
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.scaled_size = [self.width,self.height]
        self.time_anim = 0
        self.time_anim_temp = 0
        self.framepos = 0
        self.frameposjump = 0
        self.lefthand_framepos = 0
        self.righthand_framepos = 0
        self.position = (0,0,0)
        self.velocity = (0,0,0)
        self.velocity_up = 0
        self.equipment = ['Sword','Shield']
        self.equipment_held = [(),()]
        self.pressed_keys = []
        self.keys = {
            K_w: (0,0,-1),
            K_a: (-1,0,0),
            K_s: (0,0,1),
            K_d: (1,0,0),
            K_SPACE: (0,0,0)
        }
        self.pressed_mouse = []
        ### for now the equipment is set in __init__, maybe use change_equipment instead?
        self.mouse = {
            'LEFT': self.equipment[1],
            'RIGHT': self.equipment[1]
        }
        self.player_image_temp = pygame.image.load(os.path.join('..', 'data', 'sprites', 'classes', 'player_anim.png'))
        self.hand_image_temp = pygame.image.load(os.path.join('..', 'data', 'sprites', 'classes', 'hands_anim.png'))
        self.jumping = False
        self.lefthand = False
        self.righthand = False

    def resize(self):
        self.width = self.width * window_size_h_res/window_size_h_ren
        self.height = self.height * window_size_v_res/window_size_v_ren
        self.player_image_temp = pygame.transform.rotozoom(self.player_image_temp, 0, (window_size_h_res/window_size_h_ren))
        self.hand_image_temp = pygame.transform.rotozoom(self.hand_image_temp, 0, (window_size_h_res/window_size_h_ren))

    # this function will be used later to change the equipment of the player, for now it is just copy pasta
    def change_equipment(self):
        self.mouse['LEFT'] = self.equipment[1]
        self.mouse['RIGHT'] = self.equipment[1]

    # this crops the spritesheet using subsurfaces to get the correct sprite for a given action    
    def crop(self):
        # this resets the 3D velocity tuple
        self.velocity = (0,self.velocity_up,0)
        # this looks for any key that has been pressed that is used for 2D movement and adds its tuple to the velocity to get the sum of the velocities
        for key in self.pressed_keys:
                self.velocity = tuple(map(add,self.velocity,self.keys[key]))

        ### THIS NEEDS TO BE REMOVED OF PLAYER AT ONCE
        #edges = [list(pos_to_2d( (-250,0,-250) )), list(pos_to_2d( (250,0,-250) )), list(pos_to_2d( (250,0,250) )), list(pos_to_2d( (-250,0,250) )) ]
        #pygame.draw.polygon(screen, (0,0,255), edges )

        # this gets a temporary value for animation purposes and compares it to the existing value to see if it is greater (i.e. the required time MS_PER_FRAME has passed)
        # if the value is greater, the horizontal position of the part of the spritesheet that serves for the character's sprite is modified to animate it) <- if you do not understand this it's ok
        self.time_anim_temp=animation_loop(self.time_anim)
        if self.time_anim_temp > self.time_anim:
            if self.framepos == 9*self.width:
                self.framepos = 0
                self.frameposjump = 0
            else:
                self.framepos = self.framepos+self.width
                self.frameposjump = self.frameposjump+self.width
        else:
            pass
        
        # if not jumping, reset the frame for jumping
        if self.jumping == False:
            self.frameposjump = 0

        # same as above but for left hand, and stops looping when self.lefthand is no longer true and the left hand animation has ended
        if self.time_anim_temp > self.time_anim:    
                if self.lefthand_framepos == 9*self.width:
                    self.lefthand_framepos = 0
                elif self.lefthand == False and self.lefthand_framepos != 0:
                    self.lefthand_framepos = self.lefthand_framepos+self.width
                elif self.lefthand == True:
                    self.lefthand_framepos = self.lefthand_framepos+self.width
                else:
                    pass

        # same as above but for right hand, and stops looping when self.righthand is no longer true and the right hand animation has ended
        if self.time_anim_temp > self.time_anim:    
                if self.righthand_framepos == 9*self.width:
                    self.righthand_framepos = 0
                elif self.righthand == False and self.righthand_framepos != 0:
                    self.righthand_framepos = self.righthand_framepos+self.width
                elif self.righthand == True:
                    self.righthand_framepos = self.righthand_framepos+self.width
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

        # dictionary to know which hand/equipment combination corresponds to which vertical position on the sprite sheet that will be used for the charater's sprite <- if you do not understand this it's ok
        self.hand_equipment  = [(mouse, equipment) for mouse in self.mouse for equipment in self.equipment]
        self.hand_equipment.reverse()
        self.hand_equipment_sprites = {self.hand_equipment[i]: i for i in range(len(self.hand_equipment))}
        """print self.hand_equipment_sprites""" #debug
        
        # sets the character's sprite to the default non-moving player sprite if velocity is 0
        if self.velocity == (0,0,0):
            self.player_image = self.player_image_temp.subsurface( (0,self.height*self.character_sprites[self.velocity],self.width,self.height) )
        # sets the character's sprite to the jumping player sprite if vertical velocity is not 0
        elif self.velocity[1] != 0:
             self.player_image = self.player_image_temp.subsurface( (self.frameposjump,self.height*9,self.width,self.height) )
        # otherwise sets the characer's sprite to the moving player sprite in the appropriate direction
        else:
            self.player_image = self.player_image_temp.subsurface( (self.framepos,self.height*self.character_sprites[self.velocity],self.width,self.height) )
        # loads the equipment type for both hands
        self.equipment_held[0] = ('LEFT', self.mouse['LEFT'])
        self.equipment_held[1] = ('RIGHT', self.mouse['RIGHT'])
        """print self.hand_equipment_sprites[self.equipment_held[0]], self.hand_equipment_sprites[self.equipment_held[1]]""" #debug
        # sets the hand sprite for the left hand
        self.hand_image_left = self.hand_image_temp.subsurface( (self.lefthand_framepos,self.height*self.hand_equipment_sprites[self.equipment_held[0]],self.width,self.height) )
        # sets the hand sprite for the right hand
        self.hand_image_right = self.hand_image_temp.subsurface( (self.righthand_framepos,self.height*self.hand_equipment_sprites[self.equipment_held[1]],self.width,self.height) )
      
        # copies the temporary value to the actual value for animation purposes, so they are equal again for the time specified in MS_PER_FRAME and the frames don't change
        self.time_anim = self.time_anim_temp

    # this scales the player based on his position on the z-axis
    def scale(self):
        # scaling done by taking the difference between pos_to_2d of the position and pos_to_2d of the position+the player's dimensions, yielding a scale factor
        self.position_i = self.position
        self.position_f = tuple(map(add, self.position, (self.width, self.height, 0)))
        self.position_i_2d = list(pos_to_2d(self.position_i))
        self.position_f_2d = list(pos_to_2d(self.position_f))
        self.scale_factor = float(self.position_f_2d[0]-self.position_i_2d[0])/float(self.width)
        self.scaled_size = [int(self.scale_factor*self.width),int(self.scale_factor*self.height)]
        self.scaled_size_float = [float(self.scale_factor*self.width),float(self.scale_factor*self.height)]

        # now resizing sprites for player, left hand and right hand
        self.player_image = pygame.transform.scale(self.player_image, (int(self.scaled_size_float[0]),int(self.scaled_size_float[1])))
        self.hand_image_left = pygame.transform.scale(self.hand_image_left, (int(self.scaled_size_float[0]),int(self.scaled_size_float[1])))
        self.hand_image_right = pygame.transform.scale(self.hand_image_right, (int(self.scaled_size_float[0]),int(self.scaled_size_float[1])))

    # moving the player
    def move(self):
            self.position = tuple(map(add, self.position, self.velocity)) # add movement to position

    # draws the player, left hand and right hand      
    def draw(self):
        screen.blit(self.player_image, pos_to_2d(self.position))
        screen.blit(self.hand_image_left, pos_to_2d(self.position))
        screen.blit(self.hand_image_right, pos_to_2d(self.position))

    # some stuff to determine which keys and mouse buttons are pressed
    def key_event(self, event):
        # mouse.get_pressed returns buttons currently pressed in terms of numbers, that are converted to more practical strings via a dict
        self.mouse_list = list(pygame.mouse.get_pressed())
        self.mouse_list_dict = {
            0: 'LEFT',
            1: 'MIDDLE',
            2: 'RIGHT'
        }
        # addition and removal of mouse buttons as they are pressed and released, this also avoids duplicates
        for i in range(len(self.mouse_list)):
            if self.mouse_list[i] == True:
                if self.mouse_list_dict[i] in self.pressed_mouse:
                    pass
                else:
                    if self.mouse_list_dict[i] in self.mouse:
                        self.pressed_mouse.append(self.mouse_list_dict[i])
            elif self.mouse_list[i] == False:
                if self.mouse_list_dict[i] in self.pressed_mouse:
                    self.pressed_mouse.remove(self.mouse_list_dict[i])
        """print self.pressed_mouse""" #debug
        # much simpler for keyboard keys, checks if they should be added or removed, ezpz
        if event.type == KEYDOWN:
            if event.key in self.keys:
                self.pressed_keys.append(event.key)
        elif event.type == KEYUP:
            if event.key in self.pressed_keys:
                self.pressed_keys.remove(event.key)

    def tick(self):
        super(self.__class__, self).tick()
        self.crop()
        self.scale()
        self.move()
        self.draw()

        # handle keys and mouse
        for key in self.pressed_keys:
            if key == K_SPACE:
                if not self.jumping:
                    self.jumping = True
                    self.velocity_up = JUMP_SPEED
            # maybe remove comment block
            """try:
                self.position = tuple(map(add, self.position, self.keys[key]))
            except Exception:
                pass"""
        # changing the bools corresponding to left hand/right hand use if the corresponding mouse buttons are pressed
        if 'LEFT' in self.pressed_mouse:
            self.lefthand = True
        elif 'LEFT' not in self.pressed_mouse:
            self.lefthand = False
        if 'RIGHT' in self.pressed_mouse:
            self.righthand = True
        elif 'Right' not in self.pressed_mouse:
            self.righthand = False
        
        # handle jumping in a better way than previously
        if self.jumping:
            z = self.velocity_up*1 + 1.0/2*(-9.8)*((1/FRAMES_PER_SECOND)**2)  
            self.velocity_up = self.velocity_up -9.8*1/FRAMES_PER_SECOND
            self.position = tuple(map(add, self.position, (0,z,0)))
        if self.position[1] <= 0:
        # maybe remove comment block
            """if JUMP_SPEED + self.velocity_up <= 0.0 and self.velocity_up < 0:
             Here we assume that the only possible height at which the player
             can be is 0. Later on, I think we might have some platforms, so we
             will need to work out other abstractions"""
            self.jumping = False
            self.velocity_up = 0
            self.position = (self.position[0],0,self.position[2])

# this is the star class for various stars that generate shadows
class Star(Being):
    # self
    def __init__(self):
        # angle in 100ths of degrees (int)
        self.angle = 0
        # actual angle in degrees (float)
        self.angle_actual = 0
        # initial angle, CHANGE THIS TO SET INITIAL TIME OF DAY
        self.angle_initial = 0

    # increment the angle (currently in 100th of a degree every time 10ms pass)
    def increment_angle(self):
        self.angle = sun_loop(self.angle)
        # actual angle: takes the value in 100ths of a degree, divides it by 100 to get a value in degrees, adds the initial angle, and computes the congruent angle mod 360
        self.angle_actual = (self.angle_initial+float(float(self.angle)/100.0))%360
        """print self.angle_actual""" #debug
    def tick(self):
        super(self.__class__, self).tick()
        self.increment_angle()
        
# this is the shadow class for various shadows
class Shadow(Being):
    #self; owner is the thing that generates the shadow (its attributes are used extensively), owner_string is used to load the correct shadow, source is the stars (currently 1) that contribute to shadow generation
    def __init__(self,owner,owner_string,source):
        self.shadow_image = pygame.image.load(os.path.join('..', 'data', 'sprites', 'shadows', owner_string+'_shadow.png'))
        self.owner = owner
        self.source = source
        self.height = owner.scaled_size[0]/4

    # updates the shadow's position    
    def update_pos(self,owner,source):
        # using the owner's 3d position to compute the shadow's position offset when the owner jumps
        # converting position 3d tuples into lists
        self.position_3d = owner.position
        self.position_3d_list = list(self.position_3d)
        self.owner_position_list = list(owner.position)
        # shadow's height is always 0
        self.position_3d_list[1] = 0
        # for angles between 0 and 90 degrees, the shadow moves towards the left when the owner jumps
        if source.angle_actual >=0.0 and source.angle_actual <=90.0:
            # shadow's x-position is owner's x-position - owner's y-position * cot(angle)
            try:
                self.position_3d_list[0] = self.owner_position_list[0]-self.owner_position_list[1]*(math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180))
            # if cot(angle) = infinity, cot(angle) = 10000 (arbitrarily large value)
            except:
                self.position_3d_list[0] = self.owner_position_list[0]-self.owner_position_list[1]*10000
        # for angles between 90 and 180 degrees, the shadow moves towards the right when the owner jumps
        elif source.angle_actual >90.0 and source.angle_actual <=180.0:
            # shadow's x-position is owner's x-position + owner's y-position * cot(angle)
            try:
                self.position_3d_list[0] = self.owner_position_list[0]+self.owner_position_list[1]*abs((math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180)))
            # if cot(angle) = infinity, cot(angle) = 10000 (arbitrarily large value)
            except:
                self.position_3d_list[0] = self.owner_position_list[0]+self.owner_position_list[1]*10000
        # converting finished position 3d list into tuple
        self.position_3d = tuple(self.position_3d_list)

        # using the owner's 2d position to compute the shadow's position offset
        # converting position 3d tuple into 2d tuple and into list
        self.position = pos_to_2d(self.position_3d)
        self.position_list = list(self.position)
        # for angles between 0 and 90 degrees, the shadow's x-position has to be offset to the left by an amount equivalent to its length since it's to the left of the owner
        if source.angle_actual >=0.0 and source.angle_actual <=90.0:
            # shadow's x-position is its own x-position - its length, which is represented by: owner's height * cot(angle)
            try:
                self.position_list[0] = self.position_list[0]-(owner.scaled_size[1]*(math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180)))
            # if cot(angle) = infinity, shadow's length is 10000
            except:
                 self.position_list[0] = self.position_list[0]-10000
            # if cot(angle) is such that the shadow's length exceeds 10000, it becomes 10000
            else:
                if (owner.scaled_size[1]*(math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180))) > 10000:
                    self.position_list[0] = self.position_list[0]+(owner.scaled_size[1]*(math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180)))-10000
                    """print "Corrected!""""" #debug
        # for angles between 90 and 180 degrees, the shadow's x-position does not need offset since it's to the right of the owner
        elif source.angle_actual >90.0 and source.angle_actual <=180.0:
            pass
        # moving the shadow vertically to the owner's feet
        self.position_list[1] = self.position_list[1]+owner.scaled_size[1]-self.height/2
        # converting finished position tuple into list
        self.position = tuple(self.position_list)
    
    def update_scale(self,owner,source):
        # first of all, updating the shadow's height
        self.height = owner.scaled_size[0]/4
        # for angles between 0 and 90 degrees, cot(angle) is positive and requires no adjustment
        if source.angle_actual >=0.0 and source.angle_actual <=90.0:
            # shadow's length is equal to owner's height * cot(angle) and increased by owner's width (to make its minimum size the owner's width)
            try:
                self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (int(owner.scaled_size[0]+owner.scaled_size[1]*(math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180))),self.height))
            # if cot(angle) = infinity, shadow's length is 10000 and increased by owner's width
            except:
                self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (owner.scaled_size[0]+10000,self.height))
            # if cot(angle) is such that the shadow's length exceeds 10000, it becomes 10000 and increased by owner's width
            else:
                if (owner.scaled_size[0]+owner.scaled_size[1]*(math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180))) > 10000:
                    self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (owner.scaled_size[0]+10000,self.height))
                    """print "Corrected!""""" #debug
        # for angles between 90 and 180 degrees, cot(angle) is negative and thus abs(cot(angle)) must be used
        elif source.angle_actual >90.0 and source.angle_actual <=180.0:
            # shadow's length is equal to owner's height * abs(cot(angle)) and increased by owner's width (to make its minimum size the owner's width)
            try:
                self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (int(owner.scaled_size[0]+owner.scaled_size[1]*abs(math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180))),self.height))
            # if abs(cot(angle)) = infinity, shadow's length is 10000 and increased by owner's width
            except:
                self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (owner.scaled_size[0]+10000,self.height))
            # if cot(angle) is such that the shadow's length exceeds 10000, it becomes 10000 and increased by owner's width
            else:
                if (owner.scaled_size[0]+owner.scaled_size[1]*abs(math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180))) > 10000:
                    self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (owner.scaled_size[0]+10000,self.height))
                    """print "Corrected!""""" #debug
        # for angles above 180 degrees, the shadow does not appear and thus its size becomes 0
        elif source.angle_actual >180.0:
            self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (0,0))
    # finally we can update the scale and the position of the shadow and then draw it...
    def draw(self,*position):
        self.update_scale(self.owner,self.source)
        self.update_pos(self.owner,self.source)
        screen.blit(self.shadow_image_scaled, self.position)
    def tick(self):
        super(self.__class__, self).tick()
        self.draw()
        
class Enemy(Being):
    """ A class for the enemy. Will have to have some sort of AI. """

    # self; width is the enemy's width, height is the enemy's height, scaled_size stores the enemy's size after scaling, time_anim and time_anim_temp are variables for creating the animation
    # all the framepos are for positioning the area for the cropping, position and velocity are self-explanatory (the position is random for now), velocity_randomizer is a value used to determine the velocity randomly, eventually will be removed, enemy_image_temp is a spritesheet
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.scaled_size = [self.width,self.height]
        self.time_anim = 0
        self.time_anim_temp = 0
        self.framepos = 0
        self.position = (random.randint(-100,100),0,random.randint(-500,-400))
        self.velocity = (0,0,0)
        self.velocity_randomizer = 8
        self.enemy_image_temp = pygame.image.load(os.path.join('..', 'data', 'sprites', 'bosses', 'boss.png'))

    def resize(self):
        self.width = self.width * window_size_h_res/window_size_h_ren
        self.height = self.height * window_size_v_res/window_size_v_ren
        self.enemy_image_temp = pygame.transform.rotozoom(self.enemy_image_temp, 0, (window_size_h_res/window_size_h_ren))
        
    # the velocity is determined in a random way for now
    def randomize_parameters(self):
        self.randomize_chance = random.randint(0,100)
        if self.randomize_chance == 0:
            self.velocity_randomizer = random.randint(0,8)

    # this crops the spritesheet using subsurfaces to get the correct sprite for a given action            
    def crop(self):
        self.velocity_random_assignment = {
        0: (-1,0,1),
        1: (1,0,1),
        2: (0,0,0),
        3: (0,0,0),
        4: (0,0,1),
        5: (0,0,0),
        6: (-1,0,0),
        7: (1,0,0),
        8: (0,0,0)
        }
        # this resets the 3D velocity tuple
        self.velocity = self.velocity_random_assignment[self.velocity_randomizer]
        # this gets a temporary value for animation purposes and compares it to the existing value to see if it is greater (i.e. the required time MS_PER_FRAME has passed)
        # if the value is greater, the horizontal position of the part of the spritesheet that serves for the character's sprite is modified to animate it) <- if you do not understand this it's ok
        self.time_anim_temp=animation_loop(self.time_anim)
        if self.time_anim_temp > self.time_anim:
            if self.framepos == 9*self.width:
                self.framepos = 0
            else:
                self.framepos = self.framepos+self.width
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
                self.enemy_image = self.enemy_image_temp.subsurface( (0,self.height*self.character_sprites[self.velocity],self.width,self.height) )
        # otherwise sets the characer's sprite to the moving player sprite in the appropriate direction
        else:
                self.enemy_image = self.enemy_image_temp.subsurface( (self.framepos,self.height*self.character_sprites[self.velocity],self.width,self.height) )

        # copies the temporary value to the actual value for animation purposes, so they are equal again for the time specified in MS_PER_FRAME and the frames don't change
        self.time_anim = self.time_anim_temp

    # this scales the enemy based on his position on the z-axis
    def scale(self):
        # scaling done by taking the difference between pos_to_2d of the position and pos_to_2d of the position+the player's dimensions, yielding a scale factor
        self.position_i = self.position
        self.position_f = tuple(map(add, self.position, (self.width, self.height, 0)))
        self.position_i_2d = list(pos_to_2d(self.position_i))
        self.position_f_2d = list(pos_to_2d(self.position_f))
        self.scale_factor = float(self.position_f_2d[0]-self.position_i_2d[0])/float(self.width)
        self.scaled_size = [int(self.scale_factor*self.width),int(self.scale_factor*self.height)]
        self.scaled_size_float = [float(self.scale_factor*self.width),float(self.scale_factor*self.height)]
        print self.scaled_size_float

        # now resizing sprites for enemy
        self.enemy_image = pygame.transform.scale(self.enemy_image, (int(self.scaled_size_float[0]),int(self.scaled_size_float[1])))
        
    # moving the enemy
    def move(self):
            self.velocity_list = list(self.velocity)
            self.velocity_list = [self.velocity_list[i]/5.0 for i in range(3)]
            self.velocity = tuple(self.velocity_list)
            self.position = tuple(map(add, self.position, self.velocity)) # Add movement to position

    # draws the enemy
    def draw(self):
        screen.blit(self.enemy_image, pos_to_2d(self.position))

    def tick(self):
        super(self.__class__, self).tick()
        self.randomize_parameters()
        self.crop()
        self.scale()
        self.move()
        self.draw()

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
    """ The Manager of the whole game?
        For now the game runs perfectly fine with just a while loop but we might
        need to organize things more later on... """

    def __init__(self):
        pass
