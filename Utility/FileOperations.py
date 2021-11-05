import os

def Setup():
    if os.path.exists('data'):
        return True
    else:
        print("FIRST LAUNCH: Creating a \"data\" folder.")
        os.mkdir('./data')


# Utilities
async def SaveLists(object, path):
    try:
        mode = 'a' if os.path.exists(path) else 'w'
        with open('data/Lists.sadogire', 'wb') as SadoList:
            SadoList.write(object)
    except:
        print("Did you mess with the data folder?")