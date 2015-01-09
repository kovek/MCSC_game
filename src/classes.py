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

class Render(object):
	def __init__(self, parent, source):
		self.parent = parent
		self.source = source
        #self.player_image = pygame.image.load(os.path.join('..', 'data', 'sprites', 'classes', 'player_anim.png'))
		self.pygame = self.parent.pygame
		self.player_image = pygame.image.load(os.path.join('..', 'data', 'sprites', 'classes', 'player_anim.png'))
		self.image = pygame.image.load(Resources[self.source]['spritesheet_file'])
	
	def tick(self):
		position = self.parent.components['physics'].position
		offset = Resources[self.source]['offset']
		
		screen.blit(self.image,
			pos_to_2d(self.parent.components['physics'].position),


		)

class Physics(object):
	def __init__(self, parent, position, velocity=[0,0,0] ):
		self.parent = parent
		self.position = position
		self.velocity = velocity

	def tick(self):
		for i in xrange(3):
			self.position[i] += self.velocity[i]

		# Acceleration of gravity
		self.velocity[2] = self.velocity[2]*1 + 1.0/2*(-6.8)*((1/FRAMES_PER_SECOND)**2)
		self.velocity[2] = self.velocity[2] -6.8*1/FRAMES_PER_SECOND
		print self.position

class PhysicsEngine(object):
	things_on_field = []

import itertools
class Collision(object):
	def __init__(self, parent, source):
		self.parent = parent
		self.source = source


		# needed to find all 8 corners of a box around a point
		self.permutations = []
		for subset in itertools.combinations_with_replacement([-1,1], 3):
			self.permutations.append(subset)
		for subset in itertools.combinations_with_replacement([1,-1], 3):
			self.permutations.append(subset)

	def tick(self):
		bounds = Resources[self.source]['box_size']
		position = self.parent.components['physics'].position
		x_bounds = (position[0]-bounds[0]/2.0, position[0]+bounds[0]/2.0)
		y_bounds = (position[1]-bounds[1]/2.0, position[1]+bounds[1]/2.0)
		z_bounds = (position[2]-bounds[2]/2.0, position[2]+bounds[2]/2.0)
		list_of_colliding_with_self = []
		for item in PhysicsEngine.things_on_field:
			item_position = item.components['physics'].position	
			box_size = Resources[item.name].box_size
			points = []
			
			for corner in self.permutations:
				points.append( [
					position[0] + 1/2.0 * corner[0] * box_size[0],
					position[1] + 1/2.0 * corner[1] * box_size[1],
					position[2] + 1/2.0 * corner[2] * box_size[2],
				] )

			for point in points:
				if x_bounds[0] < point[0] < x_bounds[0]:
					if y_bounds[0] < point[1] < y_bounds[0]:
						if x_bounds[2] < point[2] < _bounds[2]:
							list_of_colliding_with_self.append(item)
		for item in list_of_colliding_with_self:
			CollisionsPossible.collision(self.parent.name, item.name)(self.parent, item)

class CollisionsPossible(object):
	def __init__(self):
		pass

	def __getitem__(self, name):
		return getattr(self, name)

	def collision(self, one, two):
		return self[str(one) + '_with_' + str(two)]

	def Tree_with_Player(self, tree, player):
		print 'tree gives shadow to player'

	def Wall_with_Player(self, wall, player):
		# Push the character off

		# k is the distance we have to push the player off
		k = numpy.dot(player.components['physics'].position, wall.direction) + numpy.dot(player.components['collision'].box_size, wall.direction)/2.0 - ( numpy.dot(wall.components['physics'].position, wall.direction) - numpy.dot(wall.components['collision'].box_size, wall.direction)/2.0 )

		player.components['physics'].position = map(add,
			player.components['physics'].position,
			[x* (k) for x in wall.direction] )

class Battlefield(object):
	def __init__(self):
		self.components = {
				"render": Render("Battlefield"),
				"physics": {position: (0,0,0)}
			}


		pass

	def tick(self):
		pass


class Controls(object):
	def __init__(self, parent):
		self.parent = parent
		self.pygame = None
		self.pressed_keys = []

		self.keys = {
            K_w: [0,0,-1],
            K_a: [-1,0,0],
            K_s: [0,0,1],
            K_d: [1,0,0],
            K_SPACE: [0,0,0]
        }

	def tick(self):
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
							state = State.paused

						classes.PauseMenu.show()

						# put pause menu to focus.
						focus = classes.PauseMenu

						state = State.paused
					elif state == State.menu or state == State.paused:
						# send the escape event to menu. It will 'go back' if it can. If not, then it will remove the pause menu.
						if focus.escape_pressed() == "close_menu":
							pass
			self.key_event(event)

		for key in self.pressed_keys:
			if key in [K_w, K_a, K_s, K_d]:
				self.parent.components['physics'].velocity = self.keys[key]
			elif key is K_SPACE:
				if self.parent.components['physics'].velocity[1] is 0:
					self.parent.components['physics'].velocity[1] = 2
			else:
				pass

	def key_event(self, event):
		if event.type == KEYDOWN:
			if event.key in self.keys:
				self.pressed_keys.append(event.key)
		elif event.type == KEYUP:
			if event.key in self.pressed_keys:
				self.pressed_keys.remove(event.key)

class Wall(object):
	def __init__(self, position, direction):
		self.physics = {'position': position}
		self.direction = direction
		self.components = {
			"collision": Collision(self),
		}

	def tick(self):
		pass
	

class Warrior(object):
	def __init__(self, pygame):
		position = [0,0,0]
		self.pygame = pygame
		self.components = {
			'physics': Physics(self, position),
			'collision': Collision(self, "Warrior"),
			'controls': Controls(self),
			'render': Render(self, "Warrior")
		}
	
	def tick(self):
		for name, component in self.components.iteritems():
				component.tick()

class Assassin(object):
	def __init__(self, parent):
		position = (0,0,0)
		box = (2,2,2)
		self.components = {
			'physics': Physics(position),
			'collision': Collision(box),
			'render': Render("Assassin")
		}
	
	def tick(self):
		pass		

import yaml
class ResourcesClass(object):
	def __init__(self):
		self.data = {}
		self.all_data = yaml.load( file('../data/resources.yaml') )
	
	def __getitem__(self, x):
		if x not in self.data:
			self.data[x] = self.all_data.__getitem__(x)
		return self.data[x]

Resources = ResourcesClass()




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
		return str(u) + "," + str(v)
	def body_center(self):
		u = self.x - self.width/2
		v = self.y - self.height/2
		return str(u) + "," + str(v)"""

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
		
    out = numpy.dot(camera_matrix, position+[1] )
    for i in range(len(out)):
        out[i] /= out[3]
    out[0] *= window_size_h
    out[1] *= window_size_v
    out[0] += window_size_h/2
    out[1] += window_size_v/2
    out2 = ( int(out[0]), int(out[1]) )
    return out2


class Player(Being):
    """ """

    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.time_anim = 0
        self.time_anim_temp = 0
        self.framepos = 0
        self.frameposjump = 0
        self.position = (0,0,0)
        self.velocity = (0,0,0)
        self.pressed_keys = []
        self.player_image = pygame.image.load(os.path.join('..', 'data', 'sprites', 'classes', 'player_anim.png'))
        self.jumping = False
        self.velocity_up = 0

    def draw(self):
        # this resets the 3D velocity tuple
        self.velocity = (0,0,0)
        # this looks for any key that has been pressed that is used for 2D movement and adds its tuple to the velocity to get the sum of the velocities
        for key in self.pressed_keys:
            if key is not K_SPACE:
                self.velocity = tuple(map(add,self.velocity,self.keys[key]))

        #edges = [list(pos_to_2d( (-250,0,-250) )), list(pos_to_2d( (250,0,-250) )), list(pos_to_2d( (250,0,250) )), list(pos_to_2d( (-250,0,250) )) ]
        pygame.draw.polygon(screen, (0,0,255), edges )

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
            #screen.blit(self.player_image, pos_to_2d(self.position), (0,self.height*self.character_sprites[self.velocity],self.width,self.height) )
			pass
        # if it is not, sets the character's sprite to the corresponding animation sprite
        else:
            #screen.blit(self.player_image, pos_to_2d(self.position), (self.framepos,self.height*self.character_sprites[self.velocity],self.width,self.height) )
			pass

        # if jumping, sets the character's sprite to the corresponding jumping animation sprite
        if self.jumping == False:
            self.frameposjump = 0
        # copies the temporary value to the actual value for animation purposes, so they are equal again for the time specified in MS_PER_FRAME and the frames don't change
        elif self.jumping == True:
            #screen.blit(self.player_image, pos_to_2d(self.position), (self.frameposjump,self.height*9,self.width,self.height) )
			pass

        self.time_anim = self.time_anim_temp


    def move(self):
            self.position = tuple(map(add, self.position, self.velocity)) # Add movement to position

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

# this is the star class for various stars
class Star(Being):
    def __init__(self):
        self.angle = 0
        self.angle_actual = 0
        self.angle_initial = 150
    def increment_angle(self):
        self.angle = sun_loop(self.angle)
        # division by 100 because we are getting a result in 100ths of degree from the polling
        self.angle_actual = (self.angle_initial+float(float(self.angle)/100.0))%360
    def tick(self):
        super(self.__class__, self).tick()
        self.increment_angle()
        
# this is the shadow class for various shadows
class Shadow(Being):
    def __init__(self,owner,owner_string,source):
        self.shadow_image = pygame.image.load(os.path.join('..', 'data', 'sprites', 'shadows', owner_string+'_shadow.png'))
        self.owner = owner
        self.source = source
        self.height = owner.width/4
        
    def update_pos(self,owner,source):
        self.position_3d = owner.position
        self.position_3d_list = list(self.position_3d)
        self.owner_position_list = list(owner.position)
        self.position_3d_list[1] = 0
        if source.angle_actual >=0.0 and source.angle_actual <=90.0:
            try:
                self.position_3d_list[0] = self.owner_position_list[0]-self.owner_position_list[1]*(math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180))
            except ArithmeticError:
                self.position_3d_list[0] = self.owner_position_list[0]-10000
        elif source.angle_actual >90.0 and source.angle_actual <=180.0:
            try:
                self.position_3d_list[0] = self.owner_position_list[0]+self.owner_position_list[1]*abs((math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180)))
            except ArithmeticError:
                self.position_3d_list[0] = self.owner_position_list[0]+10000
        self.position_3d = tuple(self.position_3d_list)
        
        #self.position = pos_to_2d(self.position_3d)
        self.position_list = list(self.position)
        if source.angle_actual >=0.0 and source.angle_actual <=90.0:    
            try:
                self.position_list[0] = self.position_list[0]-(owner.height*(math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180)))
            except ArithmeticError:
                 self.position_list[0] = self.position_list[0]-10000
        elif source.angle_actual >90.0 and source.angle_actual <=180.0:
            pass
        self.position_list[1] = self.position_list[1]+owner.height-self.height/2
        self.position = tuple(self.position_list)
    
    def update_scale(self,owner,source):
        #self.position = pos_to_2d(owner.position)
        if source.angle_actual >=0.0 and source.angle_actual <=90.0:
            try:
                self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (int(owner.width+owner.height*(math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180))),self.height))
            except:
                self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (10000,self.height))
        elif source.angle_actual >90.0 and source.angle_actual <=180.0:
            try:
                self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (int(owner.width+owner.height*abs(math.cos(source.angle_actual*PI/180)/math.sin(source.angle_actual*PI/180))),self.height))
            except:
                self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (10000,self.height))
        elif source.angle_actual >180.0:
            self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (0,0))
    def draw(self,*position):
        self.update_scale(self.owner,self.source)
        self.update_pos(self.owner,self.source)
        screen.blit(self.shadow_image_scaled, self.position)
    def tick(self):
        super(self.__class__, self).tick()
        self.draw()
        
class Enemy(Being):
    """ A class for the enemy. Will have to have some sort of AI. """

    def __init__(self,width,height):
        self.width = width
        self.height = height
        # initializes enemy sprite from file
        self.gui_item = pygame.image.load(os.path.join('..', 'data', 'sprites', 'bosses', 'boss.png'))
        # sets x and y position for enemy to random values within the window
        self.position = (random.randint(-100,100),random.randint(-100,100),random.randint(-100,100))
        #self.position = pos_to_2d(self.position)
    # draws enemy at (x,y) coordinates
    def draw(self,position):
      #screen.blit(self.gui_item, self.position)
	  pass

    def tick(self):
        super(self.__class__, self).tick()
        self.draw(self.position)


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
