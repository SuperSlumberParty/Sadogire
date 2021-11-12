#\x45\x4e\x44\x45\x52\x42\x4c\x49\x54\x5a\x27\x53\x0a
#\x53\x55\x50\x45\x52
#\x53\x4c\x55\x4d\x42\x45\x52
#\x50\x41\x52\x54\x59
import warnings
import asyncio

import discord
from discord.ext import commands
from discord.ext.commands import Bot, has_permissions, CheckFailure


from Variables import Config, Lists
from Classes import SadogireObjects
from Utility import Cryptography, FileOperations
from Handling import StarhookControl, Responses, SadogirePermissions, StarhookRCF

import zmq # Communication via tcp
import zmq.asyncio


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # Error supression for zmq

# Server block start
async def Init():
    sock = zmq.asyncio.Context().socket(zmq.REP)
    sock.setsockopt(zmq.SNDTIMEO, Config.TIMEOUT)
    sock.bind(f"tcp://*:{Config.INPORT}")
    while True:
        Request = await Cryptography.Unscramble(await sock.recv()) #Unscramble (Decrypt&Decode) an object
        isSadoObject = await Responses.DetermineObject(Request) #Check if object belongs to SadogireObjects
        if (isSadoObject == False): # If not - Deny
            await sock.send(b"You're delusional")
        else:
            Response = await Responses.GetResponse(Request) # Send Object for processing
            await sock.send(await Cryptography.Scramble(Response))

# Bot preconfiguration
Triton=commands.Bot(command_prefix="sg>", case_insensitive=True)

# This function sends a message to a specified logchannel in the config
async def ActionLog(message):
    if (Config.LOGCHANNEL == 0):
        print(message) #Print error in console
    else:
        await Triton.get_channel(Config.LOGCHANNEL).send(message)

# Init event - starts when the bot is being booted up
@Triton.event
async def on_ready():
    asyncio.get_event_loop().create_task(Init())
    try:
        await Load()
    except:
        warnings.warn(f"{Config.FILENAME} failed to load! Please (re)create {Config.FILENAME} in the \"data\" folder using the \"resetdata\" command!")

    print("Sadogire is running!")
    #await ActionLog("Sadogire instance is running. Awaiting nodes")

# Queries whether or not this user is approved to use the bot
@Triton.command(name='query')
async def QueryUser(ctx, userid=None):
    if (userid==None):
        userid = ctx.author.id
    if (await SadogirePermissions.PermissionsCheck(ctx.author.id, Lists.ApprovedUsers) == False):
        await ctx.channel.send("You are not approved to use this command.")
        return
    PermissionLevel=await SadogirePermissions.PermissionsCheck(int(userid), Lists.ApprovedUsers)
    if (PermissionLevel == False):
        await ctx.channel.send("This user is not approved")
    elif (PermissionLevel == 0):
        await ctx.channel.send("This user's permissions have been revoked.")
    else:
        await ctx.channel.send(f"This user is approved and has permissions level {PermissionLevel}")

# Approves user, requires owner access
# This command *should* be only available to the owner
@Triton.command(name='approve')
async def ApproveUser(ctx, userid, level):
    if (await SadogirePermissions.PermissionsCheck(ctx.author.id, Lists.ApprovedUsers) == Config.OWNERLEVEL):
        if (await SadogirePermissions.GetUser(int(userid), Lists.ApprovedUsers) == False):
            Lists.ApprovedUsers.append([int(userid), SadogireObjects.UserPermissions(int(level), False)])
            await SavePrep()
        else:
            await ctx.channel.send("This user is already on the approved list.")
    print(Lists.ApprovedUsers)

# Flips permissions of a user
# This command *should* be only available to the owner
@Triton.command(name='switch')
async def RevokeRestore(ctx, userid):
    if (await SadogirePermissions.PermissionsCheck(ctx.author.id, Lists.ApprovedUsers) == Config.OWNERLEVEL):
        await SadogirePermissions.RRPermissions(int(userid), Lists.ApprovedUsers)
        await SavePrep()

# Adds own userid to SilenceList
# This command requires the user to be approved
@Triton.command(name='silence')
async def AddToSilenceList(ctx):
    if (await SadogirePermissions.PermissionsCheck(ctx.author.id, Lists.ApprovedUsers) > 0):
        AuthorId = str(ctx.author.id) # Get author ID
        if (AuthorId in Lists.SilenceList):
            Lists.SilenceList = [id for id in Lists.SilenceList if AuthorId not in id]
            await SavePrep()
        else:
            Lists.SilenceList.append(AuthorId)
            await SavePrep()

# Reset/Create the data file
# This command *should* be only available to the owner
@Triton.command(name='resetdata')
async def ResetData(ctx):
    if (await SadogirePermissions.PermissionsCheck(ctx.author.id, Lists.ApprovedUsers) == Config.OWNERLEVEL):
        Lists.ReconfigQueueList=[]
        Lists.SilenceList=[]
        Lists.StarhookList=[]
        Lists.ApprovedUsers=[]
        await SavePrep()

# Create an RCF Task
# This command requires permission level 2 or higher
@Triton.command(name='Task')
async def AddRCFTask(ctx, id, vars):
    if (await SadogirePermissions.PermissionsCheck(ctx.author.id, Lists.ApprovedUsers) >= 2):
        if(await StarhookRCF.CreateRCFTask(int(id), vars)):
            await ctx.channel.send("Task created")
        else:
            await ctx.channel.send("Failed to create task!")

# Sends all list contents in DM's
# This command requires owner permissions
@Triton.command(name='dump')
async def DumpLists(ctx):
    if (await SadogirePermissions.PermissionsCheck(ctx.author.id, Lists.ApprovedUsers) == Config.OWNERLEVEL):
        await ctx.author.send(f"ApprovedUsers: {Lists.ApprovedUsers}\nSilenceList: {Lists.SilenceList}\nStarhookList: {Lists.StarhookList[0]}\nReconfigQueueList: {Lists.ReconfigQueueList}")


# Config checks before initialization 
def CheckConfig():
    if (Config.TOKEN == ""): # If the token is empty - Assume Config.py was untouched
        raise ValueError("You have not configured the config file!\nPlease edit config.py with the required variables!")
    if (Config.INPORT > 65535 or Config.INPORT < 0): # If RFC 793 is violated - raise an error and explain why
        raise ValueError("Port value is incorrect! You are allowed to have a port number ranging from 1 to 65535 due to TCP header limitations!\
                          Negative numbers, 0, or anything over 65535 will not work!")
    if (Config.OWNERID == 0): # If Owner is not specified - warn the user
        warnings.warn("OWNERID is not set! Sadogire cannot be used to its full extent without an owner!")
    if (Config.LOGCHANNEL == 0): # If logchannel is not set - warn the user
        warnings.warn("LOGCHANNEL is not set! You will not receive log information via discord!")
    if (Config.SECRET == "TwinklingStar"): # If the secret is default - warn the user
        warnings.warn("You are running Sadogire with the default secret! This is unsecure and may grant access to any third party!")
    if (Config.TIMEOUT > 3000): # If timeout is over 3 seconds - issue a warning
        warnings.warn("Timeout is too high! This may cause sadogire to malfunction!")



# Monkeypatch, monkeypatch
def warnformat(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'

# Save function
async def SavePrep():
    await FileOperations.Save([Lists.ApprovedUsers, Lists.SilenceList], f"./data/{Config.FILENAME}")

# Load (and assign) stuff from the data file
async def Load():
    try:
        SavedList = await FileOperations.Load(f"./data/{Config.FILENAME}")
        Lists.ApprovedUsers = SavedList[0]
        Lists.SilenceList = SavedList[1]
    except Exception as e:
        warnings.warn("Unable to load, does data.sadogire exist?\nError:\n" + e)

def Boot():
    warnings.formatwarning = warnformat #Issue warnings without showing lines
    FileOperations.Setup()
    CheckConfig()
    Triton.run(Config.TOKEN)

Boot()