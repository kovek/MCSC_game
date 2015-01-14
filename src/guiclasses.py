from __future__ import absolute_import
from classes import Entity
import pygame, sys, os
from classes import Resources, resolution_scale, options_scale, resolution, System

class GUIManager(System):
    components = set([])
    pass

class GUIContainer(Entity):
	def __init__(self, main_char, **kwargs):
                # kwargs is to link additional characters' health & mana bars.

		self.components = {
                    #'health': GUIItem('health'),
                    'mana': GUIItem('mana'),
                    'LH': GUIItem('LH'),
		}


class GUIBackground(object):
	def __init__(self, parent):
            self.parent = parent
            self.image = pygame.transform.scale(
                pygame.image.load(
                    file( os.path.join(*Resources['GUI'][parent.name]['background_img']) )),
                tuple(Resources['GUI'][self.parent.name]['dimensions']) )

            self.image = pygame.transform.scale(
                self.image,
                (int(resolution_scale * options_scale * self.image.get_width()),
                    int(resolution_scale * options_scale * self.image.get_height())) )

        def tick(self):
            gui_resources = Resources['GUI'][self.parent.name]
            position_on_img = gui_resources['point_to_img']
            position_on_screen = gui_resources['point_to_screen']

            dimensions = gui_resources['dimensions']

            screen.blit(self.image,
                (position_on_screen[0] * resolution[0] - position_on_img[0] * self.image.get_width(),
                position_on_screen[1] * resolution[1] - position_on_img[1] * self.image.get_height()),
            )

class GUIDynamicContent(object):
	def __init__(self, parent):
            self.parent = parent
            self.image = pygame.transform.scale(
                pygame.image.load(
                    file( os.path.join( *Resources['GUI'][parent.name]['content_img'] ) ) ),
                tuple(Resources['GUI'][self.parent.name]['dimensions']))
            self.image = pygame.transform.scale(
                self.image,
                (int(resolution_scale * options_scale * self.image.get_width()),
                    int(resolution_scale * options_scale * self.image.get_height())) )

        def tick(self):
            gui_resource = Resources['GUI'][self.parent.name]
            position_on_img = gui_resource['point_to_img']
            position_on_screen = gui_resource['point_to_screen']

            dimensions = gui_resource['dimensions']

            k = 1.0
            if "linked_entity" in dir(self):
                k = self.linked_entity.components['stats'].health/\
                    self.linked_entity.components['stats'].max_health

            cropped = pygame.Surface( (self.image.get_width()*k, self.image.get_height()) )
            cropped.blit(self.image, (0,0))

            screen.blit(cropped,
                (position_on_screen[0] * resolution[0] - position_on_img[0] * dimensions[0] * options_scale * resolution_scale,
                position_on_screen[1] * resolution[1] - position_on_img[1] * dimensions[1] * options_scale * resolution_scale)
            )

class GUIBorder(object):
	def __init__(self, parent):
            self.parent = parent
            self.image = pygame.image.load(
                file( os.path.join( *Resources['GUI'][parent.name]['border_img']) ) )

            gui_resource = Resources['GUI'][self.parent.name]

            self.position_on_img = gui_resource['point_to_img']
            self.position_on_screen = gui_resource['point_to_screen']

            dimensions = gui_resource['dimensions']
            dimensions_scaled = [int(dimensions[0]*resolution_scale*options_scale),
                int(dimensions[1]*resolution_scale*options_scale)]

            position = (
                self.position_on_screen[0] * resolution[0] - self.position_on_img[0] * dimensions_scaled[0],
                self.position_on_screen[1] * resolution[1] - self.position_on_img[1] * dimensions_scaled[1])

            width_of_subsection = 1/3.0*self.image.get_width()
            height_of_subsection = 1/3.0*self.image.get_height()

            border_thickness = int(gui_resource['border_pct'] * dimensions[1])

            # Top border
            cropped_top_border = pygame.Surface(
                (width_of_subsection, height_of_subsection))
            cropped_top_border.blit(self.image,
                (0, 0),
                (width_of_subsection, 0.0,
                    width_of_subsection, height_of_subsection))
            cropped_top_border = pygame.transform.scale(cropped_top_border,
                (dimensions[0], border_thickness))

            # Bottom border
            cropped_bottom_border = pygame.Surface(
                (width_of_subsection, height_of_subsection))
            cropped_bottom_border.blit(self.image,
                (0, 0),
                (width_of_subsection, 2*height_of_subsection,
                    width_of_subsection, height_of_subsection))
            cropped_bottom_border = pygame.transform.scale(cropped_bottom_border,
                (dimensions[0], border_thickness))

            # Left border
            cropped_left_border = pygame.Surface(
                (width_of_subsection, height_of_subsection))
            cropped_left_border.blit(self.image,
                (0, 0),
                (0, height_of_subsection,
                    width_of_subsection, height_of_subsection))
            cropped_left_border = pygame.transform.scale(cropped_left_border,
                (border_thickness, dimensions[1]))

            # Right border
            cropped_right_border = pygame.Surface(
                (width_of_subsection, height_of_subsection))
            cropped_right_border.blit(self.image,
                (0, 0),
                (2*width_of_subsection, height_of_subsection,
                    width_of_subsection, height_of_subsection))
            cropped_right_border = pygame.transform.scale(cropped_right_border,
                (border_thickness, dimensions[1]))

            # Top Left Corner
            cropped_top_left_corner = pygame.Surface(
                (width_of_subsection, height_of_subsection))
            cropped_top_left_corner.blit(self.image,
                (0, 0),
                (0, 0, width_of_subsection, height_of_subsection))
            cropped_top_left_corner = pygame.transform.scale(cropped_top_left_corner,
                (border_thickness, border_thickness))

            # Top Right Corner
            cropped_top_right_corner = pygame.Surface(
                (width_of_subsection, height_of_subsection))
            cropped_top_right_corner.blit(self.image,
                (0, 0),
                (2*width_of_subsection, 0, width_of_subsection, height_of_subsection))
            cropped_top_right_corner = pygame.transform.scale(cropped_top_right_corner,
                (border_thickness, border_thickness))

            # Bottom Left Corner
            cropped_bottom_left_corner = pygame.Surface(
                (width_of_subsection, height_of_subsection))
            cropped_bottom_left_corner.blit(self.image,
                (0, 0),
                (0, 2*height_of_subsection, width_of_subsection, height_of_subsection))
            cropped_bottom_left_corner = pygame.transform.scale(cropped_bottom_left_corner,
                (border_thickness, border_thickness))

            # Bottom Right Corner
            cropped_bottom_right_corner = pygame.Surface(
                (width_of_subsection, height_of_subsection))
            cropped_bottom_right_corner.blit(self.image,
                (0, 0),
                (2*width_of_subsection, 2*height_of_subsection, width_of_subsection, height_of_subsection))
            cropped_bottom_right_corner = pygame.transform.scale(cropped_bottom_right_corner,
                (border_thickness, border_thickness))

            final_gui_item = pygame.Surface( tuple(dimensions), pygame.SRCALPHA, 32)
            final_gui_item.blit(cropped_top_border, (border_thickness, 0) )
            final_gui_item.blit(cropped_bottom_border,
                (border_thickness, dimensions[1]-border_thickness) )
            final_gui_item.blit(cropped_left_border,
                (0, border_thickness) )
            final_gui_item.blit(cropped_right_border,
                (dimensions[0]-border_thickness, border_thickness) )

            final_gui_item.blit(cropped_top_left_corner,
                (0, 0) )
            final_gui_item.blit(cropped_top_right_corner,
                (dimensions[0]-border_thickness, 0) )
            final_gui_item.blit(cropped_bottom_left_corner,
                (0, dimensions[1]-border_thickness) )
            final_gui_item.blit(cropped_bottom_right_corner,
                (dimensions[0]-border_thickness, dimensions[1]-border_thickness) )

            self.final_gui_item = pygame.transform.scale(final_gui_item,
                tuple(dimensions_scaled))


        def tick(self):
            # Note: we still need to adjust the position

            screen.blit(self.final_gui_item,
                (self.position_on_screen[0] * resolution[0] - self.position_on_img[0] * self.final_gui_item.get_width(),
                self.position_on_screen[1] * resolution[1] - self.position_on_img[1] * self.final_gui_item.get_height()),
            )


class GUIItem(Entity):
	def __init__(self, name):
            self.name = name
            self.components = {
                'background': GUIBackground(self),
                'content': GUIDynamicContent(self),
                'border': GUIBorder(self),
            }
            GUIManager.components.add(self)

        def tick(self):
            self.components['background'].tick()
            self.components['content'].tick()
            self.components['border'].tick()

class PlayingGUI(Entity):
    components = {
        'health_bar': GUIItem('health'),
        'mana_bar': GUIItem('mana'),
        'boss_health': GUIItem('boss_health'),
        'left_hand': GUIItem('left_hand'),
        'right_hand': GUIItem('right_hand'),
        'spell1': GUIItem('spell1'),
        'spell2': GUIItem('spell2'),
        'spell3': GUIItem('spell3'),
        'spell4': GUIItem('spell4'),
    }

    @classmethod
    def tick(cls):
        for key, component in cls.components.iteritems():
            component.tick()

