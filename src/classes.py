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
from copy import copy
import pdb
import numpy.ma.bench

# Set up pygame, random number generator, font, colors and math constants
pygame.init()
pygame.font.init()
random.seed()
screen = None
COMIC_SANS = os.path.join('..','data', 'comic.ttf')
myfont = pygame.font.Font(COMIC_SANS, 15)

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
    """ I System is a class that will control the logic of the different
    components in the running game. For example, the main game logic will call
    tick on CollisionManager, which will then inspect all of the collision boxes
    in game at that moment and figure out which ones collide with eachother.

    We require tick to be defined because that's how we get a System to run its
    logic"""

    @classmethod
    def tick(cls):
        # Each System should have a components attribute to then be able to
        # run some logic on them.
        if 'components' not in dir(cls):
            raise Exception('The system %s should have a .components attribute'\
            % (str(cls),) )
        raise Exception('The .tick() method for %s has not been implemented'\
        %(str(cls),))

class Component(object):
    """ A Component is just a container of information that is connected to a
    System which takes care of the logic for that component. The great thing is
    that those components can be plugged in and out of Entities.

    For example, you could have a Collision component in a Ragdoll Entity.
    The Collision component will also be connected the a collision system.
    The system will always check if the Collision component intersects with any
    other collision component in the game. If we want the Ragdoll to stop having
    a collision box, we just disconnect the Collision component from it and it
    will now not collide with anything anymore!
    """
    def __init__(self):
        pass

class RenderManager(System):
    """ This System draws components on screen. Right now, it only focuses on
    character or boss components. """

    components = set([])

    @classmethod
    def tick(cls):

        # We order the components so that the objects that are further away do
        # not appear in front of objects that are closer
        ordered = list(cls.components)
        ordered.sort(
            key = lambda x: x.parent.components['physics'].position[2],
            reverse=False)

        for item in ordered:
            cls.draw(item)

    @classmethod
    def draw(cls, item):

        # Go to the next frame in the animation
        item.which_frame = (pygame.time.get_ticks()//MS_PER_FRAME)%\
            item.parent.num_of_frames

        # Check if the character is jumping to give him the jumping animation.
        velocity = item.parent.components['physics'].velocity
        if velocity[1] != 0:
            item.which_animation = character_sprites[ tuple( (0,1,0) ) ]
        else:
            item.which_animation = character_sprites[ tuple(velocity) ]


        position = item.parent.components['physics'].position

        # An example of the use of the offset is to make the character appear
        # such that its position is at its feet
        offset = item.parent.offset

        num_of_frames = item.parent.num_of_frames
        num_of_animations = item.parent.num_of_animations

        # We have big image files that contain spritesheets.
        # These frame dimensions are the dimensions of one sprite on a
        # spritesheet
        frame_dimensions = (
            item.image.get_width()/num_of_frames,
            item.image.get_height()/num_of_animations)

        # We're using this to scale the image depending on its depth
        feet_point = pos_to_2d([position[0], 0, position[2]])
        head_point = pos_to_2d([
            position[0],
            item.parent.sprite_size[1],
            position[2]])

        h = item.parent.sprite_size[0]
        left = pos_to_2d([position[0] - h/2.0, 0.0, position[2]])
        right = pos_to_2d([position[0] + h/2.0, 0.0, position[2]])

        height = int(-(head_point[1] - feet_point[1]))
        width = int(-(left[0] - right[0]))
        item.scaled_size = [width, height]

        # We crop the frame out of the spritesheet to then transform it at our
        # will! It's useful if we want to take an animation of a char running
        # to the right and then transform it to run to the left
        cropped = pygame.Surface( frame_dimensions )
        cropped.blit(
            item.image,
            (0,0),
            (item.which_frame*frame_dimensions[0],
                item.which_animation*frame_dimensions[1],
                frame_dimensions[0],
                frame_dimensions[1] ))
        to_draw = pygame.transform.scale(cropped, (width, height))

        dimensions = (to_draw.get_width(), to_draw.get_height())

        point_on_screen = pos_to_2d(item.parent.components['physics'].position)
        screen.blit(
            to_draw,
            (point_on_screen[0]-dimensions[0]*offset[0],
                point_on_screen[1]-dimensions[1]*offset[1])
        )


class PhysicsManager(System):
    """ Manage the Physics of the components. Change their position depending
    on their velocity. Change their velocity depending on their acceleration."""

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
                component.velocity[1] = component.velocity[1] -\
                6.8*1/FRAMES_PER_SECOND

class CollisionsManager(System):
    """ Runs the logic behind collisions. """

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
            # For each component, we update its bounds
            position = component.parent.components['physics'].position
            offset = component.parent.box_offset
            bounds = component.parent.box_size

            component.bounds.x[0] = position[0] - bounds[0]/2.0 + offset[0] * bounds[0]
            component.bounds.x[1] = position[0] + bounds[0]/2.0 + offset[0] * bounds[0]
            component.bounds.y[0] = position[1] - bounds[1]/2.0 + offset[1] * bounds[1]
            component.bounds.y[1] = position[1] + bounds[1]/2.0 + offset[1] * bounds[1]
            component.bounds.z[0] = position[2] - bounds[2]/2.0 + offset[2] * bounds[2]
            component.bounds.z[1] = position[2] + bounds[2]/2.0 + offset[2] * bounds[2]

            # Completely just for debugging purposes
            lines = [(0,5), (0,6), (4,6), (4,5), (0,2), (6,3), (5,7), (4,1), (3,1), (3,2), (7,2), (7,1)]
            component_permutations = []
            for permut in cls.permutations:
                component_permutations.append([
                    (permut[0]+offset[0]*2)*bounds[0]/2.0+position[0],
                    (permut[1]+offset[1]*2)*bounds[1]/2.0+position[1],
                    (permut[2]+offset[2]*2)*bounds[2]/2.0+position[2]] )
            for line in lines:
                pygame.draw.line(screen, (255,0,0), pos_to_2d(component_permutations[line[0]]), pos_to_2d(component_permutations[line[1]]))

        for component in cls.components:
            list_of_colliding_with_component = []

            if isinstance(component.parent, Punch):
                pass
                #pdb.set_trace()
            for item in cls.components:
                if item is component:
                    continue

                if 'physics' not in item.parent.components:
                    continue

                # Make sure to check if collisions between the two Entities are
                # possible?
                # Check if the hitboxes intersect

                collision_string = component.parent.name + '_with_' + item.parent.name
                if collision_string not in dir(CollisionsPossible):
                    #print collision_string
                    continue

                def check():
                    if component.bounds.x[0] <= item.bounds.x[0] <= component.bounds.x[1]\
                    or component.bounds.x[0] <= item.bounds.x[1] <= component.bounds.x[1]:
                        if component.bounds.y[0] <= item.bounds.y[0] <= component.bounds.y[1]\
                        or component.bounds.y[0] <= item.bounds.y[1] <= component.bounds.y[1]:
                            if component.bounds.z[0] <= item.bounds.z[0] <= component.bounds.z[1]\
                            or component.bounds.z[0] <= item.bounds.z[1] <= component.bounds.z[1]:
                                if isinstance(item.parent, Punch) or isinstance(component.parent, Punch):
                                    pass
                                    #print 'here'
                                list_of_colliding_with_component.append(item)
                check()
                temp = copy(component.bounds)
                component.bounds = item.bounds
                item.bounds = temp
                check()
                temp = copy(component.bounds)
                component.bounds = item.bounds
                item.bounds = temp



            for item in list_of_colliding_with_component:
                fn = CollisionsPossible.collision(component.parent.name, item.parent.name)
                if type(fn) is not type(None):
                    fn(component.parent, item.parent)



class ShadowManager(System):
    """ Draws the shadows depending on where the Stars are located. """

    components = set([])

    @classmethod
    def update_pos(cls):
        for shadow in cls.components:

            # This is not useful at the moment.
            # Later on, we might make multiple shadows from multiple stars.
            for star in StarManager.components:
                shadow.position =  shadow.owner.components['physics'].position[:]
                shadow.owner_position = shadow.owner.components['physics'].position[:]
                shadow.position[1] = 0
                angle = copy(star.angle)

                # We don't want the shadow to stretch too much, or else pygame
                # wont draw it
                if 0 <= angle < 3:
                    angle = 3.0
                if 177 < angle <= 180:
                    angle = 177.0

                ratio = (math.cos(angle*math.pi/180)/math.sin(angle*math.pi/180))

                shadow.shadow_foot = shadow.position[:]
                shadow.shadow_head = shadow.position[:]

                # We're setting the position on the character from where the
                # shadow will generate.
                # In a 2D world, the shadow of a rectangle coming from a star on
                # the top right would come from the top left and bottom right
                # corners of a rectangle
                if 0 <= angle < 90:
                    shadow.shadow_foot[0] += (shadow.owner.sprite_size[0])/2.0
                    shadow.shadow_head[0] -= (shadow.owner.sprite_size[0])/2.0

                elif 90 <= angle <= 180:
                    shadow.shadow_foot[0] -= (shadow.owner.sprite_size[0])/2.0
                    shadow.shadow_head[0] += (shadow.owner.sprite_size[0])/2.0


                # Use trigonometry to figure out the x positions of the shadow
                # depending on the y positions of the corners
                shadow.shadow_foot[0] -= ratio * shadow.owner.components['physics'].position[1]
                shadow.shadow_head[0] -= ratio * (shadow.owner.components['physics'].position[1] + shadow.owner.sprite_size[1])

    @classmethod
    def update_scale(cls):
        for shadow in cls.components:
            for star in StarManager.components:
                width = abs(int(pos_to_2d( shadow.shadow_head )[0] - pos_to_2d( shadow.shadow_foot )[0]))
                shadow.size = [width, shadow.shadow_image.get_height()]

                if star.angle > 180.0:
                    # Don't draw the shadow
                    shadow.size = (0,0)

                shadow.shadow_image_scaled = pygame.transform.smoothscale(copy(shadow.shadow_image), tuple(shadow.size))


    @classmethod
    def draw(cls,*position):
        cls.update_pos()
        cls.update_scale()
        for shadow in cls.components:
            for star in StarManager.components:
                position = list(pos_to_2d( shadow.shadow_foot ))
                if star.angle < 90.0:
                    position[0] -= shadow.size[0]
                position[1] -= shadow.size[1]/2.0
                position = tuple(position)

                screen.blit(shadow.shadow_image_scaled, position)

    @classmethod
    def tick(cls):
        cls.draw()

class ControlsManager(System):
    """ Manage the keys that are pressed by the user.
    The Controls component will be connected to the Entity the player is playing
    """

    components = set([])
    pressed_keys = []

    keys = {
        K_w: [0,0,-1],
        K_a: [-1,0,0],
        K_s: [0,0,1],
        K_d: [1,0,0],
        K_SPACE: [0,0,0],
        K_q: "punch..."
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
                # Make a mechanism so that there are not a punch created at
                # every tick! There should be a delay!
                Punch(item.parent)
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

class TimeoutManager(System):
    """ This System will basically take care of 'ticking bombs'. When necessary,
    a component will be created whose action will trigger after a specified
    amount of time."""

    components = set([])

    @classmethod
    def tick(cls):
        to_trigger = []
        current = pygame.time.get_ticks()

        for timeout in cls.components:
            if timeout.initial_time + timeout.duration < current:
                to_trigger.append(timeout)

        for timeout in to_trigger:
            timeout.trigger()

            # Remove it from the manager
            cls.components.remove(timeout)

            # Remove it
            del timeout


class Timeout(Component):
    """ This component's trigger function will be called after the specified
    duration has elapsed. """

    def __init__(self, target, duration, trigger):
        self.duration = duration
        self.initial_time = pygame.time.get_ticks()
        self.trigger = trigger

        TimeoutManager.components.add(self)

class StarManager(System):
    """ This System rotates the stars around the world. """
    components = set([])

    @classmethod
    def tick(cls):
        for star in cls.components:

            # Divide by MS_PER_FRAME because we are getting huge numbers because of polling
            star.angle = (pygame.time.get_ticks()//MS_PER_FRAME)\
                //(DAY_TIME/360000)\
                % 360 # Reset when angle reaches 360

class Entity(object):
    """ An Entity is just going to be an object that will contain a variable
    number of components plugged into it.
    For example, you could have an Entity with the components: collision, physics,
    render, and controls, which would respectively take care of the entity's
    collision detection, movement, drawing on screen and control by the player. """

    # When we do my_entity.some_attribute, if the attribtue is not already
    # specified in the object, we will look inside the Resources that are loaded
    # for that attribute.
    def __getattribute__(self, name):
        try:
            return super(Entity, self).__getattribute__(name)
        except AttributeError:
            try:
                the_value = Resources[super(Entity, self).__getattribute__("__class__").__name__].__getitem__(name)
            except KeyError:
                try:
                    the_value = Resources[super(Entity, self).__getattribute__("name")].__getitem__(name)
                except AttributeError:
                    return
            self.__setattr__(name, the_value)
            return the_value
        except Exception as e:
            print "Exception: ", e


class Render(Component):
    """ Component needed to draw a character or boss. """
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

class Physics(Component):
    """ Component needed to take care of the physics of the Entity """
    def __init__(self, parent, position, velocity=[0,0,0] ):
        self.parent = parent
        self.position = position

        # If we do not use copy, self.velocity will always
        # refer to the same list in memory, no matter from
        # which object it is referred.
        self.velocity = copy(velocity)

        PhysicsManager.components.add(self)

class Bunch(object):
    pass

import itertools
class Collision(Component):
    def __init__(self, parent, source):
        self.parent = parent
        self.source = source
        self.points = [[0,0,0] for i in xrange(8)]
        self.bounds = Bunch()
        self.bounds.x = [0,0]
        self.bounds.y = [0,0]
        self.bounds.z = [0,0]
        self.box_size = self.parent.box_size

        CollisionsManager.components.add(self)


class Punch(Entity):
    def __init__(self, parent):
        self.parent = parent
        self.name = "Punch"

        def destroy_self(self=self):
            for key, val in self.parent.components.iteritems():
                if val is self:
                    del self.parent[key]
            CollisionsManager.components.remove(self.components['collision'])
            del self.components['collision']
            del self

        position = copy(self.parent.components['physics'].position)
        direction_facing = 1
        position[0] += direction_facing * parent.box_size[0]/2.0
        position[1] += parent.box_size[1]-10.0

        physics = Component()
        physics.position = position

        self.components = {
            'timeout': Timeout(self, 0, destroy_self),
            'collision': Collision(self, "punch"),
            'physics': physics
        }

        #self.components['collision'].position += [direction*offset, height, 0]

class Punch(Entity):
    def __init__(self, parent):
        self.parent = parent
        self.name = "Punch"

        def destroy_self(self=self):
            for key, val in self.parent.components.iteritems():
                if val is self:
                    del self.parent[key]
            CollisionsManager.components.remove(self.components['collision'])
            del self.components['collision']
            del self

        position = copy(self.parent.components['physics'].position)
        direction_facing = 1
        position[0] += direction_facing * parent.box_size[0]/2.0
        position[1] += parent.box_size[1]-10.0

        physics = Component()
        physics.position = position

        self.components = {
            'timeout': Timeout(self, 0, destroy_self),
            'collision': Collision(self, "punch"),
            'physics': physics
        }

        #self.components['collision'].position += [direction*offset, height, 0]


class CollisionsPossibleClass(object):
    def __getitem__(self, name):
        return getattr(self, name)

    def collision(self, one, two):
        key = str(one) + '_with_' + str(two)
        second_key = str(two) + '_with_' + str(one)

        if one == "Punch" or two == "Punch":
            print 'here'

        print key
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

    def Punch_with_RagdollBoss(self, punch, boss):
        print 'Warrior punched ragdoll!'
        boss.components['stats'].health -= 0.1
        if boss.components['stats'].health <= 0.0:
            boss.components['stats'].health = 0.0

# I'm just doing this so that we do not need to wrap every method with @classmethod
CollisionsPossible = CollisionsPossibleClass()


class Battlefield(object):
    @classmethod
    def tick(cls):
        edges = [list(pos_to_2d( [-250,0,-250] )), list(pos_to_2d( [250,0,-250] )), list(pos_to_2d( [250,0,250] )), list(pos_to_2d( [-250,0,250] )) ]
        pygame.draw.polygon(screen, (0,0,255), edges )


class Controls(Component):
    def __init__(self, parent):
        self.parent = parent
        self.pressed_keys = []

        ControlsManager.components.add(self)

class FightingStats(Component):
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
            'stats': FightingStats(self),
        }


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

class Star(Component):
    """ This is the star class for various stars """

    def __init__(self):
        self.angle = 0
        StarManager.components.add(self)


class Shadow(Component):
    """ This is the shadow class for various shadows. """

    def __init__(self, owner, owner_string):
        self.shadow_image = pygame.image.load(os.path.join('..', 'data', 'sprites', 'shadows', owner_string+'_shadow.png'))
        self.owner = owner
        self.height = owner.sprite_size[0]/4
        ShadowManager.components.add(self)
