import os, random

# get random guy from the bad-guys folder.
def random_bad_guy():
    array = os.listdir("bad-guys/")
    return array[random.randint(0, 13)]