# file data logging
# fortnite game
# Will be very useful for debugging.

import os, datetime

def create(string):
    if os.path.exists(str(string)):
        print(str(string), "| EXISTS")
    else:
        f = open(str(string), "x") # x = create in docs
        print(str(string), "| CREATED")
        
def write(string, file):
    str_file = str(file)
    if os.path.exists(str_file):
        f = open(str_file, "a")
        f.write("[" + str(datetime.datetime.now())+ "] " + str(string) + "\n")
        f.close()
    else:
        print("No file exists:", str_file)

def delete(file):
    str_file = str(file)
    if os.path.exists(str_file):
        os.remove(str_file)
        print("Removed:", str_file)
    else:
        print("No file exists:", str_file)

def read(file):
    str_file = str(file)
    if os.path.exists(str_file):
        f = open(str_file, "r")
        return(f.read())
    else:
        print("No file exists:", str_file)