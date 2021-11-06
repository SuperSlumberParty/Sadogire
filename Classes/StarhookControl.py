# NodeIdentity (NDID) Operations
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

# TODO: Reconfig (RCF) Opearations
