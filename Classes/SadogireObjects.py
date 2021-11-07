# This file states class types Sadogire is using
# If you need to change this - reflect the changes for Starhook instances aswell
# Every class (except for UserPermissions) has an "Identity" variable, which tells Sadogire from what Starhook instance a message is coming from

# Request Class (RCF)
# This class is responsible for sending messages to be processed and pinging the server in case it's not responding
class Request:
    Identity=None
    MessageType=None
    # 0 - Ping, Content should be None
    # 1 - Node message, Content states string needed to be processed
    Content=None

    def getType(self):
        return self.MessageType

    def __init__(self, MsgType, Cont):
        self.MessageType=MsgType
        self.Content=Cont

# NodeIdentity class (NDID)
# This class is responsible for identifying itself to the Sadogire instance and what it relays from.
class NodeIdentity:
    Identity=None
    ChannelName=None
    GuildName=None

    def __init__(self, Id, ChannelName, GuildName):
        self.Identity=Id
        self.ChannelName=ChannelName
        self.GuildName=GuildName

# Reconfig class (RCF) 
# This class is responsible for changing settings of a Starhook instance.
class Reconfig:
    Identity=None
    ChannelID=None
    GuildID=None
    GuildMode=None
    WebhookURL=None

    def __init__(self, Id, CId, GId, GMode, WHUrl):
        self.Identity=Id
        self.ChannelID=CId
        self.GuildID=GId
        self.GuildMode=GMode
        self.WebhookURL=WHUrl
    
    def edit(self, Id=None, CId=None, GId=None, GMode=None, WHUrl=None):
        if (Id != None):
            self.Identity = Id
        if (CId != None):
            self.ChannelID = CId
        if (GId != None):
            self.GuildID = GId
        if (GMode != None):
            self.GuildMode = GMode
        if (WHUrl != None):
            self.WebhookURL = WHUrl

# UserPermissions class (UP) 
# This class is responsible for user identification and Sadogire command permission checks
# See Handling.SadogirePermissions for more information
class UserPermissions:
    PermissionLevel=None
    Revoked=False

    def __init__(self, PermissionsLevel=0, Revoked=False):
        self.PermissionLevel=PermissionsLevel
        self.Revoked=Revoked
    
    def UpdatePermissions(self, Level):
        self.PermissionLevel=Level
    def TogglePermissions(self):
        self.Revoked=not self.Revoked
        
        