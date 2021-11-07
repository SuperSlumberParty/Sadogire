# SadogirePermissions is an internal permissions system designed to give different users different bot functionality independent of their personal permissions.
# It uses Classes.SadogireObjects.UserPermissions objects to accomplish this
# 0 stands for revoked permissions, while 3 is the owner. Everything in between is for approved users
# False is for when the user is not on the list

from Variables.Config import OWNERID

# Obtains a UserPermissions Object of a user
async def GetUser(userid, ApprovedUsers):
    if userid in (item[0] for item in ApprovedUsers): # Check if user exists in list
        return [item for item in ApprovedUsers if userid == item[0]][0][1] 
    else: # If not found - return false
        return False

# Returns permission level of a person
async def PermissionsCheck(userid, ApprovedUsers):
    if (userid == OWNERID): # If userid matches owner - return max permission level
        return 3
    User = await GetUser(userid, ApprovedUsers)
    if (User == False):
        return False # Not A User
    if (User.Revoked == True):
            return 0
    return User.PermissionLevel

# Revokes/Restores permission to use the bot
async def RRPermissions(userid, ApprovedUsers):
    User = await GetUser(userid, ApprovedUsers)
    User.TogglePermissions()