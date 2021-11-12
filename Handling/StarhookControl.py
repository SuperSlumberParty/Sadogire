# This file is responsible for handling NodeIdentity objects (NDID) and managing the StarhookList list from Variables
# See Handling.SadogireObjects.NodeIndentity for more information

# Check if NDID exists in list
async def CheckNode(id, SHList):
    if id in (NDID.Identity for NDID in SHList):
        return True
    return False

# Return a NDID object if exists
async def GetNode(id, SHList):
    if (await CheckNode(id, SHList)):
        return [NDID for NDID in SHList if id == NDID.Identity]
    return False

# Add NDID object to list
async def AssignNode(NDID, SHList):
    return SHList.append(NDID)

# Edit an NDID object
async def EditNode(NDID, ChannelName, GuildName):
    NDID.ChannelName=ChannelName
    NDID.GuildName=GuildName

# Check list for a free NDID Identity variable
async def GetStarhookID(SHList):
    i=1 # declare temp variable
    if not SHList: # Check if list is empty
        return 0
    while True:
        if (await CheckNode(i, SHList) == False):
            return False
        i=i+1
