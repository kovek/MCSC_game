# For now, the classes are in a file apart. It does not mean they will stay organized this way.
import pygame, sys, os
from pygame.locals import *
from operator import add
from math_functions import pos_to_2d, translate, scale, rotate
import numpy
import math
import random
import yaml
import copy

# Set up pygame, random number generator, font, colors and math constants
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
PI = math.pi

configs = yaml.load( file('../local/config.yaml') )
resolution = configs['options']['resolution']

default_height = 720.0
resolution_scale = resolution[1]/default_height
options_scale = configs['options']['scale_gui']

# Variables for target framerate, milliseconds per animation frame, jump speed
# of character, and time for 1 day (in ms = 6 min)
FRAMES_PER_SECOND = 500
MS_PER_FRAME = 200
JUMP_SPEED = 1.5
DAY_TIME = 360000

character_sprites = {
	(-1,0,1):	1,
	(1,0,1):	2,
	(-1,0,-1):	3,
	(1,0,-1):	4,
	(0,0,1):	5,
	(0,0,-1):	6,
	(-1,0,0):	7,
	(1,0,0):	8,
	(0,0,0):	9,
	(0,1,0):	0,
}

class Entity(object):
	def __getattribute__(self, name):
		try:
			return super(Entity, self).__getattribute__(name)
		except AttributeError:
			try:
				return Resources[super(Entity, self).__getattribute__("__class__").__name__].__getitem__(name)
			except KeyError:
				return Resources[super(Entity, self).__getattribute__("name")].__getitem__(name)
		except Exception as e:
			print "Exception: ", e

	def tick(self):
            for name, component in self.components.iteritems():
                component.tick()
        # Note: Maybe count how many times each `name` has been queried for.
        # If the count is high enough, add the attribute as one of the object's if
        # the object does not have that attribute already


class Render(object):
    def __init__(self, parent, source):
        self.parent = parent
        self.source = source
        self.image = pygame.image.load(self.parent.spritesheet_file)
        self.which_frame = 0
        self.which_animation = 0
        self.dw = self.image.get_width()
        self.dh = self.image.get_height()

    def tick(self):
        self.which_frame = (pygame.time.get_ticks()//MS_PER_FRAME)%self.parent.num_of_frames

        velocity = self.parent.components['physics'].velocity
        if velocity[1] != 0:
            self.which_animation = character_sprites[ tuple( (0,1,0) ) ]
        else:
            self.which_animation = character_sprites[ tuple(velocity) ]


        position = self.parent.components['physics'].position

        offset = self.parent.offset
        num_of_frames = self.parent.num_of_frames
        num_of_animations = self.parent.num_of_animations

        frame_dimensions = (self.image.get_width()/num_of_frames, self.image.get_height()/num_of_animations)

        feet_point = pos_to_2d([position[0], 0, position[2]])
        head_point = pos_to_2d([position[0], self.parent.sprite_size[1], position[2]])
        h = self.parent.sprite_size[0]
        left = pos_to_2d([position[0] - h/2.0, 0.0, position[2]])
        right = pos_to_2d([position[0] + h/2.0, 0.0, position[2]])

        height = int(-(head_point[1] - feet_point[1]))
        width = int(-(left[0] - right[0]))

        cropped = pygame.Surface( frame_dimensions )
        cropped.blit(self.image, (0,0), (self.which_frame*frame_dimensions[0], self.which_animation*frame_dimensions[1], frame_dimensions[0], frame_dimensions[1] ))
        to_draw = pygame.transform.scale(cropped, (width, height))

        dimensions = (to_draw.get_width(), to_draw.get_height())

        point_on_screen = pos_to_2d(self.parent.components['physics'].position)
        screen.blit(to_draw,
                (point_on_screen[0]-dimensions[0]*offset[0], point_on_screen[1]-dimensions[1]*offset[1])
        )

class Physics(object):
	def __init__(self, parent, position, velocity=[0,0,0] ):
		self.parent = parent
		self.position = position

                # If we do not use copy, self.velocity will always
                # refer to the same list in memory, no matter from
                # which object it is referred.
		self.velocity = copy.copy(velocity)

	def tick(self):
		for i in xrange(3):
			self.position[i] += self.velocity[i]

		# Bounds of battlefield
		if self.position[0] < -250: self.position[0] = -250
		if self.position[0] > 250: self.position[0] = 250
		if self.position[1] < 0:
			self.position[1] = 0
			self.velocity[1] = 0
		if self.position[2] > 250: self.position[2] = 250
		if self.position[2] < -250: self.position[2] = -250

		# Acceleration of gravity
		if self.position[1] != 0:
			self.velocity[1] = self.velocity[1] -6.8*1/FRAMES_PER_SECOND


class PhysicsEngine(object):
	things_on_field = []

import itertools
class Collision(object):
	def __init__(self, parent, source):
		self.parent = parent
		self.source = source

		# Needed to find all 8 corners of a box around a point
		self.permutations = [
			[1,1,1], # 0
			[-1,-1,-1],
			[-1,1,1],
			[-1,-1,1],
			[1,-1,-1], # 4
			[1,1,-1],
			[1,-1,1],
			[-1,1,-1] # 7
		]

	def tick(self):
                permutations = []
                for permut in self.permutations:
                    permutations.append( [permut[0]*10.0, permut[1]*20.0+20.0, permut[2]*10.0] )
                pygame.draw.line(screen, (255,0,0), pos_to_2d([0,0,0]), pos_to_2d([0,40.0,0]))
                #square right
                pygame.draw.line(screen, (255,0,0), pos_to_2d(permutations[0]), pos_to_2d(permutations[5]) )
                pygame.draw.line(screen, (255,0,0), pos_to_2d(permutations[0]), pos_to_2d(permutations[6]) )
                pygame.draw.line(screen, (255,0,0), pos_to_2d(permutations[4]), pos_to_2d(permutations[6]) )
                pygame.draw.line(screen, (255,0,0), pos_to_2d(permutations[4]), pos_to_2d(permutations[5]) )

                pygame.draw.line(screen, (255,0,0), pos_to_2d(permutations[0]), pos_to_2d(permutations[2]) )
                pygame.draw.line(screen, (255,0,0), pos_to_2d(permutations[6]), pos_to_2d(permutations[3]) )
                pygame.draw.line(screen, (255,0,0), pos_to_2d(permutations[5]), pos_to_2d(permutations[7]) )
                pygame.draw.line(screen, (255,0,0), pos_to_2d(permutations[4]), pos_to_2d(permutations[1]) )

                # square left
                pygame.draw.line(screen, (255,0,0), pos_to_2d(permutations[3]), pos_to_2d(permutations[1]) )
                pygame.draw.line(screen, (255,0,0), pos_to_2d(permutations[3]), pos_to_2d(permutations[2]) )
                pygame.draw.line(screen, (255,0,0), pos_to_2d(permutations[7]), pos_to_2d(permutations[2]) )
                pygame.draw.line(screen, (255,0,0), pos_to_2d(permutations[7]), pos_to_2d(permutations[1]) )

		bounds = self.parent.box_size
		offset = self.parent.box_offset
		position = self.parent.components['physics'].position

		# We should not compute this for every tick. We should somehow fit that back into Resources so
		# that it could be used later.
		x_bounds = (position[0] - bounds[0]/2.0 + offset[0] * bounds[0],
					position[0] + bounds[0]/2.0 + offset[0] * bounds[0])
		y_bounds = (position[1] - bounds[1]/2.0 + offset[1] * bounds[1],
					position[1] + bounds[1]/2.0 + offset[1] * bounds[1])
		z_bounds = (position[2] - bounds[2]/2.0 + offset[2] * bounds[2],
					position[2] + bounds[2]/2.0 + offset[2] * bounds[2])

		list_of_colliding_with_self = []
		for item in PhysicsEngine.things_on_field:
			if item is self.parent:
				continue

			try:
				physics_component = item.components['physics']
			except Exception:
				continue

			if type(item) == RagdollBoss and type(self.parent) == Warrior:
				pass

			item_position = item.components['physics'].position
			box_size = item.box_size
			points = []

			for corner in self.permutations:
				points.append( [
					item_position[0] + 1/2.0 * corner[0] * box_size[0],
					item_position[1] + 1/2.0 * corner[1] * box_size[1],
					item_position[2] + 1/2.0 * corner[2] * box_size[2],
				] )

                        # If we don't use this, there will be a collision for
                        # every point inside the bounds
                        stop_comparing_points = False

			for point in points:
                                if stop_comparing_points: break
				if x_bounds[0] < point[0] < x_bounds[1]:
					if y_bounds[0] < point[1] < y_bounds[1]:
						if z_bounds[0] < point[2] < z_bounds[1]:
                                                        stop_comparing_points = True
							list_of_colliding_with_self.append(item)

		for item in list_of_colliding_with_self:
			fn = CollisionsPossible.collision(self.parent.name, item.name)
                        if type(fn) is None: (self.parent, item)

class CollisionsPossibleClass(object):
	def __init__(self):
		pass

	def __getitem__(self, name):
		return getattr(self, name)

	def collision(self, one, two):
		key = str(one) + '_with_' + str(two)
		if key in dir(self):
			return self[key]

	def Tree_with_Player(self, tree, player):
		print 'tree gives shadow to player'

	def Wall_with_Player(self, wall, player):
		return
		# Push the character off

		# k is the distance we have to push the player off
		k = numpy.dot(player.components['physics'].position, wall.direction) +\
			numpy.dot(player.components['collision'].box_size, wall.direction)/2.0 -\
			(numpy.dot(wall.components['physics'].position, wall.direction) -\
			numpy.dot(wall.components['collision'].box_size, wall.direction)/2.0)

		player.components['physics'].position = map(add,
			player.components['physics'].position,
			[x* (k) for x in wall.direction] )

	def RagdollBoss_with_Warrior(self, boss, player):
		print "Player looks at Ragdoll awkwardly"
CollisionsPossible = CollisionsPossibleClass()

class Battlefield(object):
	def __init__(self):
		pass

	def tick(self):
		edges = [list(pos_to_2d( [-250,0,-250] )), list(pos_to_2d( [250,0,-250] )), list(pos_to_2d( [250,0,250] )), list(pos_to_2d( [-250,0,250] )) ]
		pygame.draw.polygon(screen, (0,0,255), edges )


class Controls(object):
	def __init__(self, parent):
		self.parent = parent
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

		self.parent.components['physics'].velocity[0] = 0
		self.parent.components['physics'].velocity[2] = 0
		for key in self.pressed_keys:
			if key in [K_w, K_a, K_s, K_d]:
				self.parent.components['physics'].velocity = map(add, self.parent.components['physics'].velocity, self.keys[key])
			elif key is K_SPACE:
				if self.parent.components['physics'].velocity[1] is 0:
					self.parent.components['physics'].velocity[1] = 1
			else:
				pass

	def key_event(self, event):
		if event.type == KEYDOWN:
			if event.key in self.keys:
				self.pressed_keys.append(event.key)
		elif event.type == KEYUP:
			if event.key in self.pressed_keys:
				self.pressed_keys.remove(event.key)

class FightingStats(object):
	def __init__(self, parent):
                self.health = 0
                self.mana = 0
                self.regeneration = 0

class Warrior(Entity):
	def __init__(self):
		position = [0,0,0]
		self.name = "Warrior"
                some_star = Star()

		self.components = {
			'physics': Physics(self, position),
			'collision': Collision(self, "Warrior"),
			'controls': Controls(self),
			'render': Render(self, "Warrior"),
			'shadow': Shadow(self, "player", some_star),
		}


class Assassin(Entity):
	def __init__(self, parent):
		position = (0,0,0)
		box = (2,2,2)
		self.components = {
			'physics': Physics(position),
			'collision': Collision(box),
			'render': Render("Assassin")
		}

class RagdollBoss(Entity):
	def __init__(self):
		self.name = "RagdollBoss"
		position = [50,0,50]
		self.components = {
			'physics': Physics(self, position),
			'collision': Collision(self, "RagdollBoss"),
			'render': Render(self, "RagdollBoss")
		}


def call_super(func, cls):
    def wrapped(self, *args, **kwargs):
        super(cls, self).__getattribute__(func.__name__)(self, *args, **kwargs)
        func(self, *args, **kwargs)
    return wrapped


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



class Player(object):
    """ """

    def __init__(self,width,height):
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

# This is the star class for various stars
class Star(object):
    def __init__(self):
        self.angle = 0

    def tick(self):
        # Divide by MS_PER_FRAME because we are getting huge numbers because of polling
        self.angle = (pygame.time.get_ticks()//MS_PER_FRAME)\
            //(DAY_TIME/36000)\
            % 360 # Reset when angle reaches 360

# This is the shadow class for various shadows
class Shadow(object):
    def __init__(self, owner, owner_string, source):
        self.shadow_image = pygame.image.load(os.path.join('..', 'data', 'sprites', 'shadows', owner_string+'_shadow.png'))
        self.owner = owner
        self.source = source
        self.height = owner.sprite_size[0]/4

    def update_pos(self, owner, source):
        self.position =  owner.components['physics'].position[:]
        self.owner_position = owner.components['physics'].position[:]
        self.position[1] = 0
        angle = copy.copy(source.angle)

        if 0 <= angle < 3:
            angle = 3.0
        if 177 < angle <= 180:
            angle = 177.0

        push_back = self.owner_position[1]*((math.cos(angle*PI/180)/math.sin(angle*PI/180)))
        self.position[0] = self.owner_position[0]-push_back

        # Offset
        if 0.0 <= angle <= 90.0:
            self.position[0] = self.position[0]-(owner.sprite_size[1]*(math.cos(angle*PI/180)/math.sin(angle*PI/180)))

        self.position[1] = self.position[1]+owner.sprite_size[1]-self.height/2

    def update_scale(self, owner, source):
        angle = copy.copy(source.angle)
        if 0 <= angle < 3:
            angle = 3.0
        if 177 < angle <= 180:
            angle = 177.0
        self.shadow_image_scaled = pygame.transform.smoothscale(
            self.shadow_image,
            (int(owner.sprite_size[0]+owner.sprite_size[1]*abs(math.cos(angle*PI/180)/math.sin(angle*PI/180))), self.height))
        if angle > 180.0:
            self.shadow_image_scaled = pygame.transform.smoothscale(self.shadow_image, (0,0))

    def draw(self,*position):
        self.update_scale(self.owner, self.source)
        self.update_pos(self.owner, self.source)
        screen.blit(self.shadow_image_scaled, pos_to_2d(self.position))

    def tick(self):
        self.draw()
