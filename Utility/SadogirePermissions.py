from Variables.Config import OWNERID

# SadogirePermissions is an internal permissions system designed to give different users different bot functionality independent of their personal permissions
# This is not to be confused with SadogireObjects.UserPermissions, which is a class with permissions of a specific user
# 0 stands for revoked permissions, while 3 is the owner
# False is for when the user is not on the list

# Obtains a UserPermissions Object of a user
async def GetUser(userid, ApprovedUsers):
    if userid in (item[0] for item in ApprovedUsers):
        return [item for item in ApprovedUsers if userid == item[0]][0][1] 
    else:
        return False

# Returns permission level of a person
async def PermissionsCheck(userid, ApprovedUsers):
    if (userid == OWNERID):
        return 3
    User = await GetUser(userid, ApprovedUsers)
    if (User.Revoked == True):
            return 0
    return User.PermissionLevel

# Revokes/Restores permission to use the bot
async def RRPermissions(userid, ApprovedUsers):
    User = await GetUser(userid, ApprovedUsers)
    User.TogglePermissions()