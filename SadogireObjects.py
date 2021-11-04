class RequestObject:
    MessageType=None
    # 0 - Ping, Content should be None
    # 1 - Node message, Content states 
    # 2 - WhoAmI, assigns ID number, Content states what server and channel it's relaying from
    # 3 - WhereAmI,
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

    def __init__(self, ID, ChannelName, GuildName):
        self.Identity=ID
        self.ChannelName=ChannelName
        self.GuildName=GuildName
