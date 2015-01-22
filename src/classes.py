# For now, the classes are in a file apart. It does not mean they will stay organized this way.
# Day night (phases) system for calling .tick() on the system?
import pygame, sys, os
from pygame.locals import *
from operator import add
from math_functions import pos_to_2d, translate, scale, rotate
import numpy
import math
import random
import yaml
import copy
import pdb
import numpy.ma.bench

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
	(-1,0,1):	0,
	(1,0,1):	1,
	(-1,0,-1):	2,
	(1,0,-1):	3,
	(0,0,1):	4,
	(0,0,-1):	5,
	(-1,0,0):	6,
	(1,0,0):	7,
	(0,0,0):	8,
	(0,1,0):	9,
}

class System(object):
    @classmethod
    def tick(cls):
        if 'components' not in dir(cls):
            raise Exception('The system %s should have a .components attribute' % (str(cls),) )
        raise Exception('The .tick() method for %s has not been implemented' %(str(cls),))

class RenderManager(System):
    components = set([])

    @classmethod
    def tick(cls):
        ordered = list(cls.components)
        ordered.sort(
            key = lambda x: x.parent.components['physics'].position[2],
            reverse=False)

        for item in ordered:
            cls.draw(item)

    @classmethod
    def draw(cls, item):
        item.which_frame = (pygame.time.get_ticks()//MS_PER_FRAME)%item.parent.num_of_frames

        velocity = item.parent.components['physics'].velocity
        if velocity[1] != 0:
            item.which_animation = character_sprites[ tuple( (0,1,0) ) ]
        else:
            item.which_animation = character_sprites[ tuple(velocity) ]


        position = item.parent.components['physics'].position

        offset = item.parent.offset
        num_of_frames = item.parent.num_of_frames
        num_of_animations = item.parent.num_of_animations

        frame_dimensions = (item.image.get_width()/num_of_frames, item.image.get_height()/num_of_animations)

        feet_point = pos_to_2d([position[0], 0, position[2]])
        head_point = pos_to_2d([position[0], item.parent.sprite_size[1], position[2]])
        h = item.parent.sprite_size[0]
        left = pos_to_2d([position[0] - h/2.0, 0.0, position[2]])
        right = pos_to_2d([position[0] + h/2.0, 0.0, position[2]])

        height = int(-(head_point[1] - feet_point[1]))
        width = int(-(left[0] - right[0]))
        item.scaled_size = [width, height]

        cropped = pygame.Surface( frame_dimensions )
        cropped.blit(item.image, (0,0), (item.which_frame*frame_dimensions[0], item.which_animation*frame_dimensions[1], frame_dimensions[0], frame_dimensions[1] ))
        to_draw = pygame.transform.scale(cropped, (width, height))

        dimensions = (to_draw.get_width(), to_draw.get_height())

        point_on_screen = pos_to_2d(item.parent.components['physics'].position)
        screen.blit(to_draw,
                (point_on_screen[0]-dimensions[0]*offset[0], point_on_screen[1]-dimensions[1]*offset[1])
        )


class PhysicsManager(System):
    components = set([])

    @classmethod
    def tick(cls):
        for component in cls.components:
            for i in xrange(3):
                component.position[i] += component.velocity[i]

            # Bounds of battlefield
            if component.position[0] < -250: component.position[0] = -250
            if component.position[0] > 250: component.position[0] = 250
            if component.position[1] < 0:
                component.position[1] = 0
                component.velocity[1] = 0
            if component.position[2] > 250: component.position[2] = 250
            if component.position[2] < -250: component.position[2] = -250

            # Acceleration of gravity
            if component.position[1] != 0:
                component.velocity[1] = component.velocity[1] -6.8*1/FRAMES_PER_SECOND

class CollisionsManager(System):
    components = set([])

    # Needed to find all 8 corners of a box around a point
    permutations = [
            [1,1,1], # 0
            [-1,-1,-1],
            [-1,1,1],
            [-1,-1,1],
            [1,-1,-1], # 4
            [1,1,-1],
            [1,-1,1],
            [-1,1,-1] # 7
    ]


    @classmethod
    def tick(cls):
        list_of_checked_component_pairs = []

        for component in cls.components:
            position = component.parent.components['physics'].position
            offset = component.parent.box_offset
            bounds = component.parent.box_size

            component.x_bounds[0] = position[0] - bounds[0]/2.0 + offset[0] * bounds[0]
            component.x_bounds[1] = position[0] + bounds[0]/2.0 + offset[0] * bounds[0]
            component.y_bounds[0] = position[1] - bounds[1]/2.0 + offset[1] * bounds[1]
            component.y_bounds[1] = position[1] + bounds[1]/2.0 + offset[1] * bounds[1]
            component.z_bounds[0] = position[2] - bounds[2]/2.0 + offset[2] * bounds[2]
            component.z_bounds[1] = position[2] + bounds[2]/2.0 + offset[2] * bounds[2]


        for component in cls.components:
            permutations = []

            bounds = component.parent.box_size
            offset = component.parent.box_offset
            position = component.parent.components['physics'].position

            # We should not compute this for every tick. We should somehow fit that back into Resources so
            # that it could be used later.
            list_of_colliding_with_component = []

            for item in cls.components:
                if item is component:
                    continue

                if 'physics' not in item.parent.components:
                    continue

                if component.x_bounds[0] <= item.x_bounds[0] <= component.x_bounds[1]\
                or component.x_bounds[0] <= item.x_bounds[1] <= component.x_bounds[1]:
                    if component.y_bounds[0] <= item.y_bounds[0] <= component.y_bounds[1]\
                    or component.y_bounds[0] <= item.y_bounds[1] <= component.y_bounds[1]:
                        if component.z_bounds[0] <= item.z_bounds[0] <= component.z_bounds[1]\
                        or component.z_bounds[0] <= item.z_bounds[1] <= component.z_bounds[1]:
                            list_of_colliding_with_component.append(item)

            for item in list_of_colliding_with_component:
                fn = CollisionsPossible.collision(component.parent.name, item.parent.name)
                if type(fn) is not type(None):
                    fn(component.parent, item.parent)




class ShadowManager(System):
    components = set([])

    @classmethod
    def update_pos(cls):
        for shadow in cls.components:
            for star in StarManager.components:
                shadow.position =  shadow.owner.components['physics'].position[:]
                shadow.owner_position = shadow.owner.components['physics'].position[:]
                shadow.position[1] = 0
                angle = copy.copy(star.angle)

                if 0 <= angle < 3:
                    angle = 3.0
                if 177 < angle <= 180:
                    angle = 177.0

                ratio = (math.cos(angle*PI/180)/math.sin(angle*PI/180))

                shadow.shadow_foot = shadow.position[:]
                shadow.shadow_head = shadow.position[:]

                if 0 <= angle < 90:
                    shadow.shadow_foot[0] += (shadow.owner.sprite_size[0])/2.0
                    shadow.shadow_head[0] -= (shadow.owner.sprite_size[0])/2.0

                elif 90 <= angle <= 180:
                    shadow.shadow_foot[0] -= (shadow.owner.sprite_size[0])/2.0
                    shadow.shadow_head[0] += (shadow.owner.sprite_size[0])/2.0


                shadow.shadow_foot[0] -= ratio * shadow.owner.components['physics'].position[1]
                shadow.shadow_head[0] -= ratio * (shadow.owner.components['physics'].position[1] + shadow.owner.sprite_size[1])

    @classmethod
    def update_scale(cls):
        for shadow in cls.components:
            for star in StarManager.components:
                angle = copy.copy(star.angle)

                if 0 <= angle < 3:
                    angle = 3.0
                if 177 < angle <= 180:
                    angle = 177.0

                width = abs(int(pos_to_2d( shadow.shadow_head )[0] - pos_to_2d( shadow.shadow_foot )[0]))
                shadow.size = (width, shadow.shadow_image.get_height())
                if angle > 180.0:
                    shadow.size = (0,0)

                shadow.shadow_image_scaled = pygame.transform.smoothscale(copy.copy(shadow.shadow_image), shadow.size)


    @classmethod
    def draw(cls,*position):
        cls.update_pos()
        cls.update_scale()
        for shadow in cls.components:
            for star in StarManager.components:
                position = pos_to_2d( shadow.shadow_foot )
                if star.angle < 90.0:
                    position = list(position)
                    position[0] -= shadow.size[0]
                    position = tuple(position)

                screen.blit(shadow.shadow_image_scaled, position)

    @classmethod
    def tick(cls):
        cls.draw()

class ControlsManager(System):
    components = set([])
    pressed_keys = []

    keys = {
        K_w: [0,0,-1],
        K_a: [-1,0,0],
        K_s: [0,0,1],
        K_d: [1,0,0],
        K_SPACE: [0,0,0]
    }

    @classmethod
    def tick(cls):
        # Handle keys
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
            cls.key_event(event)

        for item in cls.components:
            cls.move(item)

    @classmethod
    def move(cls, item):
        item.parent.components['physics'].velocity[0] = 0
        item.parent.components['physics'].velocity[2] = 0

        for key in cls.pressed_keys:
            if key in [K_w, K_a, K_s, K_d]:
                item.parent.components['physics'].velocity = map(add, item.parent.components['physics'].velocity, cls.keys[key])
            elif key is K_SPACE:
                if item.parent.components['physics'].velocity[1] is 0:
                    item.parent.components['physics'].velocity[1] = 1
            elif key is K_q:
                punch = Punch()
            else:
                pass

    @classmethod
    def key_event(cls, event):
        if event.type == KEYDOWN:
            if event.key in cls.keys:
                cls.pressed_keys.append(event.key)
        elif event.type == KEYUP:
            if event.key in cls.pressed_keys:
                cls.pressed_keys.remove(event.key)


class StarManager(System):
    components = set([])

    @classmethod
    def tick(cls):
        for star in cls.components:

            # Divide by MS_PER_FRAME because we are getting huge numbers because of polling
            star.angle = (pygame.time.get_ticks()//MS_PER_FRAME)\
                //(DAY_TIME/360000)\
                % 360 # Reset when angle reaches 360

class Entity(object):
	def __getattribute__(self, name):
            try:
                return super(Entity, self).__getattribute__(name)
            except AttributeError:
                try:
                    the_value = Resources[super(Entity, self).__getattribute__("__class__").__name__].__getitem__(name)
                except KeyError:
                    the_value = Resources[super(Entity, self).__getattribute__("name")].__getitem__(name)
                self.__setattr__(name, the_value)
                return the_value
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
        self.scaled_size = self.parent.sprite_size
        self.image = pygame.image.load(os.path.join(*self.parent.spritesheet_file))
        self.which_frame = 0
        self.which_animation = 0
        self.dw = self.image.get_width()
        self.dh = self.image.get_height()
        RenderManager.components.add(self)

class Physics(object):
    def __init__(self, parent, position, velocity=[0,0,0] ):
        self.parent = parent
        self.position = position

        # If we do not use copy, self.velocity will always
        # refer to the same list in memory, no matter from
        # which object it is referred.
        self.velocity = copy.copy(velocity)

        PhysicsManager.components.add(self)

import itertools
class Collision(object):
	def __init__(self, parent, source):
            self.parent = parent
            self.source = source
            self.points = [[0,0,0] for i in xrange(8)]
            self.x_bounds = [0,0]
            self.y_bounds = [0,0]
            self.z_bounds = [0,0]
            self.box_size = self.parent.box_size

            CollisionsManager.components.add(self)


class CollisionsPossibleClass(object):
	def __init__(self):
            pass

	def __getitem__(self, name):
            return getattr(self, name)

	def collision(self, one, two):
            key = str(one) + '_with_' + str(two)
            second_key = str(two) + '_with_' + str(one)

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
            player.components['stats'].health -= 0.1
            if player.components['stats'].health <= 0.0:
                player.components['stats'].health = 0.0

	def RagdollBoss_with_RagdollBoss(self, boss, player):
            print "Two ragdolls touch..."


CollisionsPossible = CollisionsPossibleClass()


class Battlefield(object):
    @classmethod
    def tick(cls):
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

        ControlsManager.components.add(self)

class FightingStats(object):
    def __init__(self, parent):
        self.health = 50.0
        self.max_health = 100.0
        self.mana = 0
        self.regeneration = 0

class Warrior(Entity):
    def __init__(self):
        position = [0,0,0]
        self.name = "Warrior"

        self.components = {
            'physics': Physics(self, position),
            'collision': Collision(self, "Warrior"),
            'controls': Controls(self),
            'render': Render(self, "Warrior"),
            'shadow': Shadow(self, "player"),
            'stats': FightingStats(self)
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
            'render': Render(self, "RagdollBoss"),
            'shadow': Shadow(self, "player"),
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

# This is the star class for various stars
class Star(object):
    def __init__(self):
        self.angle = 0
        StarManager.components.add(self)


# This is the shadow class for various shadows
class Shadow(object):
    def __init__(self, owner, owner_string):
        self.shadow_image = pygame.image.load(os.path.join('..', 'data', 'sprites', 'shadows', owner_string+'_shadow.png'))
        self.owner = owner
        self.height = owner.sprite_size[0]/4
        ShadowManager.components.add(self)
