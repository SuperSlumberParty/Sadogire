# This file is responsible for everything related to files and directories, be it saving configuration or initialising Sadogire

import os, pickle
from Classes import SadogireObjects

# Setup Sadogire for launch
def Setup():
    if os.path.exists('data'): # Check if 'data' exists
        return True
    else: # If not - assume it's first launch and create one
        print("FIRST LAUNCH: Creating a \"data\" folder.")
        os.mkdir('./data')

# Save Lists to file
async def Save(object, path):
    try:
        with open(path, 'wb') as SadoList:
            pickle.dump(object, SadoList)
    except:
        print("Did you mess with the data folder?")

# Load lists from file
async def Load(path):
    try:
        with open(path, 'rb') as SadogireLists:
            return pickle.load(SadogireLists)
    except:
       print("Unable to load lists!")