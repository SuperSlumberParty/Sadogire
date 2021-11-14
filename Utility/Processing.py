import re

# This function is responsible for removing User IDs in IDlist from messages it receives.
async def ScrubIDs(message, IDlist):
    def sub(m):
        return '' if m.group() in s else m.group()
    s = set(IDlist)
    result = re.sub(r'\w+', sub, message)
    result = result.replace("@here", "!MASSPING!")
    result = result.replace("@everyone", "!MASSPING!")
    print(result)
    return result

