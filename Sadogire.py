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
from SadogireObjects import *
from Utility import Encryption, FileOperations, SadogirePermissions

import zmq # Communication via tcp
import zmq.asyncio

import json # Message enconding


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) # Error supression for zmq

# Server block start
async def Init():
    sock = zmq.asyncio.Context().socket(zmq.REP)
    sock.setsockopt(zmq.SNDTIMEO, Config.TIMEOUT)
    sock.bind(f"tcp://*:{Config.INPORT}")
    while True:
        Request = await Encryption.Unscramble(await sock.recv(), Config.SECRET)
        isSadoObject = await DetermineObject(Request)
        if (isSadoObject == False): # If Unknown - Deny
            await sock.send(b"You're delusional")
        else:
            Response = await Respond(Request)
            await sock.send(Response)
            


async def Respond(SadogireObject):
    return b"OK!"
    
async def DetermineObject(message):
    if (type(message) == Request or type(message) == NodeIdentity or type(message) == Reconfiguration): # Checks for Request Object
        return True
    else:
        return False

# Bot preconfiguration
Triton=commands.Bot(command_prefix="<", case_insensitive=True)

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
    await Load()
    print("Sadogire is running!")
    #await ActionLog("Sadogire instance is running. Awaiting nodes")

@Triton.command(name='query')
async def QueryUser(ctx, userid=None):
    if (userid==None):
        userid = ctx.author.id
    if (await SadogirePermissions.PermissionsCheck(ctx.author.id, Lists.ApprovedUsers) == False):
        await ctx.channel.send("You are not approved to use this command.")
    PermissionLevel=await SadogirePermissions.PermissionsCheck(int(userid), Lists.ApprovedUsers)
    if (PermissionLevel == False):
        await ctx.channel.send("This user is not approved")
    elif (PermissionLevel == 0):
        await ctx.channel.send("This user's permissions have been revoked.")
    else:
        await ctx.channel.send(f"This user is approved and has {PermissionLevel} Permission Level")

# Adds user, requires owner access
@Triton.command(name='approve')
async def ApproveUser(ctx, userid, level):
    if (await SadogirePermissions.PermissionsCheck(ctx.author.id, Lists.ApprovedUsers) == 3):
        print("Permissions check passed!")
        Lists.ApprovedUsers.append([int(userid), UserPermissions(int(level), False)])
    await SavePrep()



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

async def Load():
    try:
        SavedList = await FileOperations.Load(f"./data/{Config.FILENAME}")
        Lists.ApprovedUsers = SavedList[0]
        Lists.SilenceList = SavedList[1]
    except:
        print("Unable to load, does data.sadogire exist?")

def Boot():
    warnings.formatwarning = warnformat
    FileOperations.Setup()
    CheckConfig()
    Triton.run(Config.TOKEN)

Boot()