# This file is responsible for managing Classes.SadogireObjects.Reconfig (RCF) objects and Lists.ReconfigQueueList (RQL) 
# RQL contains tuples, each having an ID and a list containing 4 variables
from Variables.Lists import ReconfigQueueList

# Checks if node has RCF tasks
async def CheckRQL(id):
    if id in (RQLID[0] for RQLID in ReconfigQueueList):
        return True

# Retrieves RCF list
async def GetRCFlist(id):
    return [RCF for RCF in ReconfigQueueList if id == RCF[0]][0]

# Retrieves RCF variables
async def GetRCFVars(id):
    if (await CheckRQL(id)):
        return [RQLID[1] for RQLID in ReconfigQueueList if id == RQLID[0]][0]

# Validates vars list from CreateRCFTask
# Should be [int,int,bool,string], any member of the list can be NoneType aswell
async def ValidateRCFTask(vars):
    if (len(vars) != 4):
        return False
    if (type(vars[0]) == int or vars[0] == None):
        if (type(vars[1]) == int or vars[1] == None):
            if (type(vars[2]) == bool or vars[2] == None):
                if (type(vars[3]) == str or vars[3] == None):
                    return True
    return False

async def CreateRCFTask(id,vars):
    RCFVars = vars.split(";") # Separate variables
    # Assign nonetype to "None"
    for i in range(len(RCFVars)):
        if RCFVars[i] == 'None':
            RCFVars[i] = None
    
    if (RCFVars[0] != None):
        RCFVars[0]=int(RCFVars[0])
    if (RCFVars[1] != None):
        RCFVars[1]=int(RCFVars[1])

    # Assign bool to 3rd variable
    if (RCFVars[2] != None):
        if (RCFVars[2].lower() == "true"):
            RCFVars[2] = True
        elif (RCFVars[2].lower() == "false"):
            RCFVars[2] = False
    
    if(await ValidateRCFTask(RCFVars)):
        await AddRCFTask(id, RCFVars)
        return True
    return False


# Adds a Reconfigure Task
# NOTE: This function returns a boolean to notify on whether or not a task has been overriden
# False stands for a new task, while True stands for an override
async def AddRCFTask(id, vars):
    if (await CheckRQL(id)):
        RCFlist = await GetRCFlist(id)
        RCFlist[1] = vars
        return True
    else:
        ReconfigQueueList.append([id, vars])
        return False

# Remove a Reconfigure Task
# NOTE: This function is called each time a task is processed and sent to a starhook instance
async def RemRCFTask(id):
    ReconfigQueueList.pop(ReconfigQueueList.index([RCF for RCF in ReconfigQueueList if id == RCF[0]][0])) # Masonic bullshit