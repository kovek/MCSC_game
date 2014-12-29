import sys
from enum import Enum

sys.path.insert(0, '..')

import pygame
import gooeypy as gui
from gooeypy.const import *

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((640, 480), pygame.SRCALPHA)

app = gui.Container(width=640, height=480, surface=screen)

class Menus(gui.Container):
    def activate(self, index):
        if index == Const.QUIT:
            pygame.quit()
            sys.exit()
        for w in self.widgets:
            w.active = False
        self.widgets[index].active = True

menus = Menus(width=640, height=480)
app.add(menus)


Const = Enum('Const', 'QUIT')

### Main Menu

mainmenu = gui.Container(width=640, height=480)

play_button = gui.Button("Play")
play_button.connect(CLICK, menus.activate, 1)

options_button = gui.Button("Options")
options_button.connect(CLICK, menus.activate, 2)

credits_button = gui.Button("Credits")
credits_button.connect(CLICK, menus.activate, 3)

quit_button = gui.Button("Quit")
quit_button.connect(CLICK, menus.activate, Const.QUIT)

mainmenu_menubar = gui.VBox(align="center", valign="center", y=0, spacing=20)
mainmenu_menubar.add(play_button, options_button, credits_button, quit_button)

mainmenu.add(mainmenu_menubar)

### Credits

credits_menu = gui.Container(width=640, height=480)

exit_credits_button = gui.Button("Back", align="left", valign="bottom", x=10, y=-10)
exit_credits_button.connect(CLICK, menus.activate, 0)

credits_menu.add(exit_credits_button)


### Play

play_menu = gui.Container(width=640, height=480)

single_player_button = gui.Button("Single Player")
single_player_button.connect(CLICK, menus.activate, 4)

multiplayer_button = gui.Button("Multiplayer")
multiplayer_button.connect(CLICK, menus.activate, 5)

exit_play_button = gui.Button("Back")
exit_play_button.connect(CLICK, menus.activate, 0)

play_menubar = gui.VBox(align="center", valign="center", y=0, spacing=20)
play_menubar.add(single_player_button, multiplayer_button, exit_play_button)

play_menu.add(play_menubar)


### Single Player

single_player_menu = gui.Container(width=640, height=480)

save1_button = gui.Button("save 1: rick")
save1_button.connect(CLICK, menus.activate, 97)

save2_button = gui.Button("save 2: bob")
save2_button.connect(CLICK, menus.activate, 97)

save3_button = gui.Button("save 3: morty")
save3_button.connect(CLICK, menus.activate, 97)

exit_single_player_button = gui.Button("Back")
exit_single_player_button.connect(CLICK, menus.activate, 1)

single_player_menubar = gui.VBox(align="center", valign="center", y=0, spacing=20)
single_player_menubar.add(save1_button, save2_button, save3_button, exit_single_player_button)

single_player_menu.add(single_player_menubar)

### Multiplayer

multiplayer_menu = gui.Container(width=640, height=480)

lan_button = gui.Button("LAN")
lan_button.connect(CLICK, menus.activate, 6)

online_button = gui.Button("Online")
online_button.connect(CLICK, menus.activate, 7)

exit_multiplayer_button = gui.Button("Back")
exit_multiplayer_button.connect(CLICK, menus.activate, 1)

multiplayer_menubar = gui.VBox(align="center", valign="center", y=0, spacing=20)
multiplayer_menubar.add(lan_button, online_button, exit_multiplayer_button)

multiplayer_menu.add(multiplayer_menubar)

### LAN

lan_menu = gui.Container(width=640, height=480)

### Loop over all available rooms and create a button for each
room99 = gui.Button("placeholder")
room99.connect(CLICK, menus.activate, 98)

exit_lan_button = gui.Button("Back")
exit_lan_button.connect(CLICK, menus.activate, 1)

lan_menubar = gui.VBox(align="center", valign="center", y=20, spacing=20)
lan_menubar.add(room99, exit_lan_button)

lan_menu.add(lan_menubar)

### Online

online_menu = gui.Container(width=640, height=480)

### Loop over all available rooms and create a button for each

online_room99 = gui.Button("placeholder")
online_room99.connect(CLICK, menus.activate, 96)

exit_online_button = gui.Button("Back")
exit_online_button.connect(CLICK, menus.activate, 5)

online_menubar = gui.VBox(align="center", valign="center", y=20, spacing=20)
online_menubar.add(online_room99, exit_online_button)

online_menu.add(lan_menubar)

### Game 1: Rick

save1_menu = gui.Container(width=640, height=480)

continue_button = gui.Button("Continue")
continue_button.connect(CLICK, menus.activate, 1)

replay_button = gui.Button("Replay Level")
replay_button.connect(CLICK, menus.activate, 10)

new_game_button = gui.Button("New Game")
new_game_button.connect(CLICK, menus.activate, 9)

exit_save1_button = gui.Button("Back")
exit_save1_button.connect(CLICK, menus.activate, 4)

save1_menubar = gui.VBox(align="center", valign="center", y=20, spacing=20)
save1_menubar.add(room99, exit_online_button)

save1_menu.add(lan_menubar)

### New Game: Are you sure?

are_you_sure_menu = gui.Container(width=640, height=480)

yes_button = gui.Button("Yes")
yes_button.connect(CLICK, menus.activate, 94)

no_button = gui.Button("No")
no_button.connect(CLICK, menus.activate, 97)

are_you_sure_menubar = gui.VBox(align="center", valign="center", y=20, spacing=20)
are_you_sure_menubar.add(room99, exit_online_button)

are_you_sure_menu.add(lan_menubar)

### Replay Level

replay_menu = gui.Container(width=640, height=480)

### List all completed levels

level99 = gui.Button("Level 99")
level99.connect(CLICK, menus.activate, 91)

exit_replay_button = gui.Button("Back")
exit_replay_button.connect(CLICK, menus.activate, 4)

replay_menu.add(level99, exit_replay_button)

### Options Menu

options_menu = gui.Container(width=640, height=480)

w1 = gui.HSlider(min_value=0, length=10, x=200, y=160) # Brightness
w2 = gui.Input(x=100, y=30, width=240) # Resolution X
w3 = gui.Input(x=350, y=30, width=240) # Resolution Y

w4 = gui.HSlider(min_value=0, length=10, x=200, y=560) # Volume

w5 = gui.HSlider(min_value=0, length=10, x=200, y=590) # Speed

w6 = gui.Button("On/Off") # Show GUI

w7 = gui.Button("Save") # Save

w8 = gui.Button("Defaults") # Defaults

exit_options_menu = gui.Button("Back")
exit_options_menu.connect(CLICK, menus.activate, 0)

options_menu.add(w1, w2, w3, w4, w5, w6, w7, w8, exit_options_menu)

# Inside a room.
# Right half shows image with description under it.
# Left half shows people in room and the selected map.

room_menu = gui.Container(width=640, height=480)

# For each player, create a button which you can CLICK to get image + description

player99 = gui.Button("Player", x=20, y=20)

map_button = gui.Button("Le map", x=20, y=30)
exit_room_button = gui.Button("Quit game")
exit_room_button.connect(CLICK, menus.activate, 11)

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

menus.activate(0)






while True:
    clock.tick(20)

    events = pygame.event.get()

    for event in events:
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    app.run(events)
    app.draw()
    pygame.display.flip()
