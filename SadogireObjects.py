class Request:
    MessageType=None
    # 0 - Ping, Content should be None
    # 1 - Node message, Content states 
    # 2 - WhoAmI, assigns ID number, Content states what server and channel it's relaying from
    # 3 - WhereAmI, Contains either guild or channel info
    Content=None

    def GetType(self):
        return self.MessageType

    def __init__(self, MsgType, Cont):
        self.MessageType=MsgType
        self.Content=Cont

class NodeIdentity:
    Identity=None
    ChannelName=None
    GuildName=None

    def __init__(self, Id, ChannelName, GuildName):
        self.Identity=Id
        self.ChannelName=ChannelName
        self.GuildName=GuildName

class Reconfiguration:
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
        
        