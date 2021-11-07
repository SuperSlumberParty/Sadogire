# This file is responsible for handling NodeIdentity objects (NDID) and managing the StarhookList list from Variables

async def CheckNode(id, SHList):
    if id in (NDID.Identity for NDID in SHList):
        return True
    return False

async def GetNode(id, SHList):
    if id in (NDID.Identity for NDID in SHList):
        return [NDID for NDID in SHList if id == NDID.Identity]
    return False

async def AssignNode(NDID, SHList):
    return SHList.append(NDID)

async def EditNode(NDID, ChannelName, GuildName):
    NDID.ChannelName=ChannelName
    NDID.GuildName=GuildName

async def GetStarhookID(SHList):
    i=1 # declare temp variable
    if not SHList:
        return 0
    while True:
        if (CheckNode(i, SHList) == False):
            return False
        i=i+1
