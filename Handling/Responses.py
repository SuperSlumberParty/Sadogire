# Handling.Responses is responsible for forming REP responses to requests from starhook objects
# Responses are formed based on the type of object received and whether or not it has an Identity (See Classes.SadogireObjects for more info on Identity)
# Response types are the following - "OK", "WAY", "RCF", "BAD"
# If Identity is missing - Sadogire will respond with a "RCF" (ReConFigure) or "WAY" ("Who Are You") type response for Request and Reconfig objects respectively
# If Identity is present - Sadogire will respond with an "OK" or "RCF" response depending on whether or not there is a reconfigure task on this Identity ID
# In any other case - Sadogire will respond with a "BAD" response

from Classes import SadogireObjects
from Utility import Processing
from Handling import StarhookControl, StarhookRCF
from Variables import Lists


# Checks if message is a SadogireObjects class type
async def DetermineObject(message):
    if (type(message) == SadogireObjects.Request # Checks for REQ Object
        or type(message) == SadogireObjects.NodeIdentity # Or NDID
        or type(message) == SadogireObjects.Reconfig): # Or RCF
        return True
    else:
        return False

# Retrieves response
async def GetResponse(SadoObj):
    reply=[None, None] # Declare reply variable, must be a list with 2 variables
    # Check if SadogireObjects object has an identity
    if (SadoObj.Identity == None): # If not - process with a WAI response
        await WAYProcess(SadoObj, reply)
    else:
        await Process(SadoObj)
    return reply # Return response

# Process SadogireObjects object without an Identity
async def WAYProcess(SadoObj, reply):
    if (type(SadoObj) == SadogireObjects.Request): # If object is a Request type
        reply[0] = "RCF" # Set an ReConFig reply type
        reply[1] = await Processing.ScrubIDs(SadoObj.Content, Lists.SilenceList) # Do your job
        return reply
    elif (type(SadoObj) == SadogireObjects.Reconfig):
        SadoObj.Edit(await StarhookControl.GetStarhookID(Lists.StarhookList))
        reply[0] = "WAY"
        reply[1] = SadoObj
        return reply
    else:
        reply[0] = "BAD"
        reply[1] = None

# Process SadogireObjects object with an Identity
async def Process(SadoObj, reply):
    if (type(SadoObj) == SadogireObjects.NodeIdentity):
        if (await StarhookControl.CheckNode(SadoObj.Identity)):
            reply[0] = "BAD"
            reply[1] = None
        else:
            Lists.StarhookList.append(SadoObj)
    elif (type(SadoObj) == SadogireObjects.Reconfig):
        SadoObj.edit(StarhookControl.GetStarhookID(Lists.StarhookList))
        reply[0] = "WAY"
        reply[1] = SadoObj
    elif (type(SadoObj) == SadogireObjects.Request):
        pass
    else:
        pass
