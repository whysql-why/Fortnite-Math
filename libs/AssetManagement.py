
from libs import question
from libs import config
import pygame, os, random

def better_bad_guy_generator():
    if(config.get_config()[0]['log-everything']):
        print("Starting... getting random bad guy!")
    files = os.listdir("bad-guys")
    determined = random.randint(0, len(files) - 1)
    file_name = os.path.splitext(files[determined])[0]
    the_max = get_max(str(file_name)) # get the max where the image can go. If the player is in that position, just move the player back.
    if(config.get_config()[0]['log-everything']):
        print(the_max)
    game_start = False
    load_file = pygame.image.load("bad-guys/" + file_name + ".png") # didn't i just striped the file extension? wow.
    file_name_rect = load_file.get_rect()
    file_name_rect.x = the_max[0]
    file_name_rect.y = the_max[1]
    return load_file, file_name_rect, the_max


# DO NOT DELETE THE FOLLOWING:
def get_max(name):
    print(f"In the get_max() function! PAYLOAD: {name}")
    if(config.get_config()[0]['log-everything']):
        print(f"PAYLOAD: {name}")
    if name == "building_guy":
        return 400, 170
    if name == "guy_healing":
        return 400, 140
    if name == "heal_guy":
        return 400, 200
    if name == "L_camper":
        return 400, 190
    if name == "L_camper_2":
        return 400, 135
    if name == "pickaxe_guy":
        return 400, 200
    if name == "revolver_guy":
        return 400, 210
    if name == "shotgun_guy":
        return 400, 204
    if name == "team_guy":
        return 400, 209
    if name == "teamers_in_solos":
        return 400, 125
    if name == "tree_guy":
        return 400, 139
    if name == "truck_guy":
        return 300, 139