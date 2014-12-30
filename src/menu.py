import sys
import os
import yaml
from enum import Enum

sys.path.insert(0, '..')

import pygame
import gooeypy as gui
from gooeypy.const import *

class Online(object):
    @staticmethod
    def get_lan_rooms():
        return ['onelan', 'twolan', 'threelan', 'fourlan']
        pass

    @staticmethod
    def get_online_rooms():
        return ['oneonline', 'twoonline', 'threeonline']
        pass

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480), pygame.SRCALPHA)

app = gui.Container(width=640, height=480, surface=screen)

lan_rooms = []
online_rooms = []
game_saves = []


#THE LINK
def play():
    os.startfile("main.py")
    pygame.quit()
    quit()
    

active_menu = None
class Menus(gui.Container):
    def activate(self, which_menu):
        global game_saves
        global active_menu

        if which_menu == Const.QUIT:
            pygame.quit()
            sys.exit()
        for w in self.widgets:
            w.active = False
            if w == which_menu:
                w.active = True
                active_menu = w

        if which_menu == single_player_menu:
            save_file = open(os.path.join('..', 'local', 'saves.yaml'))
            save_file_map = yaml.safe_load(save_file)

            # Clean up
            for save in game_saves:
                try:
                    menus.remove(save)
                except ValueError: pass

            for button in single_player_menubar.widgets[:]:
                single_player_menubar.remove(button)

            saves = []

            i = 0
            for save in save_file_map['saves']:
                i += 1
                print save

                # Create menu
                temp_menu = gui.Container(width=640, height=480)
                menus.add(temp_menu)

                # Create button
                temp_button = gui.Button("Save "+str(i))
                temp_button.connect(CLICK, menus.activate,temp_menu)

                single_player_menubar.add(temp_button)

                saves.append(temp_menu)

            new_button = gui.Button("New Save")
            new_button.connect(CLICK, menus.activate, new_game_menu)
            single_player_menubar.add(new_button)
            single_player_menubar2.add(exit_single_player_button)




menus = Menus(width=640, height=480)
app.add(menus)

Const = Enum('Const', 'QUIT')


mainmenu = gui.Container(width=640, height=480)
credits_menu = gui.Container(width=640, height=480)
play_menu = gui.Container(width=640, height=480)
single_player_menu = gui.Container(width=640, height=480)
multiplayer_menu = gui.Container(width=640, height=480)
lan_menu = gui.Container(width=640, height=480)
online_menu = gui.Container(width=640, height=480)
save1_menu = gui.Container(width=640, height=480)
are_you_sure_menu = gui.Container(width=640, height=480)
replay_menu = gui.Container(width=640, height=480)
options_menu = gui.Container(width=640, height=480)
room_menu = gui.Container(width=640, height=480)
new_game_menu = gui.Container(width=640, height=480)






### Main Menu


play_button = gui.Button("Play")
play_button.connect(CLICK, menus.activate, play_menu)

options_button = gui.Button("Options")
options_button.connect(CLICK, menus.activate, options_menu)

credits_button = gui.Button("Credits")
credits_button.connect(CLICK, menus.activate, credits_menu)

quit_button = gui.Button("Quit")
quit_button.connect(CLICK, menus.activate, Const.QUIT)

mainmenu_menubar = gui.VBox(align="center", valign="center", y=0, spacing=20)
mainmenu_menubar.add(play_button, options_button, credits_button, quit_button)

mainmenu.add(mainmenu_menubar)

### Credits


exit_credits_button = gui.Button("Back", align="left", valign="bottom", x=10, y=-10)
exit_credits_button.connect(CLICK, menus.activate, mainmenu)

credits_menu.add(exit_credits_button)


### Play


single_player_button = gui.Button("Single Player")
single_player_button.connect(CLICK, menus.activate, single_player_menu)

multiplayer_button = gui.Button("Multiplayer")
multiplayer_button.connect(CLICK, menus.activate, multiplayer_menu)

exit_play_button = gui.Button("Back")
exit_play_button.connect(CLICK, menus.activate, mainmenu)

play_menubar = gui.VBox(align="center", valign="center", y=0, spacing=20)
play_menubar.add(single_player_button, multiplayer_button, exit_play_button)

play_menu.add(play_menubar)


### Single Player


exit_single_player_button = gui.Button("Back")
exit_single_player_button.connect(CLICK, menus.activate, play_menu)

single_player_menubar = gui.VBox(align="center", valign="center", y=0, spacing=20)
single_player_menubar2 = gui.VBox(align="center", valign="center", y=115, spacing=0)
single_player_menubar2.add(exit_single_player_button)

single_player_menu.add(single_player_menubar2)
single_player_menu.add(single_player_menubar)
single_player_menubar.connect(CLICK,play)

### Multiplayer


lan_button = gui.Button("LAN")
lan_button.connect(CLICK, menus.activate, lan_menu)

online_button = gui.Button("Online")
online_button.connect(CLICK, menus.activate, online_menu)

exit_multiplayer_button = gui.Button("Back")
exit_multiplayer_button.connect(CLICK, menus.activate, play_menu)

multiplayer_menubar = gui.VBox(align="center", valign="center", y=0, spacing=20)
multiplayer_menubar.add(lan_button, online_button, exit_multiplayer_button)

multiplayer_menu.add(multiplayer_menubar)

### LAN


### Loop over all available rooms and create a button for each
room99 = gui.Button("placeholder")
room99.connect(CLICK, menus.activate, 98)

exit_lan_button = gui.Button("Back", x=10, y=10)
exit_lan_button.connect(CLICK, menus.activate, multiplayer_menu)

lan_menubar = gui.VBox(align="center", valign="center", y=20, spacing=20)
lan_menubar.add(room99, exit_lan_button)

lan_menu.add(lan_menubar, room99)
#lan_menu.add(room99)

### Online


### Loop over all available rooms and create a button for each

online_room99 = gui.Button("placeholder")
online_room99.connect(CLICK, menus.activate, 96)

exit_online_button = gui.Button("Back")
exit_online_button.connect(CLICK, menus.activate, multiplayer_menu)

online_menubar = gui.VBox(align="center", valign="center", y=20, spacing=20)
online_menubar.add(online_room99, exit_online_button)

online_menu.add(online_menubar)

### Game 1: Rick

continue_button = gui.Button("Continue")
continue_button.connect(CLICK, menus.activate, 1)

replay_button = gui.Button("Replay Level")
replay_button.connect(CLICK, menus.activate, replay_menu)

new_game_button = gui.Button("New Game")
new_game_button.connect(CLICK, menus.activate, are_you_sure_menu)

exit_save1_button = gui.Button("Back")
exit_save1_button.connect(CLICK, menus.activate, single_player_menu)

save1_menubar = gui.VBox(align="center", valign="center", y=20, spacing=20)
save1_menubar.add(continue_button, replay_button, new_game_button, exit_save1_button)

save1_menu.add(save1_menubar)

### New Game: Are you sure?


yes_button = gui.Button("Yes")
yes_button.connect(CLICK, menus.activate, 94)

no_button = gui.Button("No")
no_button.connect(CLICK, menus.activate, 97)

are_you_sure_menubar = gui.VBox(align="center", valign="center", y=20, spacing=20)
are_you_sure_menubar.add(yes_button, no_button)

are_you_sure_menu.add(are_you_sure_menubar)

### Replay Level


### List all completed levels

level99 = gui.Button("Level 99")
level99.connect(CLICK, menus.activate, 91)

exit_replay_button = gui.Button("Back")
exit_replay_button.connect(CLICK, menus.activate, single_player_menu)

replay_menu.add(level99, exit_replay_button)

### Options Menu


w1 = gui.HSlider(min_value=0, length=10, x=200, y=160) # Brightness
w2 = gui.Input(x=100, y=30, width=240) # Resolution X
w3 = gui.Input(x=350, y=30, width=240) # Resolution Y

w4 = gui.HSlider(min_value=0, length=10, x=200, y=560) # Volume

w5 = gui.HSlider(min_value=0, length=10, x=200, y=590) # Speed

w6 = gui.Button("On/Off") # Show GUI

w7 = gui.Button("Save") # Save

w8 = gui.Button("Defaults") # Defaults

exit_options_menu = gui.Button("Back")
exit_options_menu.connect(CLICK, menus.activate, mainmenu)

options_menu.add(w1, w2, w3, w4, w5, w6, w7, w8, exit_options_menu)

# Inside a room.
# Right half shows image with description under it.
# Left half shows people in room and the selected map.


# For each player, create a button which you can CLICK to get image + description

player99 = gui.Button("Player", x=20, y=20)

map_button = gui.Button("Le map", x=20, y=30)
exit_room_button = gui.Button("Quit game")
exit_room_button.connect(CLICK, menus.activate, room_menu)

room_menubar = gui.VBox(align="center", valign="center", y=20, spacing=20)
room_menubar.add(map_button, exit_room_button)

room_menu.add(room_menubar)

## Finito


menus.add(mainmenu, # 0
        play_menu,
        options_menu,
        credits_menu,
        single_player_menu,
        multiplayer_menu, # 5
        lan_menu,
        online_menu,
        save1_menu,
        are_you_sure_menu,
        replay_menu,
        room_menu) # 11

menus.activate(mainmenu)

#the_temp = None
the_temp = gui.Container(width=640, height=480)

while True:
    clock.tick(20)

    events = pygame.event.get()

    for event in events:
        if event.type == QUIT:
            pygame.quit()
            quit()
            
    if active_menu == lan_menu:
        all_lan_rooms = Online.get_lan_rooms()

        for room in lan_rooms:
            menus.remove(room)

        for button in lan_menubar.widgets[:]:
            lan_menubar.remove(button)
        lan_rooms = []

        for room in all_lan_rooms:
            temp = gui.Container(width=640, height=480)
            temp_button = gui.Button("Back")
            temp_button.connect(CLICK, menus.activate, lan_menu)
            temp.add(temp_button)

            lan_rooms.append(temp)
            menus.add(temp)

        # There's a weird bug that wont show the current menu when you add a menu
        menus.activate(active_menu)

        for room in lan_rooms:
            lan_room_button = gui.Button("room 99   test")
            lan_room_button.connect(CLICK, menus.activate, room)
            lan_menubar.add(lan_room_button)
        lan_menubar.add(exit_lan_button)
        #print ">>", lan_menubar.widgets

    if active_menu == online_menu:
        pass
        all_online_rooms = Online.get_online_rooms()
        for room in all_online_rooms:
            temp = gui.Container(width=640, height=480)
            online_rooms.append(temp)

    app.run(events)
    app.draw()
    pygame.display.flip()

