import pygame, sys, os
from pygame.locals import *

money = 500
shopping = True
inv_list = [ 'Copper', 'Copper', 'Copper', 'Aluminum', 'Aluminum', 'Uranium', 'Ruby', 'Ruby', 'Emerald', 'Diamond']
store_list = [ 'Copper', 'Copper', 'Copper', 'Aluminum', 'Aluminum', 'Uranium', 'Ruby', 'Ruby', 'Emerald', 'Diamond']
inv_dict = {}
store_dict = {}
item_keys = {
    K_1: 'Copper',
    K_2: 'Aluminum',
    K_3: 'Uranium',
    K_4: 'Ruby',
    K_5: 'Emerald',
    K_6: 'Diamond'}
def fill_dict(list,dict):
    for x in list:
        if x not in dict:
            dict[x] = 1
        else:
            dict[x] += 1
fill_dict(inv_list, inv_dict)
fill_dict(store_list, store_dict)
print "Money remaining: ", money
print "Your items: ", inv_dict
print "Store items: ", store_dict
prices = {
    'Copper': 10,
    'Aluminum': 25,
    'Uranium': 100,
    'Ruby': 75,
    'Emerald': 250,
    'Diamond': 1000
    }
pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.update()

def buy (item):
    global money
    if item not in store_dict:
        print "Cannot buy fggt"
    else:
        if store_dict[item] == 0 or prices[item]>money:
            print "Cannot buy fag"
        else:
            store_dict[item] -= 1
            money -= prices[item]
            if item not in inv_dict:
                inv_dict[item] = 1
            else:
                inv_dict[item] += 1
            print "Bought: ", item
            print "Money remaining: ", money
            print "Your items: ", inv_dict
            print "Store items: ", store_dict
            

def sell(item):
    global money
    if item not in inv_dict:
        print "Cannot sell fggt"
    else:
        if inv_dict[item] == 0:
            print "Cannot sell fag"
        else:
            inv_dict[item] -= 1
            money += prices[item]
            if item not in store_dict:
                store_dict[item] = 1
            else:
                store_dict[item] += 1
            print "Sold: ", item
            print "Money remaining: ", money
            print "Your items: ", inv_dict
            print "Store items: ", store_dict
                

while shopping:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key in item_keys:
                if pygame.key.get_mods() & KMOD_SHIFT == 1:
                    sell(item_keys[event.key])
                elif pygame.key.get_mods() & KMOD_SHIFT == 0:
                    buy(item_keys[event.key])
            elif event.key == K_RETURN:
                shopping = False
            else:
                pass
print "Finished shopping!"
print "Money remaining: ", money
print "Your items: ", inv_dict
print "Store items: ", store_dict
            
