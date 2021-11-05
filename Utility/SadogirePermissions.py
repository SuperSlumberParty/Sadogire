from Variables.Config import OWNERID
from Variables.Lists import ApprovedUsers
# SadogirePermissions is an internal permissions system designed to give different users 
# different bot functionality 
# independent of their personal permissions
# 0 stands for revoked permissions, while 3 is the owner
async def PermissionsCheck(userid):
    if (userid == OWNERID):
        return 3
    if userid in (item[0] for item in ApprovedUsers):
        Req = [item for item in ApprovedUsers if userid == item[0]]
        print(Req)
        if (Req[0][1].Revoked == True):
            return 0
        return Req[0][1].PermissionLevel
    else:
        return False