# Sadogire.Handling.Responses is responsible for forming REP responses to requests from starhook objects
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
        await Process(SadoObj, reply)
    return reply # Return response

# Process SadogireObjects object without an Identity
async def WAYProcess(SadoObj, reply):
    if (type(SadoObj) == SadogireObjects.Request): # If object is a Request type
        reply[0] = "RCF" # Set an ReConFig reply type
        if (SadoObj.MessageType != 0): # Check for pings!
            reply[1] = await Processing.ScrubIDs(SadoObj.Content, Lists.SilenceList) # Do your job
        return reply
    elif (type(SadoObj) == SadogireObjects.Reconfig):
        SadoObj.edit(await StarhookControl.GetStarhookID(Lists.StarhookList))
        reply[0] = "WAY"
        reply[1] = SadoObj
        return reply
    else:
        reply[0] = "BAD"
        reply[1] = "NDID object in WAYProcess"

# Process SadogireObjects object with an Identity
async def Process(SadoObj, reply):
    # Appends NDID to SHList
    if (type(SadoObj) == SadogireObjects.NodeIdentity):
        reply[0] = "OK"
        if (await StarhookControl.CheckNode(SadoObj.Identity, Lists.StarhookList)): # If exists - Reply with BAD
            Node = await StarhookControl.GetNode(SadoObj.Identity, Lists.StarhookList)
            await StarhookControl.EditNode(Node[0], SadoObj.ChannelName, SadoObj.GuildName)
        else:
            print(f"Added {SadoObj.Identity} to NodeIdentity")
            Lists.StarhookList.append(SadoObj)
    # Reconfigures a Node
    elif (type(SadoObj) == SadogireObjects.Reconfig):
        vars = await StarhookRCF.GetRCFVars(SadoObj.Identity)
        SadoObj.edit(None, vars[0], vars[1], vars[2], vars[3])
        reply[0] = "WAY"
        reply[1] = SadoObj
        await StarhookRCF.RemRCFTask(SadoObj.Identity)
    # Request response
    elif (type(SadoObj) == SadogireObjects.Request):
        reply[0] = "OK" # Assume ping
        reply[1] = None
        if (await StarhookControl.CheckNode(SadoObj.Identity, Lists.StarhookList) == False): # If object possesses an identity not known to Sadogire, send WAY
            reply[0] = "WAY"
        if (await StarhookRCF.CheckRQL(SadoObj.Identity)): # If RCF Task present - Override OK to RCF
            reply[0] = "RCF"
        if (SadoObj.MessageType != 0): # If not ping
            reply[1] = await Processing.ScrubIDs(SadoObj.Content, Lists.SilenceList)
    else:
        reply[0] = "BAD"
        reply[1] = "Unknown object in Process function"
