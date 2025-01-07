# This file is for managing assets.
# written by: Epik Games group


# import the other libraries.
from libs import question
from libs import config
import pygame, os, random


# this is the code to get a random bad guy.
# this is better than the random_bad_guy() function, which is removed.
def better_bad_guy_generator():
    if(config.get_config()[0]['log-everything']):
        print("Starting... getting random bad guy!")
    files = os.listdir("bad-guys")
    determined = random.randint(0, len(files) - 1)
    file_name = os.path.splitext(files[determined])[0]
    the_max = get_max(str(file_name)) # get the max where the image can go. If the player is in that position, just move the player back.
    if(config.get_config()[0]['log-everything']): # logging and debugging....
        print(the_max)
    game_start = False
    load_file = pygame.image.load("bad-guys/" + file_name + ".png") # didn't i just striped the file extension? wow.
    file_name_rect = load_file.get_rect()
    file_name_rect.x = the_max[0] # get the max x position the bad guy can go.
    file_name_rect.y = the_max[1] # get the max y position the bad guy can go.
    return load_file, file_name_rect, the_max # return it!


# DO NOT DELETE THE FOLLOWING:
# this took so much time to get right.

BAD_GUY_POSITIONS = {
    "building_guy": (400, 170),
    "guy_healing": (400, 140),
    "heal_guy": (400, 200),
    "L_camper": (400, 190),
    "L_camper_2": (400, 135),
    "pickaxe_guy": (400, 200),
    "revolver_guy": (400, 210),
    "shotgun_guy": (400, 204),
    "team_guy": (400,209),
    "teamers_in_solos": (400, 125),
    "tree_guy": (400, 139),
    "truck_guy": (300, 139)
}

# get_max(name) the name represents the bad guy's name from the bad-guys folder
def get_max(name):
    return BAD_GUY_POSITIONS.get(name, (400, 200))
