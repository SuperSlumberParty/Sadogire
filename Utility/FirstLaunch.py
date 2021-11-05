import os

def Setup():
    if os.path.exists('data'):
        return True
    else:
        print("FIRST LAUNCH: Creating a \"data\" folder.")
        os.mkdir('./data')