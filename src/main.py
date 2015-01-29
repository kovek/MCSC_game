import pygame, sys, os
from pygame.locals import *
import classes
import yaml
import guiclasses
from constants import *
import levels


class Game(object):
    """ Main Game class """

    @classmethod
    def init(cls):
        """ Initiate all the main varaibles """

        cls.configs = yaml.load( file('../local/config.yaml') )
        cls.is_online = False
        cls.state = State.playing
        cls.classes = classes
        cls.guiclasses = guiclasses

        # set up pygame and init
        cls.pygame = pygame
        cls.pygame.init()

        # Set up the window
        cls.screen = pygame.display.set_mode(
            tuple(cls.configs['options']['resolution']),
            0,
            32)
        classes.screen = cls.screen
        guiclasses.screen = cls.screen


    @classmethod
    def run(cls):
        """ Run the game loop """

        while True:
            cls.screen.fill(BLACK)
            if cls.state == State.paused:
                # Don't move anything
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

                #classes.ConditionsManager.tick()

            pygame.display.update()

Game.init()
levels.Level1.init(Game)
Game.run()

