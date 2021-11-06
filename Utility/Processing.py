import re, pickle

async def ScrubIDs(message, IDlist):
    def sub(m):
        return '' if m.group() in s else m.group()
    s = set(IDlist)
    result = re.sub(r'\w+', sub, message)
    return result

async def Pickle(x):
    return pickle.dumps(x)

