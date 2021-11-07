# This file is responsible for removing User IDs in IDlist from messages it receives.
import re

async def ScrubIDs(message, IDlist):
    def sub(m):
        return '' if m.group() in s else m.group()
    s = set(IDlist)
    result = re.sub(r'\w+', sub, message)
    return result

