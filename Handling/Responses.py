from Classes import SadogireObjects
from Utility import Processing
from Handling import StarhookControl
from Variables import Lists
RelayID=0

async def FormResponse(SadoObj):
    reply=[None, None] # Declare reply variable, must be a list with 2 variables
    if (SadoObj.Identity == None): # Check if SadogireObjects object has an identity
        reply = await WAIProcess(SadoObj, reply)
    else:
        reply = await Process(SadoObj)
    return reply # Return response
    
# Checks if message is a SadogireObjects class type
async def DetermineObject(message):
    if (type(message) == SadogireObjects.Request or type(message) == SadogireObjects.NodeIdentity or type(message) == SadogireObjects.Reconfig): # Checks for Request Object
        return True
    else:
        return False

# Process SadogireObjects object without an Identity
async def WAIProcess(SadoObj, reply):
    if (type(SadoObj) == SadogireObjects.Request): # If object is a Request type
        reply[0] = "RCF" # Set an ReConFig reply type
        reply[1] = await Processing.ScrubIDs(SadoObj.Content, Lists.SilenceList) # Do your job
        return reply
    elif (type(SadoObj) == SadogireObjects.Reconfig):
        reply[0] = "WAI"
        SadoObj.Edit(await StarhookControl.GetStarhookID(Lists.StarhookList))
        reply[1] = SadoObj
        return reply
    else:
        return ["BAD", None]


async def Process(SadoObj):
    if (type(SadoObj) == SadogireObjects.Request):
        pass
    elif (type(SadoObj) == SadogireObjects.NodeIdentity):
        pass
    if (type(SadoObj) == SadogireObjects.Reconfig):
        pass
