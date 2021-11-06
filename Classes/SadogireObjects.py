class Request:
    MessageType=None
    Identity=None
    # 0 - Ping, Content should be None
    # 1 - Node message, Content states string needed to be processed
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
    
    def Edit(self, Id=None, CId=None, GId=None, GMode=None, WHUrl=None):
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
        
        